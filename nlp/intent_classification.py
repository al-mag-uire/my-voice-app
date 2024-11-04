import spacy

# Load the spaCy English model
nlp = spacy.load("en_core_web_sm")

def classify_intent(text):
    text = text.lower()
    if "add" in text or "schedule" in text or "set up" in text or "create" in text:
        return "add_event"
    elif "update" in text or "change" in text or "reschedule" in text:
        return "update_event"
    elif "delete" in text or "cancel" in text:
        return "delete_event"
    else:
        return "unknown"



if __name__ == "__main__":
    test_texts = [
        "Add a meeting with John on Friday at 3 PM",
        "Delete the meeting with Sarah",
        "Update my appointment to next Monday"
    ]
    
    for text in test_texts:
        intent = classify_intent(text)
        print(f"Text: {text} -> Intent: {intent}")



# Example usage:
# text = "Add a meeting with John on Friday at 3 PM"
# intent = classify_intent(text)
# print("Intent:", intent)
