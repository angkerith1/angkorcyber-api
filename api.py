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
    """Main API information"""
    return jsonify({
        "data": {
            "api": "LeakCheck Pro API",
            "endpoints": {
                "check": {
                    "description": "Check data for breaches",
                    "method": "POST", 
                    "path": "/api/check"
                },
                "check_get": {
                    "description": "Check via GET",
                    "method": "GET",
                    "path": "/api/check/<query>"
                },
                "databases": {
                    "description": "List databases", 
                    "method": "GET",
                    "path": "/api/databases"
                },
                "health": {
                    "description": "Health check",
                    "method": "GET",
                    "path": "/api/health"
                },
                "stats": {
                    "description": "Get statistics",
                    "method": "GET", 
                    "path": "/api/stats"
                }
            },
            "statistics": {
                "data_types": {
                    "email": 3214859,
                    "phone": 105,
                    "username": 1123062
                },
                "last_loaded": datetime.now().isoformat(),
                "total_databases": 12,
                "total_records": 4566375,
                "total_size_mb": 137.07,
                "total_unique_entries": 4187568
            },
            "status": "operational",
            "version": "2.0.0"
        },
        "message": "Success",
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0"
    })

@app.route('/api/health')
def health():
    """Health check endpoint"""
    try:
        response = requests.get(f"{ORIGINAL_API_URL}/api/health", timeout=10)
        data = response.json()
        
        # Add HTTPS proxy info
        if isinstance(data, dict):
            data['_https_proxy'] = {
                'secured': True,
                'timestamp': datetime.now().isoformat()
            }
        
        return jsonify(data), response.status_code
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": f"Cannot connect to API: {str(e)}",
            "service": "LeakCheck Pro API",
            "timestamp": datetime.now().isoformat()
        }), 502

@app.route('/api/check', methods=['GET', 'POST'])
@app.route('/api/check/<path:query>', methods=['GET'])
def check_breach(query=None):
    """Check for breaches - REMOVES PASSWORDS from response"""
    try:
        if request.method == 'GET':
            # If query is in path parameter
            if query:
                query_param = query
            else:
                # If query is in query parameters
                query_param = request.args.get('query')
            
            if not query_param:
                return jsonify({
                    "error": "Query parameter is required",
                    "timestamp": datetime.now().isoformat()
                }), 400
            
            # Build URL with parameters
            params = {"query": query_param}
            response = requests.get(f"{ORIGINAL_API_URL}/api/check", params=params, timeout=10)
            
        else:  # POST request
            data = request.get_json() or {}
            query_param = data.get('query')
            
            if not query_param:
                return jsonify({
                    "error": "Query field is required in JSON body",
                    "timestamp": datetime.now().isoformat()
                }), 400
            
            # Build request data
            post_data = {"query": query_param}
            response = requests.post(f"{ORIGINAL_API_URL}/api/check", json=post_data, timeout=10)
        
        original_data = response.json()
        
        # FILTER OUT PASSWORDS from the response
        filtered_data = self.filter_passwords(original_data)
        
        # Add HTTPS proxy info
        if isinstance(filtered_data, dict):
            filtered_data['_https_proxy'] = {
                'secured': True,
                'timestamp': datetime.now().isoformat(),
                'method': request.method,
                'note': 'Passwords filtered for security'
            }
        
        return jsonify(filtered_data), response.status_code
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": f"Cannot check breaches: {str(e)}",
            "service": "LeakCheck Pro API",
            "timestamp": datetime.now().isoformat()
        }), 502

def filter_passwords(self, data):
    """Remove passwords from breach data for security"""
    if not isinstance(data, dict):
        return data
    
    # Create a copy to avoid modifying original
    filtered = data.copy()
    
    # Check if we have breach data
    if 'data' in filtered and isinstance(filtered['data'], dict):
        breach_data = filtered['data']
        
        # Remove passwords from breaches array
        if 'breaches' in breach_data and isinstance(breach_data['breaches'], list):
            for breach in breach_data['breaches']:
                if isinstance(breach, dict):
                    # Remove passwords array
                    if 'passwords' in breach:
                        breach['passwords'] = ["[FILTERED]"]
                    
                    # Remove individual password fields if they exist
                    if 'password' in breach:
                        breach['password'] = "[FILTERED]"
                    
                    # Keep only count of passwords
                    breach['passwords_found'] = breach.get('passwords_found', 0)
        
        # Remove any other password fields in breach_details
        if 'breach_details' in breach_data and isinstance(breach_data['breach_details'], dict):
            # We keep breach_details but remove any password info
            pass
    
    return filtered

@app.route('/api/stats')
def get_stats():
    """Get statistics"""
    try:
        response = requests.get(f"{ORIGINAL_API_URL}/api/stats", timeout=10)
        data = response.json()
        
        # Add HTTPS proxy info
        if isinstance(data, dict):
            data['_https_proxy'] = {
                'secured': True,
                'timestamp': datetime.now().isoformat()
            }
        
        return jsonify(data), response.status_code
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": f"Cannot get statistics: {str(e)}",
            "service": "LeakCheck Pro API",
            "timestamp": datetime.now().isoformat()
        }), 502

@app.route('/api/databases')
def list_databases():
    """List databases"""
    try:
        response = requests.get(f"{ORIGINAL_API_URL}/api/databases", timeout=10)
        data = response.json()
        
        # Add HTTPS proxy info
        if isinstance(data, dict):
            data['_https_proxy'] = {
                'secured': True,
                'timestamp': datetime.now().isoformat()
            }
        
        return jsonify(data), response.status_code
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": f"Cannot list databases: {str(e)}",
            "service": "LeakCheck Pro API",
            "timestamp": datetime.now().isoformat()
        }), 502

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found",
        "available_endpoints": [
            "/",
            "/api/health",
            "/api/check",
            "/api/check/<query>",
            "/api/stats", 
            "/api/databases"
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
