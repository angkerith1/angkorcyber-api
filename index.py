from flask import Flask, jsonify, request
import datetime
import os

app = Flask(__name__)

# Mock data for the API
API_DATA = {
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

@app.route('/')
def home():
    """Root endpoint with API information"""
    response = API_DATA.copy()
    response['timestamp'] = datetime.datetime.utcnow().isoformat()
    return jsonify(response)

@app.route('/api/health')
def health_check():
    """System health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "version": "3.0.0"
    })

@app.route('/api/databases')
def list_databases():
    """List loaded databases"""
    return jsonify({
        "databases": [
            {"name": "BreachCollection2024", "records": 1500000, "status": "loaded"},
            {"name": "Compilation2023", "records": 890000, "status": "loaded"},
            {"name": "GlobalLeaks2024", "records": 2300000, "status": "loaded"}
        ],
        "total_databases": 3,
        "total_records": 4690000,
        "timestamp": datetime.datetime.utcnow().isoformat()
    })

@app.route('/api/check', methods=['GET', 'POST'])
def check_breach():
    """Check email/phone for breaches"""
    if request.method == 'GET':
        query = request.args.get('query')
    else:
        data = request.get_json()
        query = data.get('query') if data else None
    
    if not query:
        return jsonify({
            "error": "Query parameter is required",
            "status": "error"
        }), 400
    
    # Mock breach check response
    return jsonify({
        "query": query,
        "breaches_found": 2,
        "breaches": [
            {
                "database": "BreachCollection2024",
                "records": 1,
                "first_seen": "2024-03-15"
            },
            {
                "database": "GlobalLeaks2024",
                "records": 1,
                "first_seen": "2024-07-22"
            }
        ],
        "timestamp": datetime.datetime.utcnow().isoformat()
    })

@app.route('/api/search', methods=['POST'])
def search_multiple():
    """Search multiple queries"""
    data = request.get_json()
    
    if not data or 'queries' not in data:
        return jsonify({
            "error": "Queries array is required",
            "status": "error"
        }), 400
    
    queries = data['queries']
    
    if not isinstance(queries, list):
        return jsonify({
            "error": "Queries must be an array",
            "status": "error"
        }), 400
    
    # Mock search results
    results = []
    for query in queries[:10]:  # Limit to 10 queries
        results.append({
            "query": query,
            "breaches_found": 1 if "test" not in query.lower() else 0,
            "databases": ["BreachCollection2024"] if "test" not in query.lower() else []
        })
    
    return jsonify({
        "results": results,
        "total_queries": len(queries),
        "processed": min(len(queries), 10),
        "timestamp": datetime.datetime.utcnow().isoformat()
    })

@app.route('/api/stats')
def get_stats():
    """Get detailed statistics"""
    return jsonify({
        "statistics": {
            "total_databases": 3,
            "total_records": 4690000,
            "unique_emails": 3250000,
            "unique_phones": 1440000,
            "queries_processed": 12457,
            "uptime": "99.8%"
        },
        "system": {
            "status": "operational",
            "last_update": "2024-09-28T12:00:00Z",
            "version": "3.0.0"
        },
        "timestamp": datetime.datetime.utcnow().isoformat()
    })

@app.route('/api/admin/reload', methods=['POST'])
def reload_databases():
    """Reload databases (Admin) - Mock implementation"""
    # In a real implementation, you'd want proper authentication here
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({
            "error": "Authentication required",
            "status": "error"
        }), 401
    
    # Mock reload process
    return jsonify({
        "message": "Databases reload initiated",
        "status": "success",
        "reload_time": "15 seconds",
        "timestamp": datetime.datetime.utcnow().isoformat()
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found",
        "status": "error",
        "timestamp": datetime.datetime.utcnow().isoformat()
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal server error",
        "status": "error",
        "timestamp": datetime.datetime.utcnow().isoformat()
    }), 500

# Vercel requires this to be named 'app'
if __name__ == '__main__':
    app.run(debug=True)
