import boto3
import os
import uuid
from utils import jsonify

S3_BUCKET = os.environ["IMAGE_BUCKET"]
REGION = os.environ["REGION"]
s3_client = boto3.client("s3", region_name=REGION)

def get(event, context):
    print(event)
    
    file_uuid = str(uuid.uuid1())
    key = f'{file_uuid}.jpg'

    url = s3_client.generate_presigned_url(
        ClientMethod='put_object',
        Params={
            'Bucket': S3_BUCKET,
            'Key': key,
            'ContentType': 'image/jpeg'
        }
    )

    return jsonify({'url': url, 'key': key})
