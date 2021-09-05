import base64
import boto3
import os
from utils import jsonify

S3_BUCKET = os.environ["IMAGE_BUCKET"]
REGION = os.environ["REGION"]
USERS_TABLE = os.environ["USERS_TABLE"]

dynamo_resource = boto3.resource("dynamodb", region_name=REGION)
s3_client = boto3.client("s3", region_name=REGION)
users_table = dynamo_resource.Table(USERS_TABLE)

def get(event, context):
    print(event)
    jresp = {'data': [], 'nextToken': None}
    statusCode=200
    try:
        next_token = event.get('queryStringParameters', {}).get('nextToken', None)
        start_key = _decode_token(next_token)
        items, last_key = _list_faces(start_key)
        next_token = _encode_token(last_key)
        
        j = 0
        for item in items:
            url_item = item.get('paths3')
            url = s3_client.generate_presigned_url(
                ClientMethod='get_object',
                Params={
                    'Bucket': S3_BUCKET,
                    'Key': url_item
                }
            )
            items[j]["paths3sign"] = url
            j = j + 1

        
        jresp = {'data': items, 'nextToken': next_token}

    except Exception as e:
        msgError = "An exception occurred " + str(e) + "."
        print(msgError)
        jresp = {'Error': msgError}
        statusCode=500

    print(jresp)
    return jsonify(jresp, statusCode)


def _list_faces(start_key=None, limit=3):
    if start_key:
        response = users_table.scan(ExclusiveStartKey=start_key, Limit=limit)
    else:
        response = users_table.scan(Limit=limit)
    
    items = response.get('Items', [])
    last_eval_key = response.get('LastEvaluatedKey', None)
    
    return items, last_eval_key

def _encode_token(start_key):
    if start_key:
        return base64.b64encode(f'{start_key["faceid"]}#{start_key["name"]}'.encode()).decode()
    
def _decode_token(encoded_str):
    if encoded_str:
        faceid, name = base64.b64decode(encoded_str.encode()).decode().split('#')
        return {
            'faceid': faceid,
            'name': name
        }