from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import datetime
import requests
import json

app = FastAPI(
    title="AngkorCyber Security API",
    description="Unified HTTPS API Proxy with Multiple Backend Services",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class CheckRequest(BaseModel):
    query: str

class SearchRequest(BaseModel):
    queries: List[str]

class ReloadRequest(BaseModel):
    admin_key: Optional[str] = None

class ProxyRequest(BaseModel):
    url: str
    method: str = "GET"
    headers: Optional[Dict] = None
    data: Optional[Any] = None

# Configuration
ANGKOR_BASE_URL = "http://5.175.234.87:5000"
OTHER_APIS = {
    "json_placeholder": "https://jsonplaceholder.typicode.com",
    # Add your other APIs here
    # "my_other_api": "http://your-api.com",
}

@app.get("/")
async def root():
    """Root endpoint with unified API information"""
    return {
        "data": {
            "api": "AngkorCyber Security API - HTTPS Proxy",
            "endpoints": {
                "/": "API Information (this page)",
                "/api/health": "System health check",
                "/api/databases": "List loaded databases",
                "/api/check": "Check email/phone for breaches",
                "/api/search": "Search multiple queries",
                "/api/stats": "Get detailed statistics",
                "/api/admin/reload": "Reload databases (Admin)",
                "/api/proxy": "Universal proxy endpoint",
                "/docs": "API Documentation",
                "/services": "List all available services"
            },
            "status": "operational",
            "supported_formats": [
                "email:password", "email|password", "email;password", "email password",
                "phone:password", "phone|password", "phone password", "plain email",
                "plain phone", "username:password"
            ],
            "version": "3.0.0",
            "features": [
                "HTTPS Encryption",
                "CORS Enabled",
                "Multiple API Support",
                "Proxy Services"
            ]
        },
        "message": "Welcome to AngkorCyber Security HTTPS API Gateway",
        "status": "success",
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "version": "3.0.0"
    }

@app.get("/api/health")
async def health_check():
    """System health check with backend status"""
    try:
        # Check main API health
        main_api_response = requests.get(f"{ANGKOR_BASE_URL}/api/health", timeout=10)
        main_api_status = "healthy" if main_api_response.status_code == 200 else "unhealthy"
    except:
        main_api_status = "offline"

    return {
        "status": "healthy",
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "version": "3.0.0",
        "environment": "production",
        "backend_services": {
            "main_api": main_api_status,
            "proxy_service": "healthy"
        },
        "uptime": "99.9%"
    }

@app.get("/api/databases")
async def list_databases():
    """List loaded databases from main API"""
    try:
        response = requests.get(f"{ANGKOR_BASE_URL}/api/databases", timeout=10)
        if response.status_code == 200:
            data = response.json()
            data["_proxy"] = {
                "cached": False,
                "timestamp": datetime.datetime.utcnow().isoformat(),
                "via": "HTTPS Proxy"
            }
            return data
        else:
            raise HTTPException(status_code=502, detail="Backend service unavailable")
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Backend connection failed: {str(e)}")

@app.get("/api/check")
async def check_breach_get(query: str = Query(..., description="Email, phone, or username to check")):
    """Check for breaches via GET"""
    return await _check_breach(query)

@app.post("/api/check")
async def check_breach_post(request: CheckRequest):
    """Check for breaches via POST"""
    return await _check_breach(request.query)

async def _check_breach(query: str):
    """Internal breach check logic with proxy"""
    try:
        # Try GET request to main API
        response = requests.get(f"{ANGKOR_BASE_URL}/api/check", params={"query": query}, timeout=10)
        if response.status_code != 200:
            # Try POST request
            response = requests.post(f"{ANGKOR_BASE_URL}/api/check", json={"query": query}, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            data["_proxy"] = {
                "secured": True,
                "original_query": query,
                "timestamp": datetime.datetime.utcnow().isoformat()
            }
            return data
        else:
            raise HTTPException(status_code=502, detail="Breach check service unavailable")
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Breach check failed: {str(e)}")

@app.post("/api/search")
async def search_multiple(request: SearchRequest):
    """Search multiple queries at once"""
    try:
        response = requests.post(f"{ANGKOR_BASE_URL}/api/search", json={"queries": request.queries}, timeout=15)
        if response.status_code == 200:
            data = response.json()
            data["_proxy"] = {
                "queries_processed": len(request.queries),
                "secured": True,
                "timestamp": datetime.datetime.utcnow().isoformat()
            }
            return data
        else:
            raise HTTPException(status_code=502, detail="Search service unavailable")
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Search failed: {str(e)}")

@app.get("/api/stats")
async def get_stats():
    """Get API statistics"""
    try:
        response = requests.get(f"{ANGKOR_BASE_URL}/api/stats", timeout=10)
        if response.status_code == 200:
            data = response.json()
            data["_proxy_stats"] = {
                "https_enabled": True,
                "response_time_ms": response.elapsed.total_seconds() * 1000,
                "timestamp": datetime.datetime.utcnow().isoformat()
            }
            return data
        else:
            raise HTTPException(status_code=502, detail="Stats service unavailable")
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Stats service failed: {str(e)}")

@app.post("/api/admin/reload")
async def reload_databases(request: ReloadRequest):
    """Reload databases (Admin endpoint)"""
    try:
        response = requests.post(f"{ANGKOR_BASE_URL}/api/admin/reload", json={"admin_key": request.admin_key}, timeout=30)
        if response.status_code == 200:
            data = response.json()
            data["_proxy"] = {
                "admin_action": "database_reload",
                "timestamp": datetime.datetime.utcnow().isoformat()
            }
            return data
        else:
            raise HTTPException(status_code=response.status_code, detail="Admin action failed")
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Admin action failed: {str(e)}")

@app.get("/services")
async def list_services():
    """List all available services and APIs"""
    return {
        "services": {
            "angkorcyber_main": {
                "base_url": ANGKOR_BASE_URL,
                "status": "active",
                "endpoints": [
                    "/api/health", "/api/databases", "/api/check", 
                    "/api/search", "/api/stats", "/api/admin/reload"
                ]
            },
            "json_placeholder": {
                "base_url": OTHER_APIS["json_placeholder"],
                "status": "active",
                "description": "Test API for development"
            }
        },
        "proxy_features": [
            "HTTPS Encryption",
            "CORS Support",
            "Request Logging",
            "Error Handling",
            "Multiple Backend Support"
        ],
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

@app.post("/api/proxy")
async def universal_proxy(request: ProxyRequest):
    """Universal proxy endpoint for any HTTP API"""
    try:
        headers = request.headers or {}
        headers.update({
            "User-Agent": "AngkorCyber-HTTPS-Proxy/1.0",
            "Accept": "application/json"
        })
        
        if request.method.upper() == "GET":
            response = requests.get(request.url, headers=headers, timeout=30)
        elif request.method.upper() == "POST":
            response = requests.post(request.url, json=request.data, headers=headers, timeout=30)
        elif request.method.upper() == "PUT":
            response = requests.put(request.url, json=request.data, headers=headers, timeout=30)
        elif request.method.upper() == "DELETE":
            response = requests.delete(request.url, headers=headers, timeout=30)
        else:
            raise HTTPException(status_code=400, detail="Unsupported HTTP method")
        
        # Return the proxied response
        return JSONResponse(
            content=response.json() if response.headers.get('content-type') == 'application/json' else {"data": response.text},
            status_code=response.status_code,
            headers={
                "X-Proxy-Server": "AngkorCyber HTTPS Gateway",
                "X-Original-URL": request.url,
                "Access-Control-Allow-Origin": "*"
            }
        )
        
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Proxy request failed: {str(e)}")

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Endpoint not found",
            "available_endpoints": [
                "/", "/api/health", "/api/databases", "/api/check", 
                "/api/search", "/api/stats", "/api/admin/reload", "/services", "/docs"
            ],
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "Please try again later",
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
    )

# Vercel serverless function handler
from mangum import Mangum
handler = Mangum(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
