from flask import Flask, request, jsonify
import requests
import json
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuration
ANGKOR_BASE_URL = "http://5.175.234.87:5000"

@app.route('/')
def home():
    """Main API information"""
    return jsonify({
        "data": {
            "api": "AngkorCyber Security API - HTTPS Gateway",
            "endpoints": {
                "/": "API Information",
                "/health": "Health Check",
                "/services": "List Services",
                "/angkor/health": "Angkor API Health",
                "/angkor/check": "Check Breaches",
                "/angkor/databases": "List Databases",
                "/json/users": "JSONPlaceholder API"
            },
            "status": "operational",
            "supported_formats": [
                "email:password", "email|password", "email;password", "email password",
                "phone:password", "phone|password", "phone password", "plain email",
                "plain phone", "username:password"
            ],
            "version": "3.0.0"
        },
        "message": "Welcome to AngkorCyber Security HTTPS API",
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "version": "3.0.0"
    })

@app.route('/health')
def health():
    """Health check"""
    return jsonify({
        "status": "healthy",
        "service": "AngkorCyber HTTPS Gateway",
        "timestamp": datetime.now().isoformat(),
        "version": "3.0.0"
    })

@app.route('/services')
def services():
    """List all services"""
    return jsonify({
        "services": {
            "angkor": {
                "base_url": ANGKOR_BASE_URL,
                "status": "available",
                "endpoints": ["/health", "/databases", "/check", "/stats", "/search"]
            },
            "jsonplaceholder": {
                "base_url": "https://jsonplaceholder.typicode.com",
                "status": "available",
                "endpoints": ["/users", "/posts", "/comments"]
            }
        },
        "timestamp": datetime.now().isoformat()
    })

@app.route('/angkor/health')
def angkor_health():
    """Proxy to Angkor API health"""
    try:
        response = requests.get(f"{ANGKOR_BASE_URL}/api/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            data['_proxy'] = {
                'secured': True,
                'timestamp': datetime.now().isoformat()
            }
            return jsonify(data)
        else:
            return jsonify({"error": "Angkor API unavailable", "status_code": response.status_code}), 502
    except Exception as e:
        return jsonify({"error": f"Cannot connect to Angkor API: {str(e)}"}), 502

@app.route('/angkor/check')
def angkor_check():
    """Proxy to Angkor check endpoint"""
    query = request.args.get('query', 'test@example.com')
    try:
        response = requests.get(f"{ANGKOR_BASE_URL}/api/check", params={"query": query}, timeout=10)
        if response.status_code == 200:
            data = response.json()
            data['_proxy'] = {
                'secured': True,
                'timestamp': datetime.now().isoformat()
            }
            return jsonify(data)
        else:
            return jsonify({"error": "Check service unavailable", "status_code": response.status_code}), 502
    except Exception as e:
        return jsonify({"error": f"Cannot connect to check service: {str(e)}"}), 502

@app.route('/angkor/databases')
def angkor_databases():
    """Proxy to Angkor databases endpoint"""
    try:
        response = requests.get(f"{ANGKOR_BASE_URL}/api/databases", timeout=10)
        if response.status_code == 200:
            data = response.json()
            data['_proxy'] = {
                'secured': True,
                'timestamp': datetime.now().isoformat()
            }
            return jsonify(data)
        else:
            return jsonify({"error": "Databases service unavailable", "status_code": response.status_code}), 502
    except Exception as e:
        return jsonify({"error": f"Cannot connect to databases service: {str(e)}"}), 502

@app.route('/angkor/stats')
def angkor_stats():
    """Proxy to Angkor stats endpoint"""
    try:
        response = requests.get(f"{ANGKOR_BASE_URL}/api/stats", timeout=10)
        if response.status_code == 200:
            data = response.json()
            data['_proxy'] = {
                'secured': True,
                'timestamp': datetime.now().isoformat()
            }
            return jsonify(data)
        else:
            return jsonify({"error": "Stats service unavailable", "status_code": response.status_code}), 502
    except Exception as e:
        return jsonify({"error": f"Cannot connect to stats service: {str(e)}"}), 502

@app.route('/json/users')
def json_users():
    """Proxy to JSONPlaceholder"""
    try:
        response = requests.get("https://jsonplaceholder.typicode.com/users", timeout=10)
        if response.status_code == 200:
            data = response.json()
            data['_proxy'] = {
                'service': 'JSONPlaceholder',
                'secured': True,
                'timestamp': datetime.now().isoformat()
            }
            return jsonify(data)
        else:
            return jsonify({"error": "JSON service unavailable", "status_code": response.status_code}), 502
    except Exception as e:
        return jsonify({"error": f"Cannot connect to JSON service: {str(e)}"}), 502

@app.route('/json/posts')
def json_posts():
    """Proxy to JSONPlaceholder posts"""
    try:
        response = requests.get("https://jsonplaceholder.typicode.com/posts", timeout=10)
        if response.status_code == 200:
            data = response.json()
            data['_proxy'] = {
                'service': 'JSONPlaceholder',
                'secured': True,
                'timestamp': datetime.now().isoformat()
            }
            return jsonify(data)
        else:
            return jsonify({"error": "JSON service unavailable", "status_code": response.status_code}), 502
    except Exception as e:
        return jsonify({"error": f"Cannot connect to JSON service: {str(e)}"}), 502

@app.route('/proxy')
def universal_proxy():
    """Universal proxy endpoint"""
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter required"}), 400
    
    try:
        response = requests.get(url, timeout=10)
        if response.headers.get('content-type', '').startswith('application/json'):
            data = response.json()
        else:
            data = response.text
            
        return jsonify({
            "status": response.status_code,
            "data": data,
            "proxy_info": {
                "original_url": url,
                "timestamp": datetime.now().isoformat(),
                "secured": True
            }
        })
    except Exception as e:
        return jsonify({"error": f"Proxy error: {str(e)}"}), 502

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
