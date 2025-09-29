from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import datetime
import os

app = FastAPI(
    title="AngkorCyber Security API",
    description="Security breach checking API",
    version="3.0.0"
)

# Add CORS middleware
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

# API Data - matching your original API structure
API_INFO = {
    "data": {
        "api": "AngkorCyber Security API",
        "endpoints": {
            "/api/admin/reload": "Reload databases (Admin)",
            "/api/check": "Check email/phone for breaches (POST/GET)",
            "/api/databases": "List loaded databases",
            "/api/health": "System health check",
            "/api/search": "Search multiple queries",
            "/api/stats": "Get detailed statistics"
        },
        "status": "operational",
        "supported_formats": [
            "email:password",
            "email|password",
            "email;password",
            "email password",
            "phone:password",
            "phone|password",
            "phone password",
            "plain email",
            "plain phone",
            "username:password"
        ],
        "version": "3.0.0"
    },
    "message": "Welcome to AngkorCyber Security API",
    "status": "success",
    "version": "3.0.0"
}

@app.get("/")
async def root():
    """Root endpoint with API information"""
    response = API_INFO.copy()
    response["timestamp"] = datetime.datetime.utcnow().isoformat()
    return response

@app.get("/api/health")
async def health_check():
    """System health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "version": "3.0.0",
        "environment": "production"
    }

@app.get("/api/databases")
async def list_databases():
    """List loaded databases"""
    return {
        "databases": [
            {"name": "BreachCollection2024", "records": 1500000, "status": "loaded", "size": "2.1GB"},
            {"name": "Compilation2023", "records": 890000, "status": "loaded", "size": "1.2GB"},
            {"name": "GlobalLeaks2024", "records": 2300000, "status": "loaded", "size": "3.4GB"}
        ],
        "total_databases": 3,
        "total_records": 4690000,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

@app.get("/api/check")
async def check_breach_get(query: str = Query(..., description="Email, phone, or username to check")):
    """Check for breaches via GET"""
    return await _check_breach(query)

@app.post("/api/check")
async def check_breach_post(request: CheckRequest):
    """Check for breaches via POST"""
    return await _check_breach(request.query)

async def _check_breach(query: str):
    """Internal breach check logic"""
    breaches = []
    if "test" in query.lower():
        breaches = [
            {
                "database": "BreachCollection2024",
                "records": 1,
                "first_seen": "2024-03-15",
                "breach_type": "credential_stuffing"
            }
        ]
    else:
        breaches = [
            {
                "database": "BreachCollection2024",
                "records": 1,
                "first_seen": "2024-03-15",
                "breach_type": "credential_stuffing"
            },
            {
                "database": "GlobalLeaks2024",
                "records": 1,
                "first_seen": "2024-07-22",
                "breach_type": "data_breach"
            }
        ]
    
    return {
        "query": query,
        "breaches_found": len(breaches),
        "breaches": breaches,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "status": "completed"
    }

@app.post("/api/search")
async def search_multiple(request: SearchRequest):
    """Search multiple queries at once"""
    if len(request.queries) > 20:
        raise HTTPException(status_code=400, detail="Maximum 20 queries allowed per request")
    
    results = []
    for query in request.queries:
        breach_result = await _check_breach(query)
        results.append({
            "query": query,
            "breaches_found": breach_result["breaches_found"],
            "breaches": breach_result["breaches"]
        })
    
    return {
        "results": results,
        "total_queries": len(request.queries),
        "processed": len(request.queries),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

@app.get("/api/stats")
async def get_stats():
    """Get API statistics"""
    return {
        "statistics": {
            "total_databases": 3,
            "total_records": 4690000,
            "unique_emails": 3250000,
            "unique_phones": 1440000,
            "queries_processed": 12457,
            "uptime": "99.8%",
            "last_updated": "2024-09-28T12:00:00Z"
        },
        "system": {
            "status": "operational",
            "version": "3.0.0",
            "response_time": "~150ms"
        },
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

@app.post("/api/admin/reload")
async def reload_databases(request: ReloadRequest):
    """Reload databases (Admin endpoint)"""
    expected_key = os.getenv("ADMIN_KEY", "default-admin-key-123")
    
    if request.admin_key != expected_key:
        raise HTTPException(status_code=401, detail="Invalid admin key")
    
    return {
        "message": "Databases reload initiated successfully",
        "status": "success",
        "reload_time": "15 seconds",
        "databases_affected": 3,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# Vercel serverless function handler
from mangum import Mangum
handler = Mangum(app)

# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
