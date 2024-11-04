import spacy

nlp = spacy.load("en_core_web_sm")

def extract_entities(text):
    doc = nlp(text)
    entities = {"title": None, "date": None, "time": None}

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            entities["title"] = f"Meeting with {ent.text}"
        elif ent.label_ == "DATE":
            entities["date"] = ent.text
        elif ent.label_ == "TIME":
            entities["time"] = ent.text

    return entities


if __name__ == "__main__":
    test_texts = [
        "Add a meeting with John on Friday at 3 PM",
        "Schedule a call with Lisa tomorrow",
        "Reschedule dinner with Bob to Saturday evening"
    ]
    
    for text in test_texts:
        entities = extract_entities(text)
        print(f"Text: {text} -> Entities: {entities}")



# Example usage:
# text = "Add a meeting with John on Friday at 3 PM"
# extracted_entities = extract_entities(text)
# print("Extracted Entities:", extracted_entities)
