<#
.SYNOPSIS
    MaintAI DevOps Automation Utility for PowerShell
.DESCRIPTION
    Quick command-line tool to build, run, test, and manage containers and environments.
.EXAMPLE
    .\scripts\devops.ps1 build
    .\scripts\devops.ps1 docker-build
    .\scripts\devops.ps1 up
    .\scripts\devops.ps1 health
#>

param (
    [Parameter(Position = 0)]
    [ValidateSet("help", "install", "dev", "build", "lint", "typecheck", "docker-build", "docker-run", "up", "up-proxy", "down", "logs", "health", "clean")]
    [string]$Command = "help"
)

function Show-Help {
    Write-Host "==========================================================" -ForegroundColor Cyan
    Write-Host "   MaintAI DevOps PowerShell Utility" -ForegroundColor Cyan
    Write-Host "==========================================================" -ForegroundColor Cyan
    Write-Host "Commands:"
    Write-Host "  install        Install dependencies with npm ci" -ForegroundColor Green
    Write-Host "  dev            Run local development server" -ForegroundColor Green
    Write-Host "  build          Build Next.js standalone application" -ForegroundColor Green
    Write-Host "  lint           Run ESLint checks" -ForegroundColor Green
    Write-Host "  typecheck      Run TypeScript strict type-check" -ForegroundColor Green
    Write-Host "  docker-build   Build production Docker container image" -ForegroundColor Green
    Write-Host "  docker-run     Run container locally with .env.local on port 3000" -ForegroundColor Green
    Write-Host "  up             Start stack in background via Docker Compose" -ForegroundColor Green
    Write-Host "  up-proxy       Start stack including Nginx reverse proxy" -ForegroundColor Green
    Write-Host "  down           Stop Docker Compose stack" -ForegroundColor Green
    Write-Host "  logs           View real-time logs from maintai-app container" -ForegroundColor Green
    Write-Host "  health         Test local /api/health endpoint" -ForegroundColor Green
    Write-Host "  clean          Clean build output and temporary caches" -ForegroundColor Green
    Write-Host ""
}

switch ($Command) {
    "help" {
        Show-Help
    }
    "install" {
        Write-Host "Installing dependencies..." -ForegroundColor Yellow
        npm ci
    }
    "dev" {
        Write-Host "Starting local dev server..." -ForegroundColor Yellow
        npm run dev
    }
    "build" {
        Write-Host "Building Next.js standalone app..." -ForegroundColor Yellow
        npm run build
    }
    "lint" {
        Write-Host "Running linter..." -ForegroundColor Yellow
        npm run lint
    }
    "typecheck" {
        Write-Host "Checking TypeScript types..." -ForegroundColor Yellow
        npm run typecheck
    }
    "docker-build" {
        Write-Host "Building Docker image (maintai:latest)..." -ForegroundColor Yellow
        docker build -t maintai:latest .
    }
    "docker-run" {
        Write-Host "Running Docker container on http://localhost:3000..." -ForegroundColor Yellow
        docker run --rm -p 3000:3000 --env-file .env.local --name maintai-test maintai:latest
    }
    "up" {
        Write-Host "Starting stack in background..." -ForegroundColor Yellow
        docker compose up -d
    }
    "up-proxy" {
        Write-Host "Starting stack with Nginx reverse proxy..." -ForegroundColor Yellow
        docker compose --profile proxy up -d
    }
    "down" {
        Write-Host "Stopping stack..." -ForegroundColor Yellow
        docker compose down
    }
    "logs" {
        docker compose logs -f maintai-app
    }
    "health" {
        Write-Host "Querying health check endpoint..." -ForegroundColor Yellow
        try {
            $response = Invoke-RestMethod -Uri "http://localhost:3000/api/health" -Method Get
            $response | ConvertTo-Json -Depth 5
        } catch {
            Write-Error "Failed to reach health endpoint: $_"
        }
    }
    "clean" {
        Write-Host "Cleaning build folders..." -ForegroundColor Yellow
        if (Test-Path ".next") { Remove-Item -Recurse -Force ".next" }
        if (Test-Path "out") { Remove-Item -Recurse -Force "out" }
        Write-Host "Clean completed." -ForegroundColor Green
    }
}
