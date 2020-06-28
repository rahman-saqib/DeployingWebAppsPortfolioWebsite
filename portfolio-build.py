import json
import io
import boto3
from botocore.client import Config
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import zipfile
import mimetypes

def lambda_handler(event, context):
    s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))
    s3 = boto3.resource('s3')
        
    portfolio_bucket = s3.Bucket('portfolio.sr')
    build_bucket = s3.Bucket('portfoliobuild.sr')
        
    portfolio_zip = StringIO()
    build_bucket.download_fileobj('portfoliobuild.zip', portfolio_zip)
        
    with zipfile.ZipFile(portfolio_zip) as myzip:
        for nm in myzip.namelist():
            obj = myzip.open(nm)
            portfolio_bucket.upload_fileobj(obj, nm,
                ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
            portfolio_bucket.Object(nm).Acl().put(ACL='public-read')

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
