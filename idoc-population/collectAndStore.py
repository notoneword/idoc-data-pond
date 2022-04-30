import json    
import re
import urllib.request as req
import urllib
import boto3
import os
import uuid

# separate file for all the config values, magic strings?
base = 'https://www2.illinois.gov'
reports_folder = '/idoc/reportsandstatistics/'
base_folder = base + reports_folder

docs = 'Documents/'
pages = 'Pages/'
page = 'Prison-Population-Data-Sets.aspx'
url = (base_folder + pages + page)

bucket = 'cj-data-puddle'
raw_folder = 'idoc-population-data/raw/'

tmp_dir = '/tmp/'

def lambda_handler(event, context):

    try:
        page_source = req.urlopen(url).read().decode('utf-8')
        regex_pattern = '<a href="' + reports_folder + docs + '(.*?)"'

        doc_links = re.findall(regex_pattern, page_source)
        for doc_link in doc_links:
            #Process the data from the page here.
            clean_name = urllib.parse.unquote(doc_link)  
            print('clean_name: ' + clean_name)
            doc_url = (base_folder + docs + doc_link)
            print('doc_url = ' + doc_url)
            req.urlretrieve(doc_url, (tmp_dir + clean_name))
            upload_file(clean_name)
                
        
        os.chdir(tmp_dir)
        print('files in ' + os.getcwd() + ':' + str(os.listdir()))
        print('size of ' + files[0] + ':' + str(os.stat(tmp_dir + files[0]).st_size))

            
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
            }
    
    return {
       'statusCode': 200,
       'body': json.dumps('Hello from TRC!')
    }
    
def upload_file(file):
    # Upload to S3 with the put_object call
    client = boto3.client('s3', region_name='us-east-1')

    try:
       file_obj = open(tmp_dir + file, 'rb')
       # key name: full path within your bucket to the object.
       s3keyname = raw_folder + file
       # Specify the MIME type manually -- S3 does not guess that for you unless you use the web UI
       # and this should be specified if you need S3 to serve it as content.
       contenttype = 'application/xls'
       #print('P: ' + s3keyname)
       #print('P: ' + bucket)
       uploadfile = client.put_object(
            Bucket=bucket,
            Body=file_obj,
            Key=s3keyname,
            ContentType=contenttype,
            # IMPORTANT -- the ACL setting determines the security settings for your object
            # This can be 'public-read', 'private' or specified to other IAM targets.
            ACL='public-read'
        )
    except Exception as e:
        print('There has been an error in uploading the document to S3: '  + str(e))
    
