# Docker Setup Guide for Skills Integration MCP Project

## Quick Start - Development

### Prerequisites
- Docker and Docker Compose installed
- Port 8000 available on your machine

### Running Locally

**Development mode (with hot-reload):**
```bash
docker-compose up app-dev
```

The application will be available at `http://localhost:8000`
- API docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

**Production mode:**
```bash
docker-compose up app-prod
```

The application will be available at `http://localhost:8001`

### Building Images Separately

**Development image:**
```bash
docker build -f Dockerfile.dev -t skills-app:dev .
docker run -p 8000:8000 -v $(pwd):/app skills-app:dev
```

**Production image:**
```bash
docker build -f Dockerfile -t skills-app:latest .
docker run -p 8000:8000 skills-app:latest
```

## Production Deployment

### Using Nginx Reverse Proxy

```bash
docker-compose --profile prod up nginx app-prod
```

This will:
- Run the FastAPI app on port 8001 (internal)
- Expose Nginx on ports 80 and 443 (external)
- Forward all traffic to the FastAPI backend

### SSL/TLS Configuration

1. Place your SSL certificate at `./ssl/cert.pem`
2. Place your private key at `./ssl/key.pem`
3. Uncomment the HTTPS section in `nginx.conf`
4. Update `server_name` to your domain

## Environment Variables

Create a `.env` file if needed (template):
```
PYTHONUNBUFFERED=1
```

## Docker Commands

### View logs
```bash
docker-compose logs -f app-dev
docker-compose logs -f app-prod
```

### Stop services
```bash
docker-compose down
```

### Remove all containers and volumes
```bash
docker-compose down -v
```

### Rebuild images
```bash
docker-compose build --no-cache
```

## Container Structure

- **app-dev**: Development container with hot-reload
- **app-prod**: Production-optimized multi-stage build
- **nginx**: Optional Nginx reverse proxy for production

## Troubleshooting

### Port already in use
Change the port mapping in `docker-compose.yml`:
```yaml
ports:
  - "9000:8000"  # Access on http://localhost:9000
```

### Permission denied on volume mounts (Linux)
```bash
sudo chown -R $(id -u):$(id -g) .
```

### App not responding
Check logs:
```bash
docker-compose logs app-dev
docker-compose logs app-prod
```

## Performance Tips

- Use `.dockerignore` to exclude unnecessary files
- Run `docker image prune` to clean up unused images
- Use volume mounts only in development, copy files in production
- Consider using BuildKit for faster builds: `DOCKER_BUILDKIT=1 docker build ...`

## CI/CD Integration

These Docker configurations are ready for:
- GitHub Actions
- GitLab CI
- Jenkins
- Any standard CI/CD platform

Example GitHub Actions workflow available upon request.
