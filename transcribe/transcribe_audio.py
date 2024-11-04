import sys
import os
import time
import boto3
import json
import requests

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from transcribe.config import AWS_REGION, S3_BUCKET_NAME

def upload_to_s3(filename, bucket_name):
    s3 = boto3.client('s3', region_name=AWS_REGION)
    s3.upload_file(filename, bucket_name, filename.split('/')[-1])
    print(f"Uploaded {filename} to S3 bucket {bucket_name}.")

def start_transcription_job(filename):
    transcribe = boto3.client('transcribe', region_name=AWS_REGION)
    job_name = f"transcription-job-{int(time.time())}"
    job_uri = f"s3://{S3_BUCKET_NAME}/{filename.split('/')[-1]}"

    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='wav',
        LanguageCode='en-US'
    )
    
    print(f"Started transcription job {job_name}")
    return job_name

def check_transcription_status(job_name):
    transcribe = boto3.client('transcribe', region_name=AWS_REGION)
    while True:
        result = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        status = result['TranscriptionJob']['TranscriptionJobStatus']
        if status == 'COMPLETED':
            transcript_url = result['TranscriptionJob']['Transcript']['TranscriptFileUri']
            print(f"Transcription completed. Transcript URL: {transcript_url}")
            return transcript_url
        elif status == 'FAILED':
            print("Transcription job failed.")
            return None
        print("Waiting for transcription...")
        time.sleep(5)

def download_transcription_file(transcript_url, local_filename="transcription.json"):
    # Download the transcription file using the pre-signed URL
    response = requests.get(transcript_url)
    if response.status_code == 200:
        with open(local_filename, "wb") as file:
            file.write(response.content)
        print(f"Transcription saved to {local_filename}")
        
        # Optional: Load and print the transcription content
        with open(local_filename, "r") as file:
            transcription_data = json.load(file)
            print(transcription_data)
    else:
        print(f"Failed to download the transcription file. Status code: {response.status_code}")

# Usage
if __name__ == "__main__":
    filename = "audio/recording.wav"  # Make sure this file exists
    
    # Step 1: Upload audio file to S3
    upload_to_s3(filename, S3_BUCKET_NAME)
    
    # Step 2: Start transcription job
    job_name = start_transcription_job(filename)
    
    # Step 3: Check transcription status and get the transcription URL
    transcript_url = check_transcription_status(job_name)
    
    # Step 4: Download the transcription file if available
    if transcript_url:
        download_transcription_file(transcript_url)
