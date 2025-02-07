#!/bin/bash

readonly LOG_FILE="logs/proxy_usage.log"
readonly LOG_DIR=$(dirname "$LOG_FILE")

timestamp() {
    date +"%Y-%m-%d %H:%M:%S"
}

log_message() {
    echo "$(timestamp) - $1"
}

error_message() {
    echo "$(timestamp) - ERROR: $1" >&2
}

create_or_clear_log_file() {
    if [ -f "$LOG_FILE" ]; then
        # Clear the contents of the log file
        if : > "$LOG_FILE"; then
            log_message "Log file cleared: $LOG_FILE"
        else
            error_message "Failed to clear log file: $LOG_FILE"
            exit 1
        fi
    else
        # Create the log file if it does not exist
        # Create the log file if it does not exist
        if touch "$LOG_FILE"; then
            log_message "Log file created: $LOG_FILE"
        else
            error_message "Failed to create log file: $LOG_FILE"
            exit 1
        fi
    fi
}

log_message "Cleaning logs..."

# Check if the logs directory exists
if [ ! -d "$LOG_DIR" ]; then
    if mkdir -p "$LOG_DIR"; then
        log_message "Log directory created: $LOG_DIR"
    else
        error_message "Failed to create log directory: $LOG_DIR"
        exit 1
    fi
fi

# Create or clear the log file
create_or_clear_log_file

# Set the appropriate permissions for the log file
if chmod 644 "$LOG_FILE"; then
    log_message "Permissions set to 644 for: $LOG_FILE"
else
    error_message "Failed to set permissions for: $LOG_FILE"
    exit 1
fi