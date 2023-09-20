import boto3

# Replace with your AWS access key and secret access key
ACCESS_KEY = "AKIAZKCNCMWKKZRD2KW"
SECRET_KEY = "jzB4dlyV+63D7H8NDDb7LcxbDyNsUwKdG1oSnVO"

# Replace with your AWS region and S3 bucket name
REGION = "us-west-1"
BUCKET_NAME = "transcribe-bucket-111"

# Replace with the name of the input video file in your S3 bucket
VIDEO_FILE_NAME = "Ganesh_song.mp4"

# Replace with the name of the output transcript file in your S3 bucket
TRANSCRIPT_FILE_NAME = 'transcribed'

# Create a Transcribe client
transcribe_client = boto3.client('transcribe', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name=REGION)

# Start the transcription job
transcription_job = transcribe_client.start_transcription_job(
    TranscriptionJobName='transcription_job_name',
    Media={'MediaFileUri': f's3://{BUCKET_NAME}/{VIDEO_FILE_NAME}'},
    MediaFormat='mp4',
    LanguageCode='en-US',
    OutputBucketName=BUCKET_NAME,
    OutputKey=TRANSCRIPT_FILE_NAME
)

# Wait for the transcription job to complete
while True:
    job = transcribe_client.get_transcription_job(TranscriptionJobName=transcription_job['TranscriptionJob']['TranscriptionJobName'])
    if job['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
        break

# Print the transcription job status and output URL
print(job['TranscriptionJob']['TranscriptionJobStatus'])
print(job['TranscriptionJob']['Transcript']['TranscriptFileUri'])