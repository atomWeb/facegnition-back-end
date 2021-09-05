import json
import boto3
import os
from utils import jsonify

S3_BUCKET = os.environ["IMAGE_BUCKET"]
REGION = os.environ["REGION"]
USERS_TABLE = os.environ["USERS_TABLE"]
COLLECT_NAME = os.environ["REKOGN_COLLECTION"]

s3_client = boto3.client("s3", region_name=REGION)
dynamo_resource = boto3.resource("dynamodb", region_name=REGION)
users_table = dynamo_resource.Table(USERS_TABLE)
rekog = boto3.client('rekognition', region_name=REGION)


def add(event, context):

    print(event)
    jresp = {'data': ''}
    statusCode=200

    try:
        # Datos de la ejecución
        data = json.loads(event["body"])
        name = data["nombre"]
        notify = data["notify"]
        s3path = data["imgname"]        

        # Listar y buscar la coleccion rekognition
        max_results = 5
        isCollectionFound = False
        lstcollectresp = rekog.list_collections(MaxResults=max_results)
        collections = lstcollectresp['CollectionIds']
        for collection in collections:
            if (collection == COLLECT_NAME):
                print('La Collection ya Existe !')
                isCollectionFound = True

        # Si no exite la colección se crea.
        if not isCollectionFound:
            createcollresp = rekog.create_collection(CollectionId=COLLECT_NAME)
            print('Collection ARN: ' + createcollresp['CollectionArn'])
            print('Create collection status code: ' +
                  str(createcollresp['StatusCode']))

        # Indexa la nueva foto en la colección
        idxresp = rekog.index_faces(CollectionId=COLLECT_NAME,
                                    Image={'S3Object': {
                                        'Bucket': S3_BUCKET, 'Name': data["imgname"]}},
                                    ExternalImageId=data["imgname"],
                                    MaxFaces=1,
                                    QualityFilter="AUTO",
                                    DetectionAttributes=['ALL'])

        user_uuid = idxresp['FaceRecords'][0]['Face']['FaceId']

        # Guarda en la DB el registro del usuario.
        response = users_table.put_item(
            Item={
                'faceid': user_uuid,
                'name': name,
                'paths3': s3path,
                'notify': notify
            }
        )
        print("Response Dynamo: ", response)

    except Exception as e:
        msgError = "An exception occurred " + str(e) + "."
        print(msgError)
        jresp = {'Error': msgError}
        statusCode = 500

    jresp = {'data': 'New-user tasks done!'}
    print(jresp)
    return jsonify(jresp, statusCode)    
