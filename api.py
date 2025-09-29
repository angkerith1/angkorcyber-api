from flask import Flask, request, jsonify
import requests
import json
from datetime import datetime
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Configuration
ORIGINAL_API_URL = "http://5.175.234.87:5000"

@app.route('/')
def home():
    """Main API information - EXACT copy of original"""
    return jsonify({
        "data": {
            "api": "AngkorCyber Security API",
            "endpoints": {
                "/api/admin/reload": "Reload databases (Admin)",
                "/api/check": "Check email/phone for breaches (POST/GET)",
                "/api/databases": "List loaded databases",
                "/api/health": "System health check",
                "/api/search": "Search multiple queries",
                "/api/stats": "Get detailed statistics",
                "/api/debug": "Debug information"
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
        "timestamp": datetime.now().isoformat(),
        "version": "3.0.0"
    })

@app.route('/api/health')
def health():
    """Health check endpoint - Proxy to original"""
    try:
        response = requests.get(f"{ORIGINAL_API_URL}/api/health", timeout=10)
        data = response.json()
        
        # Add HTTPS proxy info
        if isinstance(data, dict):
            data['_https_proxy'] = {
                'original_api': ORIGINAL_API_URL,
                'secured': True,
                'timestamp': datetime.now().isoformat()
            }
        
        return jsonify(data), response.status_code
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": f"Cannot connect to API: {str(e)}",
            "service": "AngkorCyber Security API",
            "timestamp": datetime.now().isoformat()
        }), 502

@app.route('/api/check', methods=['GET', 'POST'])
def check_breach():
    """Check for breaches - Supports GET and POST"""
    try:
        if request.method == 'GET':
            # GET request with query parameters
            query = request.args.get('query')
            query_type = request.args.get('type', 'auto')
            
            if not query:
                return jsonify({
                    "error": "Query parameter is required",
                    "timestamp": datetime.now().isoformat()
                }), 400
            
            # Build URL with parameters
            params = {"query": query}
            if query_type != 'auto':
                params["type"] = query_type
                
            response = requests.get(f"{ORIGINAL_API_URL}/api/check", params=params, timeout=10)
            
        else:  # POST request
            data = request.get_json() or {}
            query = data.get('query')
            data_type = data.get('data_type')
            
            if not query:
                return jsonify({
                    "error": "Query field is required in JSON body",
                    "timestamp": datetime.now().isoformat()
                }), 400
            
            # Build request data
            post_data = {"query": query}
            if data_type:
                post_data["data_type"] = data_type
                
            response = requests.post(f"{ORIGINAL_API_URL}/api/check", json=post_data, timeout=10)
        
        data = response.json()
        
        # Add HTTPS proxy info
        if isinstance(data, dict):
            data['_https_proxy'] = {
                'original_api': ORIGINAL_API_URL,
                'secured': True,
                'timestamp': datetime.now().isoformat(),
                'method': request.method
            }
        
        return jsonify(data), response.status_code
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": f"Cannot check breaches: {str(e)}",
            "service": "AngkorCyber Security API",
            "timestamp": datetime.now().isoformat()
        }), 502

@app.route('/api/stats')
def get_stats():
    """Get statistics - Proxy to original"""
    try:
        response = requests.get(f"{ORIGINAL_API_URL}/api/stats", timeout=10)
        data = response.json()
        
        # Add HTTPS proxy info
        if isinstance(data, dict):
            data['_https_proxy'] = {
                'original_api': ORIGINAL_API_URL,
                'secured': True,
                'timestamp': datetime.now().isoformat()
            }
        
        return jsonify(data), response.status_code
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": f"Cannot get statistics: {str(e)}",
            "service": "AngkorCyber Security API",
            "timestamp": datetime.now().isoformat()
        }), 502

@app.route('/api/databases')
def list_databases():
    """List databases - Proxy to original"""
    try:
        response = requests.get(f"{ORIGINAL_API_URL}/api/databases", timeout=10)
        data = response.json()
        
        # Add HTTPS proxy info
        if isinstance(data, dict):
            data['_https_proxy'] = {
                'original_api': ORIGINAL_API_URL,
                'secured': True,
                'timestamp': datetime.now().isoformat()
            }
        
        return jsonify(data), response.status_code
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": f"Cannot list databases: {str(e)}",
            "service": "AngkorCyber Security API",
            "timestamp": datetime.now().isoformat()
        }), 502

@app.route('/api/debug')
def debug_info():
    """Debug information - Proxy to original"""
    try:
        response = requests.get(f"{ORIGINAL_API_URL}/api/debug", timeout=10)
        data = response.json()
        
        # Add HTTPS proxy info
        if isinstance(data, dict):
            data['_https_proxy'] = {
                'original_api': ORIGINAL_API_URL,
                'secured': True,
                'timestamp': datetime.now().isoformat()
            }
        
        return jsonify(data), response.status_code
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": f"Cannot get debug info: {str(e)}",
            "service": "AngkorCyber Security API",
            "timestamp": datetime.now().isoformat()
        }), 502

@app.route('/api/search', methods=['POST'])
def search_multiple():
    """Search multiple queries - Proxy to original"""
    try:
        data = request.get_json()
        
        if not data or 'queries' not in data:
            return jsonify({
                "error": "Queries array is required in JSON body",
                "timestamp": datetime.now().isoformat()
            }), 400
        
        response = requests.post(f"{ORIGINAL_API_URL}/api/search", json=data, timeout=15)
        result = response.json()
        
        # Add HTTPS proxy info
        if isinstance(result, dict):
            result['_https_proxy'] = {
                'original_api': ORIGINAL_API_URL,
                'secured': True,
                'timestamp': datetime.now().isoformat(),
                'queries_processed': len(data.get('queries', []))
            }
        
        return jsonify(result), response.status_code
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": f"Cannot perform search: {str(e)}",
            "service": "AngkorCyber Security API",
            "timestamp": datetime.now().isoformat()
        }), 502

@app.route('/api/admin/reload', methods=['POST'])
def reload_databases():
    """Admin reload databases - Proxy to original"""
    try:
        # Get admin key from headers or query params
        admin_key = None
        
        # Check headers first
        admin_key_header = request.headers.get('X-Admin-Key')
        if admin_key_header:
            admin_key = admin_key_header
        
        # Check query parameters
        if not admin_key:
            admin_key = request.args.get('admin_key')
        
        if not admin_key:
            return jsonify({
                "error": "Admin key required. Use X-Admin-Key header or admin_key query parameter",
                "timestamp": datetime.now().isoformat()
            }), 401
        
        # Prepare request to original API
        headers = {'X-Admin-Key': admin_key}
        response = requests.post(f"{ORIGINAL_API_URL}/api/admin/reload", headers=headers, timeout=30)
        result = response.json()
        
        # Add HTTPS proxy info
        if isinstance(result, dict):
            result['_https_proxy'] = {
                'original_api': ORIGINAL_API_URL,
                'secured': True,
                'timestamp': datetime.now().isoformat(),
                'admin_action': 'database_reload'
            }
        
        return jsonify(result), response.status_code
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": f"Cannot reload databases: {str(e)}",
            "service": "AngkorCyber Security API",
            "timestamp": datetime.now().isoformat()
        }), 502

# Additional endpoint to show proxy info
@app.route('/api/proxy/info')
def proxy_info():
    """Show proxy information"""
    return jsonify({
        "proxy_service": "AngkorCyber HTTPS Proxy",
        "original_api": ORIGINAL_API_URL,
        "secured": True,
        "endpoints_proxied": [
            "/api/check (GET/POST)",
            "/api/stats (GET)", 
            "/api/databases (GET)",
            "/api/health (GET)",
            "/api/debug (GET)",
            "/api/search (POST)",
            "/api/admin/reload (POST)"
        ],
        "timestamp": datetime.now().isoformat(),
        "version": "3.0.0"
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found",
        "available_endpoints": [
            "/",
            "/api/health",
            "/api/check",
            "/api/stats", 
            "/api/databases",
            "/api/debug",
            "/api/search",
            "/api/admin/reload",
            "/api/proxy/info"
        ],
        "timestamp": datetime.now().isoformat()
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal server error",
        "message": "Please try again later",
        "timestamp": datetime.now().isoformat()
    }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
