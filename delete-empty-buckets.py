import boto3

# Set up access credentials
access_key = "AKIAZKCNCMWKKZRD2KW"
secret_key = "jzB4dlyV+63D7H8NDDb7LcxbDyNsUwKdG1oSnVO"
region_name = "us-west-1"

# Create an S3 client
s3_client = boto3.client("s3", aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region_name)

# Create an S3 resource
s3 = boto3.resource("s3", aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region_name)

# List all of the S3 buckets in the account
response = s3_client.list_buckets()
buckets = response["Buckets"]

# Filter out the empty buckets with versioning disabled
empty_buckets = []
for bucket in buckets:
    bucket_name = bucket["Name"]
    result = s3_client.list_objects_v2(Bucket=bucket_name)
    if "Contents" not in result:
        # Check if versioning is enabled for the bucket
        versioning = s3_client.get_bucket_versioning(Bucket=bucket_name)
        if versioning.get("Status") != "Enabled":
            empty_buckets.append(bucket_name)

# Delete the empty buckets
for bucket_name in empty_buckets:
    s3.Bucket(bucket_name).objects.all().delete()
    s3.Bucket(bucket_name).delete()
    print(f"Bucket {bucket_name} deleted.")
