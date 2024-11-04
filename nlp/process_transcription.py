import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from nlp.intent_classification import classify_intent
from nlp.entity_extraction import extract_entities

def process_transcription(json_text):
    # Parse the JSON response to extract the transcription text
    data = json.loads(json_text)
    text = data["results"]["transcripts"][0]["transcript"]
    
    print(f"Processing transcription text: {text}")  # Debug print
    intent = classify_intent(text)
    entities = extract_entities(text)
    
    print(f"Detected intent: {intent}")  # Debug print
    print(f"Extracted entities: {entities}")  # Debug print

    action = {
        "intent": intent,
        "title": entities["title"],
        "date": entities["date"],
        "time": entities["time"],
    }
    
    return action

if __name__ == "__main__":
    # Test cases to verify the intent classification and entity extraction
    test_texts = [
        '{"results": {"transcripts": [{"transcript": "Add a meeting with John on Friday at 3 PM"}]}}',
        '{"results": {"transcripts": [{"transcript": "Cancel the meeting with Sarah"}]}}',
        '{"results": {"transcripts": [{"transcript": "Change my appointment to next Monday at noon"}]}}'
    ]
    
    for json_text in test_texts:
        action = process_transcription(json_text)
        print(f"Processed JSON: {json_text} -> Action: {action}")

# Example usage:
# json_text = '{"results": {"transcripts": [{"transcript": "Add a meeting with John on Friday at 3 PM"}]}}'
# action = process_transcription(json_text)
# print("Action:", action)
