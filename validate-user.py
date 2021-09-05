import json
import boto3
from boto3.dynamodb.conditions import Key
import os
from utils import jsonify, get_str_timestamp_by_zone

S3_BUCKET = os.environ["IMAGE_BUCKET"]
REGION = os.environ["REGION"]
USERS_TABLE = os.environ["USERS_TABLE"]
VALIDATIONS_TABLE = os.environ["VALIDATIONS_TABLE"]
COLLECT_NAME = os.environ["REKOGN_COLLECTION"]
ZONE = os.environ["TIME_ZONE"]

s3_client = boto3.client("s3", region_name=REGION)
dynamo_resource = boto3.resource("dynamodb", region_name=REGION)
users_table = dynamo_resource.Table(USERS_TABLE)
validations_table = dynamo_resource.Table(VALIDATIONS_TABLE)
rekog = boto3.client('rekognition', region_name=REGION)


def validate(event, context):

    print(event)
    jresp = {'data': ''}
    statusCode=200
    faceId = "None"
    usr_name = ""
    try:
        # Datos de la ejecución
        data = json.loads(event["body"])
        s3path = data["imgname"]        

        # buscar caras por imagen en una colección
        response = rekog.search_faces_by_image(
            CollectionId=COLLECT_NAME,
            Image={
                'S3Object': {
                    'Bucket': S3_BUCKET,
                    'Name': s3path
                }
            },
            MaxFaces=5,
            FaceMatchThreshold=97.0,
            QualityFilter='AUTO'
        )

        print("Response rekognition buscar cara: ", response)

        if not response['FaceMatches']:
            statusCode = 404
        else:
            faceId = response['FaceMatches'][0]['Face']['FaceId']            
            timestamp = get_str_timestamp_by_zone(ZONE)

            # Guarda en la DB el registro de la validacion.
            response = validations_table.put_item(
                Item={
                    'faceid': faceId,
                    'timest': timestamp,
                    's3path': s3path
                }
            )
            print("Response Dynamo tabla validations: ", response)
            # Nota: Al guardar este registro en dynamo disparará la lambda que verifica el notify en la tabla de user y lanzara el email

            usrs_resp = users_table.query(
                KeyConditionExpression=Key("faceid").eq(faceId),
                Limit=1
            )            
            items = usrs_resp.get('Items', [])
            if items:                
                usr_name = items[0]["name"]

    except Exception as e:
        msgError = "An exception occurred " + str(e) + "."
        print(msgError)
        jresp = {'Error': msgError}
        statusCode = 500
 
    jresp = {"face-id": faceId, "name": usr_name}
    return jsonify(jresp, statusCode)
