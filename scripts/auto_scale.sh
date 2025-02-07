#!/bin/bash

API_URL="${API_URL:-http://localhost:5000/api/v1/autoscale}"
DATA="${DATA:-'{"instances": 3}'}"
RETRIES="${RETRIES:-3}"
RETRY_DELAY="${RETRY_DELAY:-5}"

timestamp() {
    date +"%Y-%m-%d %H:%M:%S"
}

log_message() {
    echo "$(timestamp) - $1"
}

error_message() {
    echo "$(timestamp) - ERROR: $1" >&2
}

validate_response() {
    local response=$1
    if [[ "$response" =~ ^{3}$ ]]; then
        return 0
    else
        return 1
    fi
}

parse_response() {
    local response_body=$1
    if command -v jq &> /dev/null; then
        echo "$response_body" | jq.
    else
        echo "$response_body"
    fi
}

check_dependencies() {
    if! command -v curl &> /dev/null; then
        error_message "curl is not installed. Please install curl to use this script."
        exit 1
    fi

    if! command -v jq &> /dev/null; then
        log_message "jq is not installed. JSON responses will not be parsed."
    fi
}

auto_scale() {
    log_message "Auto-scaling proxies..."
    local attempt=0
    local response
    local response_body

    while [ $attempt -lt $RETRIES ]; do
        response_body=$(
            curl -s -w "%{http_code}" -u admin:password -X POST "$API_URL" \
            -H "Content-Type: application/json" -d "$DATA"
        )
        response="${response_body: -3}"
        response_body="${response_body::-3}"

        if validate_response "$response"; then
            case "$response" in
            200)
                log_message "Auto-scaling request successful."
                parse_response "$response_body"
                return 0
              ;;
            400)
                error_message "Bad request: $response"
                parse_response "$response_body"
                return 1
              ;;
            401)
                error_message "Unauthorized: $response"
                parse_response "$response_body"
                return 1
              ;;
            500)
                error_message "Internal server error: $response"
                parse_response "$response_body"
              ;;
            *)
                error_message "Auto-scaling request failed with status code: $response"
                parse_response "$response_body"
              ;;
            esac
        else
            error_message "Invalid response received: $response"
        fi

        attempt=$((attempt + 1))
        log_message "Retrying in $RETRY_DELAY seconds... (Attempt: $attempt/$RETRIES)"
        sleep "$RETRY_DELAY"
    done

    error_message "Auto-scaling request failed after $RETRIES attempts."
    exit 1
}

check_dependencies
auto_scale