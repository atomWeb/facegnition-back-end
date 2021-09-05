import os
import boto3
from boto3.dynamodb.conditions import Key

REGION = os.environ["REGION"]
USERS_TABLE = os.environ["USERS_TABLE"]
TOPIC_ARN = os.environ["TOPIC_ARN"]

dynamo_resource = boto3.resource("dynamodb", region_name=REGION)
users_table = dynamo_resource.Table(USERS_TABLE)
sns_client = boto3.client('sns', region_name=REGION)

def notify(event, context):
    print(event)
    try:

            faceid = event["Records"][0]["dynamodb"]["Keys"]["faceid"]["S"]
            fecha = event["Records"][0]["dynamodb"]["Keys"]["timest"]["S"]

            usrs_resp = users_table.query(
                KeyConditionExpression=Key("faceid").eq(faceid),
                Limit=1
            )
            print(usrs_resp['Items'][0])
            notify = usrs_resp['Items'][0]["notify"]
            name = usrs_resp['Items'][0]["name"]
            face_id = usrs_resp['Items'][0]["faceid"]

            if notify:
                sns_client.publish(
                    TopicArn=TOPIC_ARN,
                    Subject=f'Usuario {name} validado',
                    Message=f'El usuario {name} - {face_id} ha sido validado a fecha de: {fecha}'
                )

    except Exception as e:
        msgError = "An exception occurred " + str(e) + "."
        print(msgError)

    print("Ejecución finalizada")
