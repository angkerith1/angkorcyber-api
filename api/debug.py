def handler(request, context):
    print("DEBUG: Handler called")
    print("DEBUG: Request:", request)
    
    try:
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
            },
            'body': '{"status": "ok", "message": "Debug test"}'
        }
    except Exception as e:
        print("DEBUG: Error:", str(e))
        return {
            'statusCode': 500,
            'body': f'{{"error": "{str(e)}"}}'
        }
