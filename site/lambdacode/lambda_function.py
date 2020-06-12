import boto3
import json
import requests
from requests_aws4auth import AWS4Auth

region = 'us-east-1'
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

host = 'search-localization-of-bug-p6axgikx4z4jnqiywdpafqce6m.us-east-1.es.amazonaws.com' # For example, search-mydomain-id.us-west-1.es.amazonaws.com
index = 'test1'
url = 'https://' + host + '/' + index + '/_search'

# Lambda execution starts here
def handler(event, context):

    # Put the user query into the query DSL for more accurate search results.
    # Note that certain fields are boosted (^).
    query = {
        "size": 0, 
  "query": {
        "function_score": {
            "query": {
              "multi_match" : {
              "query": event['queryStringParameters']['q'],
              "fields": ["file_name^4", "entities^2", "commit_msg", "diff_file"],
              }
            },
            "functions": [
              {
                "exp": {
                "file_date": {
                      "scale": "10d",
                      "offset": "2d", 
                      "decay" : 0.6
                    }
                  },
                  "weight": 1
                }
              ],
              "boost_mode": "multiply"
          }
    },
  "aggs": {
    "combine_commit": {
      "terms": {
        "field": "commit_id",
        "order": {
          "top_hit": "desc"
        }
      },
      "aggs": {
        "top_commits": {
          "top_hits": {
            "_source": {
              "includes": ["package_link","commit_msg","file_date"]
            },
            "size": 1
          }
        },
        "top_hit":{
          "max": {
            "script":{
              "source": "_score"
            }
          }
        }
      }
    }
  }
}

    # ES 6.x requires an explicit Content-Type header
    headers = { "Content-Type": "application/json" }

    # Make the signed HTTP request
    r = requests.get(url, auth=awsauth, headers=headers, data=json.dumps(query))

    # Create the response and add some extra content to support CORS
    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": '*'
        },
        "isBase64Encoded": False
    }

    # Add the search results to the response
    response['body'] = r.text
    return response
