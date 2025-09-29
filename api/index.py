import json
from datetime import datetime

def handler(request, context):
    """Simple handler that always works"""
    print("Handler called successfully!")
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            "status": "success",
            "message": "API is working!",
            "timestamp": datetime.now().isoformat(),
            "version": "3.0.0"
        })
    }
