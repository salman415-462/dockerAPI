#!/bin/bash

case "$1" in
    start)
        echo "Starting FastAPI server..."
        python run.py &
        echo "Server started. PID: $!"
        echo "Access at: http://localhost:8000"
        echo "Docs at: http://localhost:8000/docs"
        ;;
    stop)
        echo "Stopping FastAPI server..."
        pkill -f "python run.py"
        echo "Server stopped"
        ;;
    restart)
        echo "Restarting FastAPI server..."
        pkill -f "python run.py"
        sleep 2
        python run.py &
        echo "Server restarted. PID: $!"
        ;;
    status)
        if pgrep -f "python run.py" > /dev/null; then
            echo "✅ Server is running"
            echo "   Access: http://localhost:8000"
            echo "   Docs:   http://localhost:8000/docs"
            
            # Test if responding
            if curl -s http://localhost:8000/health > /dev/null; then
                echo "   Status: Healthy"
            else
                echo "   Status: Not responding"
            fi
        else
            echo "❌ Server is not running"
        fi
        ;;
    test)
        echo "Testing API endpoints..."
        curl -s http://localhost:8000/health | python3 -m json.tool
        ;;
    logs)
        echo "Recent server activity:"
        journalctl -u $(pgrep -f "python run.py") --since "5 minutes ago" 2>/dev/null || \
        echo "Note: Run 'journalctl -f' in another terminal to see live logs"
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|test|logs}"
        echo ""
        echo "Commands:"
        echo "  start    - Start the FastAPI server"
        echo "  stop     - Stop the FastAPI server"
        echo "  restart  - Restart the FastAPI server"
        echo "  status   - Check server status"
        echo "  test     - Test API health"
        echo "  logs     - Show recent logs"
        exit 1
        ;;
esac
