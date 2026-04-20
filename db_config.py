import json
import boto3

SECRET_NAME = "${EnvironmentName}/mysql/credentials"
DB_HOST     = "${MySQLInstance.Endpoint.Address}"
REGION      = "${AWS::Region}"

def get_db_credentials():
    """
    Retrieve DB credentials from Secrets Manager.
    Returns a dict: username, password, engine, port, dbname, host.
    """
    client = boto3.client("secretsmanager", region_name=REGION)
    response = client.get_secret_value(SecretId=SECRET_NAME)
    secret = json.loads(response["SecretString"])
    secret["host"] = DB_HOST
    return secret    