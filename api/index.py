import requests
import json
import time
from datetime import datetime

class AngkorCyberAPIChecker:
    def __init__(self, base_url="http://5.175.234.87:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.timeout = 10  # 10 seconds timeout
        
    def check_api_online(self):
        """Check if the main API endpoint is online"""
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                data = response.json()
                return {
                    "online": True,
                    "status": "operational",
                    "data": data,
                    "response_time": response.elapsed.total_seconds(),
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "online": False,
                    "status": f"HTTP {response.status_code}",
                    "error": f"Server returned status code: {response.status_code}",
                    "timestamp": datetime.now().isoformat()
                }
        except requests.exceptions.RequestException as e:
            return {
                "online": False,
                "status": "offline",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def check_health_endpoint(self):
        """Check the health endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/api/health")
            if response.status_code == 200:
                return {
                    "online": True,
                    "health_data": response.json(),
                    "response_time": response.elapsed.total_seconds()
                }
            else:
                return {
                    "online": False,
                    "error": f"Health endpoint returned {response.status_code}"
                }
        except requests.exceptions.RequestException as e:
            return {
                "online": False,
                "error": str(e)
            }
    
    def check_databases_endpoint(self):
        """Check the databases endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/api/databases")
            if response.status_code == 200:
                return {
                    "online": True,
                    "databases_data": response.json(),
                    "response_time": response.elapsed.total_seconds()
                }
            else:
                return {
                    "online": False,
                    "error": f"Databases endpoint returned {response.status_code}"
                }
        except requests.exceptions.RequestException as e:
            return {
                "online": False,
                "error": str(e)
            }
    
    def check_breach(self, query="test@example.com"):
        """Check breach endpoint with a test query"""
        try:
            # Try GET request first
            response = self.session.get(f"{self.base_url}/api/check", params={"query": query})
            if response.status_code == 200:
                return {
                    "online": True,
                    "method": "GET",
                    "breach_data": response.json(),
                    "response_time": response.elapsed.total_seconds()
                }
            else:
                # Try POST request
                response = self.session.post(f"{self.base_url}/api/check", json={"query": query})
                if response.status_code == 200:
                    return {
                        "online": True,
                        "method": "POST",
                        "breach_data": response.json(),
                        "response_time": response.elapsed.total_seconds()
                    }
                else:
                    return {
                        "online": False,
                        "error": f"Both GET and POST returned {response.status_code}"
                    }
        except requests.exceptions.RequestException as e:
            return {
                "online": False,
                "error": str(e)
            }
    
    def comprehensive_check(self):
        """Perform comprehensive check of all endpoints"""
        print(f"🔍 Checking AngkorCyber API at: {self.base_url}")
        print("=" * 60)
        
        # Check main endpoint
        print("1. Checking main API endpoint...")
        main_status = self.check_api_online()
        
        if main_status["online"]:
            print("✅ MAIN API: ONLINE")
            print(f"   Status: {main_status['data'].get('status', 'N/A')}")
            print(f"   Version: {main_status['data'].get('version', 'N/A')}")
            print(f"   Response Time: {main_status['response_time']:.3f}s")
            print(f"   Message: {main_status['data'].get('message', 'N/A')}")
            
            # Check other endpoints
            print("\n2. Checking health endpoint...")
            health_status = self.check_health_endpoint()
            if health_status["online"]:
                print("✅ HEALTH: ONLINE")
                print(f"   Status: {health_status['health_data'].get('status', 'N/A')}")
            else:
                print("❌ HEALTH: OFFLINE")
                print(f"   Error: {health_status['error']}")
            
            print("\n3. Checking databases endpoint...")
            db_status = self.check_databases_endpoint()
            if db_status["online"]:
                print("✅ DATABASES: ONLINE")
                db_data = db_status["databases_data"]
                print(f"   Total Databases: {db_data.get('total_databases', 'N/A')}")
                print(f"   Total Records: {db_data.get('total_records', 'N/A')}")
            else:
                print("❌ DATABASES: OFFLINE")
                print(f"   Error: {db_status['error']}")
            
            print("\n4. Testing breach check endpoint...")
            breach_status = self.check_breach()
            if breach_status["online"]:
                print("✅ BREACH CHECK: ONLINE")
                print(f"   Method: {breach_status['method']}")
                print(f"   Breaches Found: {breach_status['breach_data'].get('breaches_found', 'N/A')}")
            else:
                print("❌ BREACH CHECK: OFFLINE")
                print(f"   Error: {breach_status['error']}")
                
        else:
            print("❌ MAIN API: OFFLINE")
            print(f"   Error: {main_status['error']}")
            print(f"   Status: {main_status['status']}")
        
        print("\n" + "=" * 60)
        return main_status

    def monitor_api(self, interval_seconds=60):
        """Continuously monitor the API status"""
        print(f"🚀 Starting API monitoring every {interval_seconds} seconds...")
        print(f"📡 Monitoring: {self.base_url}")
        print("Press Ctrl+C to stop monitoring\n")
        
        try:
            while True:
                result = self.check_api_online()
                status_icon = "✅" if result["online"] else "❌"
                status_text = "ONLINE" if result["online"] else "OFFLINE"
                
                print(f"{status_icon} [{datetime.now().strftime('%H:%M:%S')}] API is {status_text}", end="")
                
                if result["online"]:
                    print(f" | Version: {result['data'].get('version', 'N/A')} | Response: {result['response_time']:.3f}s")
                else:
                    print(f" | Error: {result['error']}")
                
                time.sleep(interval_seconds)
                
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user")

def test_with_mock_data():
    """Test with the exact data structure you provided"""
    mock_api_data = {
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
        "timestamp": "2025-09-29T01:40:45.039892",
        "version": "3.0.0"
    }
    
    print("📋 MOCK API DATA STRUCTURE:")
    print(json.dumps(mock_api_data, indent=2))
    return mock_api_data

if __name__ == "__main__":
    # Create checker instance
    checker = AngkorCyberAPIChecker("http://5.175.234.87:5000")
    
    print("AngkorCyber API Status Checker")
    print("1. Quick Status Check")
    print("2. Comprehensive Check")
    print("3. Continuous Monitoring")
    print("4. Test with Mock Data")
    
    choice = input("\nSelect option (1-4): ").strip()
    
    if choice == "1":
        result = checker.check_api_online()
        if result["online"]:
            print(f"✅ API is ONLINE - {result['data'].get('message')}")
        else:
            print(f"❌ API is OFFLINE - {result['error']}")
            
    elif choice == "2":
        checker.comprehensive_check()
        
    elif choice == "3":
        interval = input("Enter check interval in seconds (default: 60): ").strip()
        interval = int(interval) if interval.isdigit() else 60
        checker.monitor_api(interval)
        
    elif choice == "4":
        test_with_mock_data()
        
    else:
        print("Running quick check...")
        result = checker.check_api_online()
        if result["online"]:
            print(f"✅ API is ONLINE")
            print(f"📊 Status: {result['data'].get('status')}")
            print(f"🕒 Response Time: {result['response_time']:.3f}s")
        else:
            print(f"❌ API is OFFLINE")
            print(f"🔧 Error: {result['error']}")
