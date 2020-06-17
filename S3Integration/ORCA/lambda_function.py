from __future__ import print_function
from pprint import pprint
import boto3
import json
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import urllib
import urllib3
import json
import logging
es = Elasticsearch()
awsRegion = "us-east-1"
service = "es"
logger = logging.getLogger()
logger.setLevel(logging.INFO)
s3 = boto3.client('s3')
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth( credentials.access_key, 
                        credentials.secret_key, 
                        awsRegion, 
                        service, 
                        session_token=credentials.token
                    )

logger.info('Loading function')

def connectES(esEndPoint):
    print ('Connecting to the ES Endpoint {0}'.format(esEndPoint))
    try:
        esClient = Elasticsearch(
            hosts=[{'host': esEndPoint, 'port': 443}],
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection)
        return esClient
    except Exception as E:
        print("Unable to connect to {0}".format(esEndPoint))
        print(E)
        exit(3)


def indexDocElement(esClient,key,response):
    try:
     	indexmetadata = response['Body'].read().decode("utf-8")
     	print(indexmetadata)
     	retval = esClient.index(index='orca', doc_type='_bulk', body=indexmetadata)
    except Exception as E:
    	print("Document not indexed")
    	print("Error: ",E)
    	exit(5)	
	  


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    esClient = connectES("Elasticsearch-domain.us-east-1.es.amazonaws.com")
    # createIndex(esClient)

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    # key = urllib.parse(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        indexDocElement(esClient,key,response)
        return response['ContentType']
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
