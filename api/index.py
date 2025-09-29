import requests
import json
from datetime import datetime
import traceback

def handler(request, context):
    """Vercel serverless function handler"""
    print(f"Received request: {request.get('httpMethod', 'UNKNOWN')} {request.get('path', 'UNKNOWN')}")
    
    try:
        # Extract request details
        method = request.get('httpMethod', 'GET')
        path = request.get('path', '/')
        query_params = request.get('queryStringParameters', {}) or {}
        headers = request.get('headers', {})
        body = request.get('body', '')
        
        print(f"Processing: {method} {path}")
        
        # Create API handler
        api_handler = AngkorProxyHandler()
        
        # Route the request
        if path == '/' or path == '':
            return api_handler.serve_api_info()
        elif path.startswith('/api/angkor'):
            return api_handler.proxy_angkor_api(path, method, query_params, body, headers)
        elif path.startswith('/api/json'):
            return api_handler.proxy_json_api(path, method, query_params, body, headers)
        elif path == '/api/proxy':
            return api_handler.handle_universal_proxy(method, query_params)
        elif path == '/api/health':
            return api_handler.serve_health_check()
        elif path == '/api/services':
            return api_handler.serve_services_list()
        else:
            return api_handler.send_error_response(404, "Endpoint not found")
            
    except Exception as e:
        print(f"CRITICAL ERROR: {str(e)}")
        print(traceback.format_exc())
        
        # Return a simple error response
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                "error": "Internal server error",
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            })
        }

class AngkorProxyHandler:
    """Main API handler"""
    
    def __init__(self):
        self.API_CONFIG = {
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

    def serve_api_info(self):
        """Serve API information"""
        print("Serving API info")
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
        return self.send_json_response(200, api_info)

    def serve_health_check(self):
        """Serve health check"""
        print("Serving health check")
        health_info = {
            "status": "healthy",
            "service": "AngkorCyber HTTPS Gateway",
            "timestamp": datetime.now().isoformat(),
            "version": "3.0.0",
            "environment": "production"
        }
        return self.send_json_response(200, health_info)

    def serve_services_list(self):
        """List all available services"""
        print("Serving services list")
        services = {}
        for service_name, config in self.API_CONFIG.items():
            services[service_name] = {
                "base_url": config["base_url"],
                "endpoints": list(config["endpoints"].keys()),
                "status": "available"
            }
        
        response = {
            "services": services,
            "timestamp": datetime.now().isoformat(),
            "total_services": len(services)
        }
        return self.send_json_response(200, response)

    def proxy_angkor_api(self, path, method, query_params, body, headers):
        """Proxy to AngkorCyber API"""
        print(f"Proxying to Angkor API: {path}")
        
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

        # Add query parameters
        if query_params:
            query_string = '&'.join([f"{k}={v}" for k, v in query_params.items()])
            target_url += '?' + query_string

        return self.make_proxy_request(target_url, method, body, headers, "AngkorCyber API")

    def proxy_json_api(self, path, method, query_params, body, headers):
        """Proxy to JSONPlaceholder API"""
        print(f"Proxying to JSON API: {path}")
        
        path_mapping = {
            '/api/json': '/',
            '/api/json/users': '/users',
            '/api/json/posts': '/posts',
            '/api/json/comments': '/comments'
        }

        target_path = path_mapping.get(path, '/')
        target_url = f"https://jsonplaceholder.typicode.com{target_path}"

        if query_params:
            query_string = '&'.join([f"{k}={v}" for k, v in query_params.items()])
            target_url += '?' + query_string

        return self.make_proxy_request(target_url, method, body, headers, "JSONPlaceholder API")

    def handle_universal_proxy(self, method, query_params):
        """Handle universal proxy requests"""
        print("Handling universal proxy")
        
        if method != 'GET':
            return self.send_error_response(405, "Only GET method supported")

        url = query_params.get('url')
        if not url:
            return self.send_error_response(400, "URL parameter is required")

        return self.make_proxy_request(url, 'GET', '', {}, "Universal Proxy")

    def make_proxy_request(self, target_url, method, body, headers, service_name):
        """Make proxy request to target API"""
        print(f"Making proxy request to: {target_url}")
        
        try:
            request_headers = {
                'User-Agent': 'AngkorCyber-HTTPS-Proxy/1.0',
                'Accept': 'application/json'
            }

            # Forward relevant headers
            if headers.get('content-type'):
                request_headers['Content-Type'] = headers['content-type']
            if headers.get('authorization'):
                request_headers['Authorization'] = headers['authorization']

            timeout = 10

            if method == 'GET':
                print(f"GET request to {target_url}")
                response = requests.get(target_url, headers=request_headers, timeout=timeout)
            elif method == 'POST':
                print(f"POST request to {target_url}")
                response = requests.post(target_url, data=body, headers=request_headers, timeout=timeout)
            else:
                return self.send_error_response(405, f"Method {method} not supported")

            print(f"Response status: {response.status_code}")

            # Handle response
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')
                
                if 'application/json' in content_type:
                    try:
                        data = response.json()
                        if isinstance(data, dict):
                            data['_proxy'] = {
                                'service': service_name,
                                'secured': True,
                                'timestamp': datetime.now().isoformat(),
                                'original_url': target_url
                            }
                        return self.send_json_response(200, data)
                    except Exception as e:
                        print(f"JSON parse error: {e}")
                        return self.send_text_response(200, response.text)
                else:
                    return self.send_text_response(200, response.text)
            else:
                return self.send_error_response(response.status_code, {
                    "error": f"Backend service returned {response.status_code}",
                    "service": service_name,
                    "target_url": target_url
                })

        except requests.exceptions.Timeout:
            print("Request timeout")
            return self.send_error_response(504, {
                "error": "Gateway timeout",
                "service": service_name
            })
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return self.send_error_response(502, {
                "error": f"Bad gateway: {str(e)}",
                "service": service_name
            })
        except Exception as e:
            print(f"Unexpected error in proxy: {e}")
            return self.send_error_response(500, {
                "error": f"Proxy error: {str(e)}",
                "service": service_name
            })

    def send_json_response(self, status_code, data):
        """Send JSON response"""
        print(f"Sending JSON response: {status_code}")
        return {
            'statusCode': status_code,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization'
            },
            'body': json.dumps(data, ensure_ascii=False)
        }

    def send_text_response(self, status_code, text):
        """Send text response"""
        print(f"Sending text response: {status_code}")
        return {
            'statusCode': status_code,
            'headers': {
                'Content-Type': 'text/plain',
                'Access-Control-Allow-Origin': '*'
            },
            'body': text
        }

    def send_error_response(self, status_code, message):
        """Send error response"""
        print(f"Sending error response: {status_code} - {message}")
        
        if isinstance(message, dict):
            error_data = message
        else:
            error_data = {"error": message}
        
        error_data["timestamp"] = datetime.now().isoformat()
        return self.send_json_response(status_code, error_data)
