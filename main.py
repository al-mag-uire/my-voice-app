from transcribe.record_audio import record_audio
from transcribe.transcribe_audio import upload_to_s3, start_transcription_job, check_transcription_status
from nlp.process_transcription import process_transcription
from google_calendar.calendar_actions import add_event, update_event, delete_event
import requests
from datetime import datetime

# Define your S3 bucket name if not imported from elsewhere
S3_BUCKET_NAME = "portofino777"

def download_transcription_file(url, filename="transcription.json"):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "w") as file:
            file.write(response.text)
        print(f"Downloaded transcription to {filename}")
    else:
        print("Failed to download transcription file.")
        response.raise_for_status()

def handle_action(action):
    if action["intent"] == "add_event":
        add_event(action)
    elif action["intent"] == "update_event":
        # You might need logic to locate the event ID
        event_id = "exampleEventId"  # Placeholder
        update_event(event_id, action)
    elif action["intent"] == "delete_event":
        # You might need logic to locate the event ID
        event_id = "exampleEventId"  # Placeholder
        delete_event(event_id)
    else:
        print("Unknown intent. Please try again.")


if __name__ == "__main__":
    # Generate a unique filename with a timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"audio/recording_{timestamp}.wav"

    # Record and transcribe audio
    record_audio(filename)
    upload_to_s3(filename, S3_BUCKET_NAME)
    job_name = start_transcription_job(filename)
    transcript_url = check_transcription_status(job_name)

    # Process transcription if available
    if transcript_url:
        # Download the transcription file
        download_transcription_file(transcript_url, "transcription.json")

        # Read and process transcription
        with open("transcription.json", "r") as file:
            text = file.read()  # Read transcription text
        
        action = process_transcription(text)
        handle_action(action)
