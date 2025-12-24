import json
import uuid
import redis

# connect to local docker Redis
db = redis.Redis(host='localhost', port=6379, decode_responses=True)

def create(event, context):
    body = json.loads(event['body'])
    long_url = body.get('Url', '')
    short_id = str(uuid.uuid4())[:6]

    db.set(short_id, long_url)

    return {
        'statusCode': 200,
        'body': json.dumps({'shortUrl': f"http://localhost:8000/{short_id}"}),
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
            'body':' Not Found  '}