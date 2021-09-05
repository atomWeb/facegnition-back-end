import boto3
from boto3.dynamodb.conditions import Key
import os
from utils import jsonify

S3_BUCKET = os.environ["IMAGE_BUCKET"]
REGION = os.environ["REGION"]
VALIDATIONS_TABLE = os.environ["VALIDATIONS_TABLE"]

s3_client = boto3.client("s3", region_name = REGION)
dynamo_resource = boto3.resource("dynamodb", region_name=REGION)
validations_table = dynamo_resource.Table(VALIDATIONS_TABLE)

def get(event, context):
    print(event)
    jresp = {'data': []}
    statusCode=200
    try:
        
        face_id = event.get('pathParameters', {}).get('faceid')

        response = validations_table.query(
            KeyConditionExpression=Key("faceid").eq(face_id),
            ProjectionExpression='timest,s3path',
            ScanIndexForward=False,
            Limit=10
        )

        items = response.get('Items', [])
        
        j = 0
        for item in items:
            url_item = item.get('s3path')
            url = s3_client.generate_presigned_url(
                ClientMethod='get_object',
                Params={
                    'Bucket': S3_BUCKET,
                    'Key': url_item
                }
            )
            items[j]["avatarpath"] = url
            j = j + 1            


    except Exception as e:
        msgError = "An exception occurred " + str(e) + "."
        print(msgError)
        jresp = {'Error': msgError}
        statusCode=500

    
    jresp = {'data': items}
    print(jresp)
    return jsonify(jresp, statusCode)
