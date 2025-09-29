# AngkorCyber HTTPS API Gateway

Unified HTTPS proxy for multiple HTTP APIs with enhanced security and CORS support.

## 🚀 Features

- **HTTPS Encryption** for all HTTP APIs
- **Multiple API Support** in one endpoint
- **CORS Enabled** for web applications
- **Universal Proxy** for any HTTP API
- **Auto Documentation** with Swagger UI

## 📡 Available Endpoints

### Main API
- `GET /` - API information
- `GET /api/health` - Health check
- `GET /api/databases` - List databases
- `GET/POST /api/check` - Check breaches
- `POST /api/search` - Multiple search
- `GET /api/stats` - Statistics
- `POST /api/admin/reload` - Admin reload

### Proxy Services
- `GET /services` - List all services
- `POST /api/proxy` - Universal proxy

### API Documentation
- `GET /docs` - Swagger UI
- `GET /redoc` - ReDoc UI

## 🔧 Configuration

Edit `api/index.py` to add your APIs:

```python
OTHER_APIS = {
    "my_custom_api": "http://your-api.com",
    "weather_api": "http://weather-api.com/data",
}
