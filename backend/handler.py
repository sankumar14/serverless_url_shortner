import json
import uuid
import redis
import os

# connect to local docker Redis
db = redis.Redis(host='localhost', port=6379, decode_responses=True, socket_timeout=5)

def create(event, context):
    try:
        body = json.loads(event.get('body', {}))

        long_url = body.get('url', '')
        if not long_url:
            print("DEBUG: Body received:", body)
            return {
                'statusCode': 400,
                'body': json.dumps({'error': f'url is required. Body: {body}'}),
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Credentials': 'True',
                }
            }
        short_id = str(uuid.uuid4())[:6]

        db.set(short_id, long_url)
        response = {
            "shortUrl": f"http://localhost:3000/dev/{short_id}"
             }

        return {
            'statusCode': 200,
            'body': json.dumps({"shortUrl": f"http://localhost:3000/dev/{short_id}"}),
            'headers': {
                "Content-Type": "application/json",
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': 'True',
            }
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': 'True',
            }
        }

def redirect(event, context):
    short_id = event['pathParameters']['shortId']
    long_url = db.get(short_id)

    if long_url:
        return {
            'statusCode': 301,
            'headers': {
                'Location': long_url
            }
        }
    return {
            'statusCode': 404,
            'body': json.dumps({'error': 'URL not found'}) 
            }