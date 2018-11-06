import boto3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
dynamodb = boto3.resource('dynamodb',
                          region_name='eu-central-1'
)
table = dynamodb.Table('S3_caspian_object_size')


def Notification(mail_id,threshold,bucket_name,size_in_gbs):
    msg = MIMEMultipart()
 
 
    message = 'Total Object size in '+ str(bucket_name) +' has exceeded the limit of 60GB and currently is '+str(size_in_gbs)+'GB. Do not respond to this automated email and Please contact the Administrator for more details. \n\n \n Regards,\n Caspian Support'
 
    # setup the parameters of the message
    password = "<email id passowrd>"
    msg['From'] = "<email ID>"
    msg['To'] = mail_id
    msg['Subject'] = "Objectsize Notification Alert"
 
    # add in the message body
    msg.attach(MIMEText(message, 'plain'))
 
    #create server
    server = smtplib.SMTP('smtp-mail.outlook.com: 587')
 
    server.starttls()
 
    # Login Credentials for sending the mail
    server.login(msg['From'], password)
 
 
    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())
 
    server.quit()
 
    print("successfully sent email to %s:" % (msg['To']))

def bucketSize(bucket_name,threshold,mail_id,trial_number):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    size = sum(k.size for k in bucket.objects.all())
    size_in_gbs=size/1024/1024/1024
    counter=int(trial_number)+1
    if size_in_gbs>int(threshold) and  counter!=4:
        Notification(mail_id,threshold,bucket_name,size_in_gbs)
        table.update_item(
        Key={
            'bucket': bucket_name
        },
        UpdateExpression='SET trial_number = :val1',
        ExpressionAttributeValues={
            ':val1': str(counter)
        }
        )
        print("email is successfully sent")
    else:
        print("threshold for "+str(bucket_name)+" is not crossed")

def lambda_handler(event, context):
    response = table.scan()
    dict={}
    data = response['Items']
    print(data)
    for entry in data:
        name = entry.pop('bucket') #remove and return the name field to use as a key
        dict[name] = entry
    print(dict)
    for k, v in dict.items():
        bucket=k
        mail_id=v['email_id']
        trial_number=v['trial_number'
        threshold=v['size_threshold_in_GB']
        bucketSize(bucket,threshold,mail_id,trial_number)
        
