from flask import Flask, request, jsonify
import requests
import json
from datetime import datetime
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Configuration
CAR_API_URL = "http://5.175.234.87:5000"  # Your car parking API

@app.route('/')
def home():
    """Main API information"""
    return jsonify({
        "data": {
            "api": "RithStore-Free Car Parking API",
            "service": "Free Car Parking Multiplayer Accounts",
            "endpoints": {
                "car_account": {
                    "description": "Get free car parking account",
                    "method": "GET",
                    "path": "/api/account"
                },
                "car_stats": {
                    "description": "Get car parking checker statistics",
                    "method": "GET",
                    "path": "/api/stats"
                },
                "car_queue": {
                    "description": "Check car accounts queue",
                    "method": "GET",
                    "path": "/api/queue"
                },
                "health": {
                    "description": "Health check",
                    "method": "GET",
                    "path": "/api/health"
                }
            },
            "status": "operational",
            "version": "1.0.0"
        },
        "message": "RithStore-Free Car Parking API Running",
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })

@app.route('/api/health')
def health():
    """Health check endpoint"""
    try:
        response = requests.get(f"{CAR_API_URL}/api/health", timeout=10)
        data = response.json()
        
        # Add proxy info
        if isinstance(data, dict):
            data['_proxy'] = {
                'service': 'car_parking',
                'timestamp': datetime.now().isoformat()
            }
        
        return jsonify(data), response.status_code
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": f"Cannot connect to Car Parking API: {str(e)}",
            "service": "Car Parking API",
            "timestamp": datetime.now().isoformat()
        }), 502

@app.route('/api/account')
def get_car_account():
    """Get a free car parking account"""
    try:
        response = requests.get(f"{CAR_API_URL}/api/account", timeout=10)
        data = response.json()
        
        # Add proxy info
        if isinstance(data, dict):
            data['_proxy'] = {
                'service': 'car_parking',
                'timestamp': datetime.now().isoformat()
            }
        
        return jsonify(data), response.status_code
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": f"Cannot get car account: {str(e)}",
            "service": "Car Parking API",
            "timestamp": datetime.now().isoformat()
        }), 502

@app.route('/api/stats')
def get_car_stats():
    """Get car parking checker statistics"""
    try:
        response = requests.get(f"{CAR_API_URL}/api/stats", timeout=10)
        data = response.json()
        
        # Add proxy info
        if isinstance(data, dict):
            data['_proxy'] = {
                'service': 'car_parking',
                'timestamp': datetime.now().isoformat()
            }
        
        return jsonify(data), response.status_code
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": f"Cannot get car stats: {str(e)}",
            "service": "Car Parking API",
            "timestamp": datetime.now().isoformat()
        }), 502

@app.route('/api/queue')
def get_car_queue():
    """Check car accounts queue"""
    try:
        response = requests.get(f"{CAR_API_URL}/api/queue", timeout=10)
        data = response.json()
        
        # Add proxy info
        if isinstance(data, dict):
            data['_proxy'] = {
                'service': 'car_parking',
                'timestamp': datetime.now().isoformat()
            }
        
        return jsonify(data), response.status_code
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": f"Cannot get car queue: {str(e)}",
            "service": "Car Parking API",
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
            "/api/account", 
            "/api/stats",
            "/api/queue"
        ],
        "service": "RithStore-Free Car Parking API",
        "timestamp": datetime.now().isoformat()
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal server error",
        "message": "Please try again later",
        "service": "RithStore-Free Car Parking API",
        "timestamp": datetime.now().isoformat()
    }), 500

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "error": "Method not allowed",
        "message": "Check the endpoint documentation for allowed methods",
        "timestamp": datetime.now().isoformat()
    }), 405

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))  # Using 5001 to avoid conflict
    print(f"🚗 RithStore-Free Car Parking API Gateway starting on port {port}")
    print(f"🎮 Car Parking API: {CAR_API_URL}")
    print(f"🌐 Gateway URL: http://0.0.0.0:{port}")
    print(f"📋 Available endpoints:")
    print(f"   GET  /api/health  - Health check")
    print(f"   GET  /api/account - Get free account") 
    print(f"   GET  /api/stats   - Get statistics")
    print(f"   GET  /api/queue   - Check queue")
    app.run(host='0.0.0.0', port=port, debug=False)
