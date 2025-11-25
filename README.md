# Arjent Jr Enterprise - Python Service

## 🚀 Coolify Deployment

This Python FastAPI service is ready for deployment on Coolify.

### Quick Deploy to Coolify

1. **Push to Git Repository**: Ensure your code is in a Git repository
2. **Connect to Coolify**: 
   - Add your Git repository to Coolify
   - Select "Docker" as deployment type
   - Coolify will auto-detect the Dockerfile

3. **Configuration**:
   - **Port**: 8000 (automatically exposed)
   - **Health Check**: `/health` endpoint
   - **Environment**: Production ready with non-root user

### Environment Variables (Optional)
```env
PYTHONPATH=/app
PORT=8000
```

### Local Testing

Test the Docker build locally:
```bash
# Build the image
docker build -t arjent-jr-python .

# Run the container
docker run -p 8000:8000 arjent-jr-python

# Or use docker-compose
docker-compose up
```

### API Endpoints

- **Health Check**: `GET /health`
- **Inference**: `POST /infer`
- **API Documentation**: `/docs` (Swagger UI)

### Service Features

- ✅ FastAPI with automatic API documentation
- ✅ CCP Continuity Control Panel
- ✅ Canon Engine for content processing
- ✅ WayThread Engine for conversation flow
- ✅ VaultDrive Engine for data management
- ✅ Ledger Engine for transaction tracking
- ✅ Identity management system
- ✅ Health monitoring

### Production Optimizations

- Multi-stage Docker build for smaller image size
- Non-root user for security
- Health checks for monitoring
- Proper error handling and logging
- Environment variable configuration
- Docker layer caching optimization

### Deployment Steps in Coolify

1. Create new application in Coolify
2. Connect your Git repository
3. Set deployment type to "Docker"
4. Configure domain (optional)
5. Deploy!

The service will be available at: `https://your-domain.com` or the provided Coolify URL.