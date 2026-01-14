#!/bin/bash

# Edu Agents - Development Script
# Usage: ./scripts/dev.sh <command>

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_help() {
    echo "Edu Agents - Development Script"
    echo ""
    echo "Usage: ./scripts/dev.sh <command>"
    echo ""
    echo "Commands:"
    echo "  setup          Setup all services (venv + dependencies)"
    echo "  setup-web      Setup web service only"
    echo "  setup-agent    Setup agent service only"
    echo "  run-web        Run web service locally"
    echo "  run-agent      Run agent service locally"
    echo "  docker-up      Start all services with Docker"
    echo "  docker-down    Stop all Docker services"
    echo "  supabase-up    Start Supabase locally"
    echo "  supabase-down  Stop Supabase"
    echo "  supabase-logs  View Supabase logs"
    echo "  clean          Remove all virtual environments"
    echo "  help           Show this help message"
    echo ""
    echo "Supabase URLs (when running):"
    echo "  Studio:    http://localhost:3000"
    echo "  API:       http://localhost:8000"
    echo "  Database:  postgresql://postgres:postgres@localhost:5432/postgres"
}

setup_web() {
    echo -e "${GREEN}Setting up web service...${NC}"
    cd "$PROJECT_ROOT/services/web"
    uv venv
    uv pip install -e ".[dev]"
    echo -e "${GREEN}Web service setup complete!${NC}"
}

setup_agent() {
    echo -e "${GREEN}Setting up agent service...${NC}"
    cd "$PROJECT_ROOT/services/agent"
    uv venv
    uv pip install -e ".[dev]"
    echo -e "${GREEN}Agent service setup complete!${NC}"
}

setup_all() {
    setup_web
    setup_agent
    echo -e "${GREEN}All services setup complete!${NC}"
}

run_web() {
    echo -e "${GREEN}Starting web service...${NC}"
    cd "$PROJECT_ROOT/services/web"
    uv run streamlit run app.py
}

run_agent() {
    echo -e "${GREEN}Starting agent service...${NC}"
    cd "$PROJECT_ROOT/services/agent"
    uv run uvicorn main:app --reload --port 8000
}

docker_up() {
    echo -e "${GREEN}Starting Docker services...${NC}"
    cd "$PROJECT_ROOT"
    docker-compose up --build
}

docker_down() {
    echo -e "${YELLOW}Stopping Docker services...${NC}"
    cd "$PROJECT_ROOT"
    docker-compose down
}

supabase_up() {
    echo -e "${GREEN}Starting Supabase...${NC}"
    cd "$PROJECT_ROOT/supabase"
    docker-compose up -d
    echo -e "${GREEN}Supabase started!${NC}"
    echo ""
    echo "Supabase URLs:"
    echo "  Studio:    http://localhost:3000"
    echo "  API:       http://localhost:8000"
    echo "  Database:  postgresql://postgres:postgres@localhost:5432/postgres"
    echo ""
    echo "Anon Key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0"
}

supabase_down() {
    echo -e "${YELLOW}Stopping Supabase...${NC}"
    cd "$PROJECT_ROOT/supabase"
    docker-compose down
    echo -e "${GREEN}Supabase stopped!${NC}"
}

supabase_logs() {
    echo -e "${GREEN}Showing Supabase logs...${NC}"
    cd "$PROJECT_ROOT/supabase"
    docker-compose logs -f
}

clean() {
    echo -e "${YELLOW}Cleaning virtual environments...${NC}"
    rm -rf "$PROJECT_ROOT/services/web/.venv"
    rm -rf "$PROJECT_ROOT/services/agent/.venv"
    echo -e "${GREEN}Clean complete!${NC}"
}

# Main
case "${1:-help}" in
    setup)
        setup_all
        ;;
    setup-web)
        setup_web
        ;;
    setup-agent)
        setup_agent
        ;;
    run-web)
        run_web
        ;;
    run-agent)
        run_agent
        ;;
    docker-up)
        docker_up
        ;;
    docker-down)
        docker_down
        ;;
    supabase-up)
        supabase_up
        ;;
    supabase-down)
        supabase_down
        ;;
    supabase-logs)
        supabase_logs
        ;;
    clean)
        clean
        ;;
    help|--help|-h)
        print_help
        ;;
    *)
        echo -e "${RED}Unknown command: $1${NC}"
        echo ""
        print_help
        exit 1
        ;;
esac
