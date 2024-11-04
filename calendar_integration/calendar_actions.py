def add_event(action):
    print(f"Adding event: {action['title']} on {action['date']} at {action['time']}")

def update_event(action):
    print(f"Updating event: {action['title']} to {action['date']} at {action['time']}")

def delete_event(action):
    print(f"Deleting event: {action['title']}")


if __name__ == "__main__":
    actions = [
        {"intent": "add_event", "title": "Meeting with John", "date": "Friday", "time": "3 PM"},
        {"intent": "update_event", "title": "Appointment with Dr. Smith", "date": "Monday", "time": "noon"},
        {"intent": "delete_event", "title": "Lunch with Sarah"}
    ]
    
    for action in actions:
        if action["intent"] == "add_event":
            add_event(action)
        elif action["intent"] == "update_event":
            update_event(action)
        elif action["intent"] == "delete_event":
            delete_event(action)
        else:
            print("Unknown intent")

