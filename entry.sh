#!/bin/bash
# ensures that the script exits immediately if any command exits with a non-zero status (i.e., an error).
set -o errexit
# ensures that if any command in a pipeline fails, the whole pipeline fails.
set -o pipefail
# ensures that any attempts to use an undefined variable will cause the script to exit.
set -o nounset
# useful for debugging, print each command before executing it.
set -o xtrace


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
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to handle cleanup on exit
cleanup() {
    log_info "Performing cleanup..."
    if [ -f "$SOCK_FILE" ]; then
        rm -f "$SOCK_FILE"
        log_info "Removed socket file"
    fi
}

# Check if required environment variables are set
check_environment() {
    log_info "Checking environment variables..."
    required_vars=(
        "DJANGO_SECRET_KEY"
        "DJANGO_SETTINGS_MODULE"
        "DATABASE_URL"
    )

    for var in "${required_vars[@]}"; do
        if [ -z "${!var}" ]; then
            log_error "Required environment variable $var is not set"
            exit 1
        fi
    done
    log_info "Environment check passed"
}

# Wait for database to be ready
wait_for_db() {
    log_info "Waiting for database connection..."
    retries=0
    until python3 $MANAGE_PY check --database default >/dev/null 2>&1; do
        retries=$((retries + 1))
        if [ $retries -ge $MAX_RETRIES ]; then
            log_error "Unable to connect to database after $MAX_RETRIES attempts"
            exit 1
        fi
        log_warn "Database is unavailable - retry $retries/$MAX_RETRIES"
        sleep $RETRY_INTERVAL
    done
    log_info "Database connection established"
}

# Function to set file permissions
set_permissions() {
    log_info "Setting file permissions..."
    if ! chmod 755 "$APP_DIR"; then
        log_error "Failed to set permissions on $APP_DIR"
        exit 1
    fi
    
    # Create socket file if it doesn't exist
    touch "$SOCK_FILE"
    if ! chmod 664 "$SOCK_FILE"; then
        log_error "Failed to set permissions on $SOCK_FILE"
        exit 1
    fi
    log_info "File permissions set successfully"
}

# Function to handle Django migrations
handle_migrations() {
    log_info "Running database migrations..."
    
    # Make migrations for specific apps
    apps=("account" "lot" "chat" "payment" "reviews")
    for app in "${apps[@]}"; do
        if ! python3 $MANAGE_PY makemigrations $app --noinput; then
            log_error "Failed to make migrations for $app"
            exit 1
        fi
    done
    
    # Apply migrations
    if ! python3 $MANAGE_PY migrate --noinput; then
        log_error "Failed to apply migrations"
        exit 1
    fi
    log_info "Migrations completed successfully"
}

# Function to collect static files
handle_static() {
    log_info "Collecting static files..."
    if ! python3 $MANAGE_PY collectstatic --noinput; then
        log_error "Failed to collect static files"
        exit 1
    fi
    log_info "Static files collected successfully"
}

# Function to run Django health checks
health_check() {
    log_info "Running Django health checks..."
    if ! python3 $MANAGE_PY check --deploy; then
        log_warn "Some health checks failed"
        # Don't exit here, just warn
    fi
}

# Show help message
show_help() {
    echo "Usage: $0 [command]"
    echo "Docker entrypoint script for Django application"
    echo ""
    echo "If no command is provided, the script will:"
    echo "  1. Check environment variables"
    echo "  2. Wait for database connection"
    echo "  3. Set up file permissions"
    echo "  4. Run database migrations"
    echo "  5. Collect static files"
    echo "  6. Run health checks"
    echo "  7. Execute the provided command"
    echo ""
    echo "Options:"
    echo "  --help    Show this help message"
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
    trap 'log_error "Received SIGINT/SIGTERM"; exit 1' SIGINT SIGTERM

    # Run initialization steps
    check_environment
    wait_for_db
    set_permissions
    handle_migrations
    handle_static
    health_check

    log_info "Initialization complete"
    log_info "Executing command: $@"

    # Execute the passed command
    exec "$@"
}

# Start execution
main "$@"
