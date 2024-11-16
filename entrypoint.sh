#!/bin/bash
set -e
# ensures that the script exits immediately if any command exits with a non-zero status (i.e., an error).
set -o errexit
# ensures that if any command in a pipeline fails, the whole pipeline fails.
set -o pipefail
# ensures that any attempts to use an undefined variable will cause the script to exit.
set -o nounset
# useful for debugging, print each command before executing it.
# set -o xtrace

# Configuration
APP_DIR="/code/auction"
MANAGE_PY="$APP_DIR/manage.py"
SOCK_FILE="$APP_DIR/uwsgi_app.sock"
MAX_RETRIES=5
RETRY_INTERVAL=5

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Logging functions (same as before)
log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# environment check based on docker-compose.yml
check_environment() {
    log_info "Checking environment variables..."
    required_vars=(
        # Django Configuration
        "DJANGO_SETTINGS_MODULE"
        "DEBUG_STATUS"
        "DJANGO_SECRET_KEY"
        "ALLOWED_HOSTS"
        
        # Database Configuration
        "DB_NAME"
        "DB_USER"
        "DB_PASSWORD"
        "DB_HOST"
        "DB_PORT"
        
        # Message Broker Configuration
        "CELERY_BROKER_URL"
        "CELERY_RESULT_BACKEND"
        
        # Email Configuration
        "EMAIL_HOST_USER"
        "EMAIL_HOST_PASSWORD"
        
        # # OAuth Configuration - Required for Google Signin
        # "SOCIAL_AUTH_GOOGLE_OAUTH2_KEY"
        # "SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET"
    )

    for var in "${required_vars[@]}"; do
        if [ -z "${!var}" ]; then
            log_error "Required environment variable $var is not set"
            exit 1
        fi
    done
    log_info "Environment check passed"
}

# service dependency checks
check_service_health() {
    log_info "Checking service dependencies..."

    # Check PostgreSQL
    check_postgres() {
        log_info "Checking PostgreSQL connection..."
        python3 << END
import sys
import psycopg2
try:
    conn = psycopg2.connect(
        dbname="${DB_NAME}",
        user="${DB_USER}",
        password="${DB_PASSWORD}",
        host="${DB_HOST}",
        port="${DB_PORT}",
        connect_timeout=5
    )
    conn.close()
    sys.exit(0)
except Exception as e:
    print(f"Database connection failed: {e}", file=sys.stderr)
    sys.exit(1)
END
    }


    # # Check Redis -require redis-tools
    # check_redis() {
    #     log_info "Checking Redis connection..."
    #     redis-cli -h cache ping >/dev/null 2>&1
    #     return $?
    # }

    # # Check RabbitMQ - requires rabbitmqctl package
    # check_rabbitmq() {
    #     log_info "Checking RabbitMQ connection..."
    #     rabbitmqctl status >/dev/null 2>&1
    #     return $?
    # }

    # Retry mechanism for services
    retry_service() {
        local service=$1
        local check_function=$2
        local retries=0

        while ! $check_function; do
            retries=$((retries + 1))
            if [ $retries -ge $MAX_RETRIES ]; then
                log_error "Unable to connect to $service after $MAX_RETRIES attempts"
                return 1
            fi
            log_warn "$service is unavailable - retry $retries/$MAX_RETRIES"
            sleep $RETRY_INTERVAL
        done
        log_info "$service connection established"
        return 0
    }

    # Check all services
    retry_service "PostgreSQL" check_postgres || exit 1
    # retry_service "Redis" check_redis || exit 1
    # retry_service "RabbitMQ" check_rabbitmq || exit 1
}

set_permissions() {
    log_info "Setting file permissions..."

    # Set directory permissions
    if ! chmod 755 "$APP_DIR"; then
        log_error "Failed to set directory permissions for $APP_DIR"
        exit 1
    fi

    # Create socket file if it doesn't exist
    if [ ! -e "$SOCK_FILE" ]; then
        touch "$SOCK_FILE"
    fi

    # Set socket file permissions
    if ! chmod 666 "$SOCK_FILE"; then
        log_error "Failed to set permissions for $SOCK_FILE"
        exit 1
    fi

    log_info "File permissions set successfully"
}


# static files handling
handle_static() {
    log_info "Collecting static files..."
    
    if ! python3 $MANAGE_PY collectstatic --noinput; then
        log_error "Failed to collect static files"
        exit 1
    fi
    log_info "Static files collected successfully"
}


# Handle database migrations
handle_migrations() {
    log_info "Running database migrations..."
    
    # Run makemigrations first
    if ! python3 $MANAGE_PY makemigrations --noinput; then
        log_error "Failed to make migrations"
        exit 1
    fi
    
    # Then apply migrations
    if ! python3 $MANAGE_PY migrate --noinput; then
        log_error "Failed to apply migrations"
        exit 1
    fi
    
    log_info "Database migrations completed successfully"
}


# Django checks
django_security_checks() {
    log_info "Running Django security checks..."
    
    # Check debug status
    if [ "$DEBUG_STATUS" = "True" ]; then
        log_warn "Debug mode is enabled. This is not recommended for production!"
    fi
    
    # Check allowed hosts
    if [[ "$ALLOWED_HOSTS" == *"*"* ]]; then
        log_warn "ALLOWED_HOSTS contains '*'. This is not recommended for production!"
    fi
    
    # Run Django system checks - in prod
    # python3 $MANAGE_PY check --deploy
}

# Create superuser if needed
create_superuser() {
    if [ ! -z "$DJANGO_SUPERUSER_USERNAME" ] && [ ! -z "$DJANGO_SUPERUSER_PASSWORD" ] && [ ! -z "$DJANGO_SUPERUSER_EMAIL" ]; then
        log_info "Creating superuser..."
        python3 $MANAGE_PY createsuperuser --noinput || log_warn "Superuser already exists"
    fi
}

# Cleanup function
cleanup() {
    log_info "Performing cleanup..."
    
    # Remove socket files
    find "$APP_DIR" -type s -delete
    
    # Remove pid files
    find "$APP_DIR" -name "*.pid" -delete
    
    # Clear temporary files
    find "$APP_DIR" -name "*.pyc" -delete
    find "$APP_DIR" -name "__pycache__" -type d -exec rm -r {} +
    
    log_info "Cleanup completed"
}

# Main execution
main() {
    if [ "$1" = "--help" ]; then
        show_help
        exit 0
    fi

    log_info "Starting initialization process..."

    # Set up signal handlers
    trap cleanup EXIT
    trap 'log_error "Received SIGINT/SIGTERM"; cleanup; exit 1' SIGINT SIGTERM

    # Run initialization steps
    check_environment
    check_service_health
    set_permissions
    handle_migrations
    django_security_checks
    create_superuser

    # Service-specific initialization
    case "$1" in
        "uwsgi")
            log_info "Initializing uWSGI server..."
            ;;
        "daphne")
            log_info "Initializing Daphne server..."
            ;;
        "celery")
            log_info "Initializing Celery worker..."
            ;;
    esac

    log_info "Initialization complete"
    log_info "Executing command: $@"

    exec "$@"
}

# Start execution
main "$@"
