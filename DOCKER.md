# Docker Deployment Guide

This guide explains how to run the LLM Bootcamp Project using Docker and docker-compose.

## Prerequisites

- Docker (version 20.10+)
- Docker Compose (version 2.0+)
- Make (optional, for easier command execution)

## Quick Start

### 1. Setup Environment Variables

Copy the environment template and add your API keys:

```bash
cp .env.template .env
```

Edit `.env` and add your keys:

```bash
OPENAI_API_KEY=sk-proj-your-key-here
TAVILY_API_KEY=tvly-your-key-here
MCP_SERVER_URL=http://mcp-server:8000
```

### 2. Start the Application

#### Using Make (Recommended)

```bash
# Build and start the application
make build
make up

# Or in one command
make rebuild
```

#### Using Docker Compose

```bash
# Build images
docker-compose build

# Start the application
docker-compose up -d
```

### 3. Access the Application

Open your browser and navigate to:
- **Application**: http://localhost:8501
- **Health Check**: http://localhost:8501/_stcore/health

## Available Make Commands

Run `make help` to see all available commands:

| Command | Description |
|---------|-------------|
| `make build` | Build Docker images |
| `make up` | Start the application |
| `make up-mcp` | Start with MCP server enabled |
| `make down` | Stop the application |
| `make restart` | Restart the application |
| `make logs` | Show application logs |
| `make logs-app` | Show only app logs |
| `make shell` | Open shell in app container |
| `make health` | Check application health |
| `make clean` | Remove containers and volumes |
| `make clean-cache` | Clear vectorstore cache |
| `make rebuild` | Rebuild and restart |
| `make lint` | Run ruff linting |
| `make format` | Format code with ruff |

## Advanced Usage

### Running with MCP Server

To enable the MCP server for advanced agent features:

```bash
make up-mcp
```

The MCP server will be available at http://localhost:8000

### Development Mode

For development with live code reloading:

```bash
make dev
```

This runs the containers in the foreground with source code mounted.

### Viewing Logs

```bash
# All logs
make logs

# Only application logs
make logs-app

# Only MCP server logs (if running)
make logs-mcp
```

### Accessing Container Shell

```bash
make shell
```

### Cleaning Up

```bash
# Remove containers and volumes
make clean

# Clear only the vectorstore cache
make clean-cache

# Remove all Docker resources (including images)
make prune
```

## Docker Compose Services

### streamlit-app (Main Application)

- **Port**: 8501
- **Health Check**: Every 30s
- **Volumes**:
  - `./tmp` - For file uploads and cache
  - `.` - Source code (development mode)

### mcp-server (Optional)

- **Port**: 8000
- **Profile**: mcp (only runs with `--profile mcp`)
- **Purpose**: Prompt optimization using LangMem

## Troubleshooting

### Application won't start

Check logs:
```bash
make logs
```

Rebuild from scratch:
```bash
make clean
make rebuild
```

### Health check failing

Check the health endpoint:
```bash
make health
```

Or manually:
```bash
curl http://localhost:8501/_stcore/health
```

### Port already in use

Change the port in `docker-compose.yml`:
```yaml
ports:
  - "8502:8501"  # Changed from 8501:8501
```

### Cache issues

Clear the vectorstore cache:
```bash
make clean-cache
```

### Permission issues

Ensure tmp directory has correct permissions:
```bash
chmod 755 tmp
```

## Production Deployment

For production deployment:

1. Remove development volume mount in `docker-compose.yml`:
   ```yaml
   # Comment out this line:
   # - .:/app
   ```

2. Build optimized images:
   ```bash
   docker-compose build --no-cache
   ```

3. Use environment variables instead of `.env` file:
   ```bash
   OPENAI_API_KEY=xxx docker-compose up -d
   ```

4. Set up reverse proxy (nginx, Traefik) for SSL termination

5. Enable resource limits in `docker-compose.yml`:
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '2'
         memory: 4G
       reservations:
         cpus: '1'
         memory: 2G
   ```

## Performance Optimization

### Multi-stage Build

The Dockerfile uses multi-stage builds to minimize image size:
- Builder stage: Installs dependencies
- Final stage: Copies only what's needed

### Cache Management

The application includes smart caching:
- Vectorstore cache expires after 7 days
- Cache size limit: 500MB
- Automatic cleanup on startup

### Resource Usage

Monitor container resources:
```bash
make stats
```

## Security Considerations

1. **API Keys**: Never commit `.env` file to git
2. **Permissions**: Cache files have restrictive permissions (0600)
3. **Network**: Containers run on isolated network
4. **Health Checks**: Built-in health monitoring

## Backup and Restore

### Backup Cache

```bash
make backup-cache
```

This creates a timestamped tarball of the vectorstore cache.

### Restore Cache

```bash
tar -xzf cache-backup-YYYYMMDD-HHMMSS.tar.gz
```

## CI/CD Integration

Example GitHub Actions workflow:

```yaml
name: Docker Build

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker image
        run: make build
      - name: Run tests
        run: make test
```

## Support

For issues and questions:
- Check logs: `make logs`
- Review health: `make health`
- Rebuild clean: `make clean && make rebuild`
