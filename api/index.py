from http.server import BaseHTTPRequestHandler
import requests
import json
import urllib.parse
from datetime import datetime

class AngkorProxyHandler(BaseHTTPRequestHandler):
    
    # API Configuration
    API_CONFIG = {
        "angkor": {
            "base_url": "http://5.175.234.87:5000",
            "endpoints": {
                "/": "API Information",
                "/api/health": "Health Check",
                "/api/databases": "List Databases",
                "/api/check": "Check Breaches",
                "/api/stats": "Get Statistics",
                "/api/search": "Search Multiple",
                "/api/admin/reload": "Admin Reload"
            }
        },
        "json": {
            "base_url": "https://jsonplaceholder.typicode.com",
            "endpoints": {
                "/users": "Get Users",
                "/posts": "Get Posts",
                "/comments": "Get Comments"
            }
        }
    }

    def do_GET(self):
        """Handle GET requests"""
        self.handle_request('GET')

    def do_POST(self):
        """Handle POST requests"""
        self.handle_request('POST')

    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()

    def send_cors_headers(self):
        """Send CORS headers"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With')

    def handle_request(self, method):
        """Main request handler"""
        try:
            parsed_path = urllib.parse.urlparse(self.path)
            path = parsed_path.path
            query_params = urllib.parse.parse_qs(parsed_path.query)

            # Remove trailing slash
            if path.endswith('/') and len(path) > 1:
                path = path[:-1]

            # Route requests
            if path == '' or path == '/':
                self.serve_api_info()
            elif path.startswith('/api/angkor'):
                self.proxy_angkor_api(path, method, query_params)
            elif path.startswith('/api/json'):
                self.proxy_json_api(path, method, query_params)
            elif path == '/api/proxy':
                self.handle_universal_proxy(method, query_params)
            elif path == '/api/health':
                self.serve_health_check()
            elif path == '/api/services':
                self.serve_services_list()
            else:
                self.send_error_response(404, "Endpoint not found")

        except Exception as e:
            self.send_error_response(500, f"Internal server error: {str(e)}")

    def serve_api_info(self):
        """Serve API information"""
        api_info = {
            "data": {
                "api": "AngkorCyber Security API - HTTPS Gateway",
                "endpoints": {
                    "/": "API Information (this page)",
                    "/api/health": "System health check",
                    "/api/services": "List all services",
                    "/api/angkor/health": "Angkor API Health",
                    "/api/angkor/databases": "List databases",
                    "/api/angkor/check": "Check breaches",
                    "/api/angkor/stats": "Get statistics",
                    "/api/json/users": "JSONPlaceholder Users",
                    "/api/proxy": "Universal proxy"
                },
                "status": "operational",
                "supported_formats": [
                    "email:password", "email|password", "email;password", "email password",
                    "phone:password", "phone|password", "phone password", "plain email",
                    "plain phone", "username:password"
                ],
                "version": "3.0.0"
            },
            "message": "Welcome to AngkorCyber Security HTTPS API Gateway",
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "version": "3.0.0"
        }
        self.send_json_response(200, api_info)

    def serve_health_check(self):
        """Serve health check"""
        health_info = {
            "status": "healthy",
            "service": "AngkorCyber HTTPS Gateway",
            "timestamp": datetime.now().isoformat(),
            "version": "3.0.0"
        }
        self.send_json_response(200, health_info)

    def serve_services_list(self):
        """List all available services"""
        services = {}
        for service_name, config in self.API_CONFIG.items():
            services[service_name] = {
                "base_url": config["base_url"],
                "endpoints": list(config["endpoints"].keys()),
                "status": "available"
            }
        
        response = {
            "services": services,
            "timestamp": datetime.now().isoformat()
        }
        self.send_json_response(200, response)

    def proxy_angkor_api(self, path, method, query_params):
        """Proxy to AngkorCyber API"""
        path_mapping = {
            '/api/angkor': '/',
            '/api/angkor/health': '/api/health',
            '/api/angkor/databases': '/api/databases',
            '/api/angkor/check': '/api/check',
            '/api/angkor/stats': '/api/stats',
            '/api/angkor/search': '/api/search',
            '/api/angkor/admin/reload': '/api/admin/reload'
        }

        target_path = path_mapping.get(path, '/')
        target_url = f"http://5.175.234.87:5000{target_path}"

        if query_params:
            query_string = '&'.join([f"{k}={v[0]}" for k, v in query_params.items()])
            target_url += '?' + query_string

        self.make_proxy_request(target_url, method, "AngkorCyber API")

    def proxy_json_api(self, path, method, query_params):
        """Proxy to JSONPlaceholder API"""
        path_mapping = {
            '/api/json': '/',
            '/api/json/users': '/users',
            '/api/json/posts': '/posts',
            '/api/json/comments': '/comments'
        }

        target_path = path_mapping.get(path, '/')
        target_url = f"https://jsonplaceholder.typicode.com{target_path}"

        if query_params:
            query_string = '&'.join([f"{k}={v[0]}" for k, v in query_params.items()])
            target_url += '?' + query_string

        self.make_proxy_request(target_url, method, "JSONPlaceholder API")

    def handle_universal_proxy(self, method, query_params):
        """Handle universal proxy requests"""
        if method != 'GET':
            self.send_error_response(405, "Only GET method supported")
            return

        url = query_params.get('url', [None])[0]
        if not url:
            self.send_error_response(400, "URL parameter is required")
            return

        self.make_proxy_request(url, 'GET', "Universal Proxy")

    def make_proxy_request(self, target_url, method, service_name):
        """Make proxy request to target API"""
        try:
            headers = {
                'User-Agent': 'AngkorCyber-HTTPS-Proxy/1.0',
                'Accept': 'application/json'
            }

            if method == 'GET':
                response = requests.get(target_url, headers=headers, timeout=10)
            elif method == 'POST':
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length) if content_length > 0 else None
                
                if post_data:
                    response = requests.post(target_url, data=post_data, headers=headers, timeout=10)
                else:
                    response = requests.post(target_url, headers=headers, timeout=10)
            else:
                self.send_error_response(405, f"Method {method} not supported")
                return

            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')
                
                if 'application/json' in content_type:
                    try:
                        data = response.json()
                        if isinstance(data, dict):
                            data['_proxy'] = {
                                'service': service_name,
                                'secured': True,
                                'timestamp': datetime.now().isoformat()
                            }
                        self.send_json_response(200, data)
                    except:
                        self.send_text_response(200, response.text)
                else:
                    self.send_text_response(200, response.text)
            else:
                self.send_error_response(response.status_code, {
                    "error": f"Backend service returned {response.status_code}",
                    "service": service_name
                })

        except requests.exceptions.Timeout:
            self.send_error_response(504, "Gateway timeout")
        except requests.exceptions.RequestException as e:
            self.send_error_response(502, f"Bad gateway: {str(e)}")

    def send_json_response(self, status_code, data):
        """Send JSON response"""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def send_text_response(self, status_code, text):
        """Send text response"""
        self.send_response(status_code)
        self.send_header('Content-type', 'text/plain')
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(text.encode())

    def send_error_response(self, status_code, message):
        """Send error response"""
        if isinstance(message, dict):
            error_data = message
        else:
            error_data = {"error": message}
        
        error_data["timestamp"] = datetime.now().isoformat()
        self.send_json_response(status_code, error_data)

# Vercel handler
def handler(request, context):
    return AngkorProxyHandler()
