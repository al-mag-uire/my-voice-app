from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime, timedelta
import calendar
import re

# Ensure your credentials file path is set correctly
SERVICE_ACCOUNT_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google_account():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return credentials

def list_upcoming_events():
    service = build('calendar', 'v3', credentials=authenticate_google_account())
    now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

if __name__ == "__main__":
    list_upcoming_events()
    
def get_next_weekday_date(weekday):
    """Returns the date of the next specified weekday."""
    days_ahead = list(calendar.day_name).index(weekday) - datetime.now().weekday()
    if days_ahead <= 0:  # If today is the day or the day has passed, look for the next week
        days_ahead += 7
    return datetime.now() + timedelta(days=days_ahead)

def convert_time_to_24hr_format(time_str):
    """Converts '5 p.m.' or '11 a.m.' format to '17:00' or '11:00' (24-hour format)."""
    match = re.match(r"(\d+)\s*(a\.m\.|p\.m\.)", time_str, re.IGNORECASE)
    if match:
        hour = int(match.group(1))
        period = match.group(2).lower()
        if period == "p.m." and hour != 12:
            hour += 12
        elif period == "a.m." and hour == 12:
            hour = 0
        time_24hr = f"{hour:02}:00"
        print(f"Converted time: {time_str} to {time_24hr}")
        return time_24hr
    print(f"Failed to parse time, defaulting to 17:00: {time_str}")
    return "17:00"  # Default to 5 PM if parsing fails

def add_event(action):
    service = build('calendar', 'v3', credentials=authenticate_google_account())

    # Define the Calendar ID for the target calendar
    calendar_id = "maguire.alexander.j@gmail.com" # Use calendars email

    # Extract title, date, and time from the action dictionary
    title = action.get("title", "No Title")
    weekday = action.get("date", "Friday")  # Assuming weekday name
    time_str = action.get("time", "5 p.m.")  # Default to 5 PM if not specified

    # Convert weekday to the next specific date
    date_obj = get_next_weekday_date(weekday)
    date_str = date_obj.strftime("%Y-%m-%d")

    # Convert the time string to 24-hour format
    time_24hr = convert_time_to_24hr_format(time_str)
    event_datetime_str = f"{date_str}T{time_24hr}:00-08:00"  # Adjust timezone offset if necessary
    print(f"Event start datetime string: {event_datetime_str}")

    start_datetime = datetime.strptime(event_datetime_str, "%Y-%m-%dT%H:%M:%S%z")
    end_datetime = start_datetime + timedelta(hours=1)

    print(f"Event start: {start_datetime.isoformat()}, Event end: {end_datetime.isoformat()}")

    event = {
        'summary': title,
        'start': {
            'dateTime': start_datetime.isoformat(),
            'timeZone': 'America/Los_Angeles'  # Update for your timezone
        },
        'end': {
            'dateTime': end_datetime.isoformat(),
            'timeZone': 'America/Los_Angeles'
        }
    }

    # Insert the event into the specified calendar
    created_event = service.events().insert(calendarId=calendar_id, body=event).execute()
    print(f"Event created: {created_event.get('htmlLink')}")

def update_event(event_id, action):
    service = build('calendar', 'v3', credentials=authenticate_google_account())
    event = service.events().get(calendarId='primary', eventId=event_id).execute()

    # Update the event details
    event['summary'] = action['title']
    weekday = action.get("date", "Friday")
    date_obj = get_next_weekday_date(weekday)
    date_str = date_obj.strftime("%Y-%m-%d")

    time_str = action.get("time", "5 p.m.")
    time_24hr = convert_time_to_24hr_format(time_str)
    event_datetime_str = f"{date_str}T{time_24hr}:00-07:00"

    start_datetime = datetime.strptime(event_datetime_str, "%Y-%m-%dT%H:%M:%S%z")
    end_datetime = start_datetime + timedelta(hours=1)

    event['start']['dateTime'] = start_datetime.isoformat()
    event['end']['dateTime'] = end_datetime.isoformat()

    updated_event = service.events().update(calendarId='primary', eventId=event_id, body=event).execute()
    print(f"Event updated: {updated_event.get('htmlLink')}")

def delete_event(event_id):
    service = build('calendar', 'v3', credentials=authenticate_google_account())
    service.events().delete(calendarId='primary', eventId=event_id).execute()
    print(f"Event with ID {event_id} deleted.")
