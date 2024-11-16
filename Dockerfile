# Stage 1: Build stage
FROM python:3.12-alpine AS builder

# ensures that the Python interpreter doesn’t generate .pyc
ENV PYTHONDONTWRITEBYTECODE=1
# send python output to the terminal without being buffered in real-time
ENV PYTHONUNBUFFERED=1

# Working directory
WORKDIR /code

# Define build arguments for user and group names and IDs
ARG USER_NAME=test
ARG GROUP_NAME=test
ARG USER_UID=1000
ARG USER_GID=${USER_UID}
# Build-time arguments
ARG BUILD_ENV=production

# Install build dependencies
RUN apk add --no-cache --virtual .build-deps \
    gcc musl-dev python3-dev \
    # for psycopg2-binary package installation
    && apk add postgresql-dev \
    # Install Pillow dependencies and other system libraries
    && apk add jpeg-dev zlib-dev libjpeg \
    # Install uWSGI dependencies
    && apk add build-base linux-headers pcre-dev \
    # Upgrade pip
    && python3 -m pip install --upgrade pip \
    # Cleanup: Remove build dependencies and unnecessary cache
    && apk del .build-deps \
    && rm -rf /var/cache/apk/*
    

# create a new user and group by assigning the specified user ID (USER_UID), group ID (USER_GID), and home directory, associating the user with the defined group.
RUN addgroup -g ${USER_GID} ${GROUP_NAME} && \
    adduser -u ${USER_UID} -G ${GROUP_NAME} -S -h /home/${USER_NAME} ${USER_NAME}

# Copy and install Python dependenciese
COPY --chown=${USER_NAME}:${GROUP_NAME} ./requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime stage
FROM python:3.12-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Working directory
WORKDIR /code

# Define build arguments for user and group names and IDs
ARG USER_NAME=test
ARG GROUP_NAME=test
ARG USER_UID=1000
ARG USER_GID=${USER_UID}

# Install runtime dependencies (excluding build tools)
RUN apk add --no-cache postgresql-libs libjpeg libpng pcre curl bash dos2unix

# Re-create the user in the runtime stage
RUN addgroup -g ${USER_GID} ${GROUP_NAME} && \
    adduser -u ${USER_UID} -G ${GROUP_NAME} -S -h /home/${USER_NAME} ${USER_NAME}

# Copy installed Python packages and binaries from the build stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy the application code
COPY --chown=${USER_NAME}:${GROUP_NAME} . .

# Use the non-root user to run the app
USER ${USER_NAME}:${GROUP_NAME}

RUN chmod +x /code/wait-for-it.sh
