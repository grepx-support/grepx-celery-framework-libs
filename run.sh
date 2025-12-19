#!/bin/bash
set -e

cd "$(dirname "$0")"

VENV_DIR="venv"
CELERY_PID_FILE="celery.pid"
FLOWER_PID_FILE="flower.pid"
CELERY_LOG_FILE="celery.log"
FLOWER_LOG_FILE="flower.log"
FLOWER_PORT=5555

# Activate venv
activate_venv() {
    if [ -f "$VENV_DIR/bin/activate" ]; then
        source "$VENV_DIR/bin/activate"
    elif [ -f "$VENV_DIR/Scripts/activate" ]; then
        source "$VENV_DIR/Scripts/activate"
    else
        echo "ERROR: venv not found. Run ./setup.sh first"
        exit 1
    fi
}

# Start Celery
start_celery() {
    if [ -f "$CELERY_PID_FILE" ]; then
        PID=$(cat "$CELERY_PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            echo "Celery is already running (PID: $PID)"
            return 1
        else
            rm -f "$CELERY_PID_FILE"
        fi
    fi

    echo "Starting Celery worker..."
    nohup celery -A example_app:app worker --loglevel=info > "$CELERY_LOG_FILE" 2>&1 &
    PID=$!
    echo $PID > "$CELERY_PID_FILE"
    echo "✓ Celery started (PID: $PID)"
}

# Start Flower
start_flower() {
    if [ -f "$FLOWER_PID_FILE" ]; then
        PID=$(cat "$FLOWER_PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            echo "Flower is already running (PID: $PID)"
            return 1
        else
            rm -f "$FLOWER_PID_FILE"
        fi
    fi

    echo "Starting Flower..."
    nohup celery -A example_app:app flower --port=$FLOWER_PORT > "$FLOWER_LOG_FILE" 2>&1 &
    PID=$!
    echo $PID > "$FLOWER_PID_FILE"
    echo "✓ Flower started (PID: $PID) on http://localhost:$FLOWER_PORT"
}

# Start both
start() {
    activate_venv
    start_celery
    sleep 1
    start_flower
    echo ""
    echo "Services started:"
    echo "  Celery worker: tail -f $CELERY_LOG_FILE"
    echo "  Flower UI: http://localhost:$FLOWER_PORT"
}

# Stop Celery
stop_celery() {
    if [ ! -f "$CELERY_PID_FILE" ]; then
        pkill -f "celery.*example_app.*worker" 2>/dev/null || true
        return 0
    fi

    PID=$(cat "$CELERY_PID_FILE")
    echo "Stopping Celery (PID: $PID)..."

    if kill -0 "$PID" 2>/dev/null; then
        kill "$PID" 2>/dev/null || true
        sleep 2

        if kill -0 "$PID" 2>/dev/null; then
            kill -9 "$PID" 2>/dev/null || true
        fi
    fi

    pkill -f "celery.*example_app.*worker" 2>/dev/null || true
    rm -f "$CELERY_PID_FILE"
    echo "✓ Celery stopped"
}

# Stop Flower
stop_flower() {
    if [ ! -f "$FLOWER_PID_FILE" ]; then
        pkill -f "celery.*example_app.*flower" 2>/dev/null || true
        return 0
    fi

    PID=$(cat "$FLOWER_PID_FILE")
    echo "Stopping Flower (PID: $PID)..."

    if kill -0 "$PID" 2>/dev/null; then
        kill "$PID" 2>/dev/null || true
        sleep 1

        if kill -0 "$PID" 2>/dev/null; then
            kill -9 "$PID" 2>/dev/null || true
        fi
    fi

    pkill -f "celery.*example_app.*flower" 2>/dev/null || true
    rm -f "$FLOWER_PID_FILE"
    echo "✓ Flower stopped"
}

# Stop both
stop() {
    stop_flower
    stop_celery
}

# Status
status() {
    echo "Service Status:"
    echo ""

    # Celery status
    if [ -f "$CELERY_PID_FILE" ]; then
        PID=$(cat "$CELERY_PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            echo "✓ Celery is running (PID: $PID)"
        else
            echo "✗ Celery is not running (stale PID)"
            rm -f "$CELERY_PID_FILE"
        fi
    else
        echo "✗ Celery is not running"
    fi

    # Flower status
    if [ -f "$FLOWER_PID_FILE" ]; then
        PID=$(cat "$FLOWER_PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            echo "✓ Flower is running (PID: $PID) on http://localhost:$FLOWER_PORT"
        else
            echo "✗ Flower is not running (stale PID)"
            rm -f "$FLOWER_PID_FILE"
        fi
    else
        echo "✗ Flower is not running"
    fi
}

# Restart
restart() {
    echo "Restarting services..."
    stop 2>/dev/null || true
    sleep 2
    start
}

# Logs
logs() {
    case "${2:-celery}" in
        celery)
            if [ -f "$CELERY_LOG_FILE" ]; then
                tail -f "$CELERY_LOG_FILE"
            else
                echo "No Celery log file found"
                exit 1
            fi
            ;;
        flower)
            if [ -f "$FLOWER_LOG_FILE" ]; then
                tail -f "$FLOWER_LOG_FILE"
            else
                echo "No Flower log file found"
                exit 1
            fi
            ;;
        *)
            echo "Usage: ./run.sh logs {celery|flower}"
            exit 1
            ;;
    esac
}

# Main
case "${1:-}" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    status)
        status
        ;;
    logs)
        logs "$@"
        ;;
    *)
        echo "Usage: ./run.sh {start|stop|restart|status|logs}"
        echo ""
        echo "Commands:"
        echo "  start         - Start Celery worker and Flower"
        echo "  stop          - Stop Celery worker and Flower"
        echo "  restart       - Restart both services"
        echo "  status        - Check service status"
        echo "  logs celery   - Tail Celery logs"
        echo "  logs flower   - Tail Flower logs"
        exit 1
        ;;
esac
