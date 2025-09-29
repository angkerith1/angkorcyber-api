from http.server import BaseHTTPRequestHandler
import requests
import json
from urllib.parse import urlparse, parse_qs
from datetime import datetime

class ProxyHandler(BaseHTTPRequestHandler):
    
    # API Configuration - ADD YOUR APIS HERE
    API_CONFIG = {
        # Main AngkorCyber API
        "angkor": {
            "base_url": "http://5.175.234.87:5000",
            "endpoints": {
                "/": {"methods": ["GET"]},
                "/api/health": {"methods": ["GET"]},
                "/api/databases": {"methods": ["GET"]},
                "/api/check": {"methods": ["GET", "POST"]},
                "/api/stats": {"methods": ["GET"]},
                "/api/search": {"methods": ["POST"]},
                "/api/admin/reload": {"methods": ["POST"]}
            }
        },
        # JSON Placeholder API (example)
        "json": {
            "base_url": "https://jsonplaceholder.typicode.com",
            "endpoints": {
                "/users": {"methods": ["GET"]},
                "/posts": {"methods": ["GET", "POST"]},
                "/comments": {"methods": ["GET"]}
            }
        },
        # ADD YOUR CUSTOM APIS HERE:
        "myapi": {
            "base_url": "http://your-api-domain.com",
            "endpoints": {
                "/data": {"methods": ["GET"]},
                "/users": {"methods": ["GET", "POST"]}
            }
        }
    }
    
    def do_GET(self):
        self.handle_request('GET')
    
    def do_POST(self):
        self.handle_request('POST')
    
    def do_PUT(self):
        self.handle_request('PUT')
    
    def do_DELETE(self):
        self.handle_request('DELETE')
    
    def do_OPTIONS(self):
        self.send_cors_headers()
        self.send_response(200)
        self.end_headers()
    
    def send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With')
    
    def handle_request(self, method):
        path = self.path.rstrip('/')
        
        # Route the request
        if path == "" or path == "/":
            self.serve_api_info()
        elif path.startswith("/api/angkor/"):
            self.proxy_to_api("angkor", path.replace("/api/angkor", ""), method)
        elif path.startswith("/api/json/"):
            self.proxy_to_api("json", path.replace("/api/json", ""), method)
        elif path.startswith("/api/myapi/"):
            self.proxy_to_api("myapi", path.replace("/api/myapi", ""), method)
        else:
            self.send_error(404, "Endpoint not found")
    
    def serve_api_info(self):
        """Serve API information"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_cors_headers()
        self.end_headers()
        
        info = {
            "api": "AngkorCyber Unified HTTPS Proxy",
            "version": "3.0.0",
            "timestamp": datetime.now().isoformat(),
            "available_services": {},
            "endpoints": {
                "/": "This information",
                "/api/angkor/*": "AngkorCyber Security API",
                "/api/json/*": "JSONPlaceholder API",
                "/api/myapi/*": "Your Custom API"
            }
        }
        
        for service_name, config in self.API_CONFIG.items():
            info["available_services"][service_name] = {
                "base_url": config["base_url"],
                "endpoints": list(config["endpoints"].keys())
            }
        
        self.wfile.write(json.dumps(info, indent=2).encode())
    
    def proxy_to_api(self, service_name, path, method):
        """Proxy request to backend API"""
        if service_name not in self.API_CONFIG:
            self.send_error(404, f"Service '{service_name}' not found")
            return
        
        config = self.API_CONFIG[service_name]
        base_url = config["base_url"]
        endpoints = config["endpoints"]
        
        # Find matching endpoint
        target_endpoint = None
        for endpoint in endpoints:
            if path == endpoint or path.startswith(endpoint + '/'):
                target_endpoint = endpoint
                break
        
        if not target_endpoint or method not in endpoints[target_endpoint]["methods"]:
            self.send_error(405, f"Method {method} not allowed for {path}")
            return
        
        # Build target URL
        if path.startswith(target_endpoint + '/') and len(path) > len(target_endpoint) + 1:
            remaining_path = path[len(target_endpoint):]
            target_url = base_url.rstrip('/') + target_endpoint + remaining_path
        else:
            target_url = base_url.rstrip('/') + path
        
        # Add query parameters
        parsed_path = urlparse(self.path)
        if parsed_path.query:
            target_url += '?' + parsed_path.query
        
        try:
            # Prepare headers
            headers = {
                'User-Agent': 'AngkorCyber-HTTPS-Proxy/1.0',
                'Accept': 'application/json'
            }
            
            # Forward request
            if method == 'GET':
                response = requests.get(target_url, headers=headers, timeout=30)
            elif method == 'POST':
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)
                headers['Content-Type'] = self.headers.get('Content-Type', 'application/json')
                response = requests.post(target_url, data=post_data, headers=headers, timeout=30)
            elif method == 'PUT':
                content_length = int(self.headers.get('Content-Length', 0))
                put_data = self.rfile.read(content_length)
                headers['Content-Type'] = self.headers.get('Content-Type', 'application/json')
                response = requests.put(target_url, data=put_data, headers=headers, timeout=30)
            elif method == 'DELETE':
                response = requests.delete(target_url, headers=headers, timeout=30)
            
            # Forward response
            self.send_response(response.status_code)
            self.send_header('Content-type', 'application/json')
            self.send_cors_headers()
            self.send_header('X-Proxy-Server', 'AngkorCyber-HTTPS-Gateway')
            self.send_header('X-Proxied-From', target_url)
            self.end_headers()
            
            self.wfile.write(response.content)
            
        except requests.exceptions.RequestException as e:
            self.send_error(502, f"Gateway error: {str(e)}")
    
    def send_error(self, code, message):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.send_cors_headers()
        self.end_headers()
        
        error_response = {
            "error": True,
            "code": code,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "proxy": "AngkorCyber HTTPS Proxy"
        }
        
        self.wfile.write(json.dumps(error_response).encode())
    
    def log_message(self, format, *args):
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {format % args}")

# Vercel handler
def handler(request, context):
    return ProxyHandler()
