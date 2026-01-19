# Edu Agents - Development Script (Windows PowerShell)
# Usage: .\scripts\dev.ps1 <command>

param(
    [Parameter(Position=0)]
    [string]$Command = "help"
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

function Write-ColorOutput($ForegroundColor, $Message) {
    Write-Host $Message -ForegroundColor $ForegroundColor
}

function Show-Help {
    Write-Host "Edu Agents - Development Script (Windows)"
    Write-Host ""
    Write-Host "Usage: .\scripts\dev.ps1 <command>"
    Write-Host ""
    Write-Host "Commands:"
    Write-Host "  setup          Setup all services (venv + dependencies)"
    Write-Host "  setup-web      Setup web service only"
    Write-Host "  setup-agent    Setup agent service only"
    Write-Host "  run-web        Run web service locally"
    Write-Host "  run-agent      Run agent service locally"
    Write-Host "  docker-up      Start all services with Docker"
    Write-Host "  docker-down    Stop all Docker services"
    Write-Host "  supabase-up    Start Supabase locally"
    Write-Host "  supabase-down  Stop Supabase"
    Write-Host "  supabase-logs  View Supabase logs"
    Write-Host "  clean          Remove all virtual environments"
    Write-Host "  help           Show this help message"
    Write-Host ""
    Write-Host "Supabase URLs (when running):"
    Write-Host "  Studio:    http://localhost:3000"
    Write-Host "  API:       http://localhost:8000"
    Write-Host "  Database:  postgresql://postgres:postgres@localhost:5432/postgres"
}

function Setup-Web {
    Write-ColorOutput Green "Setting up web service..."
    Push-Location "$ProjectRoot\services\web"
    try {
        uv venv
        uv pip install -e ".[dev]"
        Write-ColorOutput Green "Web service setup complete!"
    } finally {
        Pop-Location
    }
}

function Setup-Agent {
    Write-ColorOutput Green "Setting up agent service..."
    Push-Location "$ProjectRoot\services\agent"
    try {
        uv venv
        uv pip install -e ".[dev]"
        Write-ColorOutput Green "Agent service setup complete!"
    } finally {
        Pop-Location
    }
}

function Setup-All {
    Setup-Web
    Setup-Agent
    Write-ColorOutput Green "All services setup complete!"
}

function Run-Web {
    Write-ColorOutput Green "Starting web service..."
    Push-Location "$ProjectRoot\services\web"
    try {
        uv run streamlit run app.py
    } finally {
        Pop-Location
    }
}

function Run-Agent {
    Write-ColorOutput Green "Starting agent service..."
    Push-Location "$ProjectRoot\services\agent"
    try {
        uv run uvicorn main:app --reload --port 8000
    } finally {
        Pop-Location
    }
}

function Docker-Up {
    Write-ColorOutput Green "Starting Docker services..."
    Push-Location $ProjectRoot
    try {
        docker-compose up --build
    } finally {
        Pop-Location
    }
}

function Docker-Down {
    Write-ColorOutput Yellow "Stopping Docker services..."
    Push-Location $ProjectRoot
    try {
        docker-compose down
    } finally {
        Pop-Location
    }
}

function Supabase-Up {
    Write-ColorOutput Green "Starting Supabase..."
    Push-Location "$ProjectRoot\supabase"
    try {
        docker-compose up -d
        Write-ColorOutput Green "Supabase started!"
        Write-Host ""
        Write-Host "Supabase URLs:"
        Write-Host "  Studio:    http://localhost:3000"
        Write-Host "  API:       http://localhost:8000"
        Write-Host "  Database:  postgresql://postgres:postgres@localhost:5432/postgres"
        Write-Host ""
        Write-Host "Anon Key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0"
    } finally {
        Pop-Location
    }
}

function Supabase-Down {
    Write-ColorOutput Yellow "Stopping Supabase..."
    Push-Location "$ProjectRoot\supabase"
    try {
        docker-compose down
        Write-ColorOutput Green "Supabase stopped!"
    } finally {
        Pop-Location
    }
}

function Supabase-Logs {
    Write-ColorOutput Green "Showing Supabase logs..."
    Push-Location "$ProjectRoot\supabase"
    try {
        docker-compose logs -f
    } finally {
        Pop-Location
    }
}

function Clean-Envs {
    Write-ColorOutput Yellow "Cleaning virtual environments..."
    $webVenv = "$ProjectRoot\services\web\.venv"
    $agentVenv = "$ProjectRoot\services\agent\.venv"

    if (Test-Path $webVenv) {
        Remove-Item -Recurse -Force $webVenv
    }
    if (Test-Path $agentVenv) {
        Remove-Item -Recurse -Force $agentVenv
    }
    Write-ColorOutput Green "Clean complete!"
}

# Main
switch ($Command.ToLower()) {
    "setup"         { Setup-All }
    "setup-web"     { Setup-Web }
    "setup-agent"   { Setup-Agent }
    "run-web"       { Run-Web }
    "run-agent"     { Run-Agent }
    "docker-up"     { Docker-Up }
    "docker-down"   { Docker-Down }
    "supabase-up"   { Supabase-Up }
    "supabase-down" { Supabase-Down }
    "supabase-logs" { Supabase-Logs }
    "clean"         { Clean-Envs }
    "help"          { Show-Help }
    "--help"        { Show-Help }
    "-h"            { Show-Help }
    default {
        Write-ColorOutput Red "Unknown command: $Command"
        Write-Host ""
        Show-Help
        exit 1
    }
}
