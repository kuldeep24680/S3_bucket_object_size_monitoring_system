# S3_bucket_object_size_monitoring_system
This solution uses AWS lambda function and dynamodb table to monitor and notify the bucket owner about the bucket size for particular s3 bucket, to avoid the unnecessary costing

Dynamodb Table::
Here, I am using dynamodb table "S3_object_size" that contains the details given below:
1. bucket --> Name of the S3 bucket whose total object size you want to monitor
2. email_id --> Email ID of the bucket owner, to whom code will send the mail notifying about the bucket-size.
3. owner --> Name of the bucket owner
4. size_threshold_in_GB --> threshold size limit (in GBs) of bucket, which if crossed, the owner gets notified
5. trail number is to keep a track of notification sent to the user.


AWS Lambda function::
This lambda function will first hit the dynamodb table mentioned above and scans it. Then it stores all those information and Once all the parameters are collected, it executes a function that can calculate the total object-size of those buckets and check if the any of those bucket object size is crossing the threshold value and if that is so, the lambda function prompts an customized email to bucket owner, notifying about the bucket size. As a user is sent an email, lambda function updates and increases the value of trial_number to keep a track of emails sent to the user.
Lambda function is triggered through cloudwatch events that acts as an scheduler which is triggered I every 20 minutes.


