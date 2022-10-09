import requests
from requests.structures import CaseInsensitiveDict
from requests_oauthlib import OAuth2Session
import os
import csv
import time

from get_authorization import Config, Clio

def get_users(url: str, session: OAuth2Session) -> list[dict]:
    """
    Sends get request to /users.json endpoint and returns JSON of all entries.
    Navigates paginated results if response includes a 'next' url.
    """

    # base url
    # url = "https://app.clio.com/api/v4/users.json"

    users = []

    resp = session.get(url, params={
        "fields": "id,name,default_calendar_id",
        "order": "id(asc)"
    })

    print(resp.status_code)
    users.extend(resp.json()['data'])

    while resp.json()['meta']['paging'].get('next'):
        
        url = resp.json()['meta']['paging'].get('next')
        print(f"Requesting: {url}")
        resp = session.get(url)
        print(resp.status_code)
        print(f"X-RateLimit-Remaining: {resp.headers['X-RateLimit-Remaining']}")

        if resp.headers.get('Retry-After'):
            retry_period = int(resp.headers.get('Retry-After'))
            print(f"Retry-After: {retry_period}")

            for i in range(retry_period+1):
                print(i, end='\r', flush=True)
                time.sleep(1)

        else:
            users.extend(resp.json()['data'])

    return users

def get_calendar_entries(url: str, session: OAuth2Session) -> list[dict]:
    """
    Sends get request to /calendar_entries.json endpoint and returns the JSON of all entries.
    Navigates paginated results if response includes a 'next' url.
    """
    # calendar_entries/####.json for specific entry
    # e.g. 2524822026

    # base url
    # url = "https://app.clio.com/api/v4/calendar_entries.json"

    entries = []

    resp = session.get(url, params={
        "fields": "id,attendees,calendar_owner",
        "order" : "id(asc)"
    })

    print(resp.status_code)
    entries.extend(resp.json()['data'])

    while resp.json()['meta']['paging'].get('next'):
        
        url = resp.json()['meta']['paging'].get('next')
        print(f"Requesting: {url}")
        resp = session.get(url)
        print(resp.status_code)
        print(f"X-RateLimit-Remaining: {resp.headers['X-RateLimit-Remaining']}")

        if resp.headers.get('Retry-After'):
            retry_period = int(resp.headers.get('Retry-After'))
            print(f"Retry-After: {retry_period}")

            for i in range(retry_period+1):
                print(i, end='\r', flush=True)
                time.sleep(1)

        else:
            entries.extend(resp.json()['data'])

    return entries

def parse_calendar_entries(entries: list[dict]) -> list[dict]:
    """
    Parses JSON response of calendar entries and returns a list of dicts for future processing
    """
    attendees = []

    for entry in entries:
        attendees.extend(
            [{
                'attendee_id': entry['attendees'][i]['id'],
                'attendee_type': entry['attendees'][i]['type'],
                'calendar_owner_id': entry['calendar_owner']['id'],
                'activity_id': entry['id']
            }
            for i in range(len(entry['attendees']))]
        )

    return attendees

def write_csv(attendees: list[dict], csv_file: str) -> None:
    """
    Takes a list of dicts and writes specified fields from each dict to a CSV
    """

    with open(csv_file, 'w', newline="") as csvfile:
        fieldnames = attendees[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(attendees)

def get_csv_filepath(endpoint: str) -> str:
    """
    Takes the name of an endpoint and prompts user for absolute filepath to the desired CSV file for that endpoint
    Returns the filepath as a string for use in csv.writer functions
    """
    csv_file = input(
        f"Please enter the fully-qualified (absolute) path to the CSV file for data from endpoint {endpoint}: "
    )

    return csv_file

def main() -> None:

    # client_id and client_secret should be in config.ini; create Config object to read in
    curpath = os.path.dirname(os.path.realpath(__file__))
    config_file = os.path.join(curpath, "config.ini")
    config = Config("config.ini")

    # Create new Clio(OAuth2Session) object 
    session = Clio(config.client_id)
    print(f"Please go to {session.authorization_url(session.auth_url)[0]} and authorize access")
    authorization_response = input("Enter the full callback URL: ")
    session.fetch_token(
        session.token_url,
        authorization_response=authorization_response,
        client_secret=config.client_secret,
        include_client_id=True
    )

    # Get CSV file paths
    calendar_csv_file = get_csv_filepath("/calendar_entries.json")
    users_csv_file = get_csv_filepath("/users.json")

    base_calendar_url = "https://app.clio.com/api/v4/calendar_entries.json"
    base_users_url = "https://app.clio.com/api/v4/users.json"

    # Get and parse calendar entries
    calendar_entries = get_calendar_entries(base_calendar_url, session)
    attendees = parse_calendar_entries(calendar_entries)

    # Get users
    users = get_users(base_users_url, session)

    # Write CSV files
    write_csv(attendees, calendar_csv_file)
    write_csv(users, users_csv_file)

if __name__ == "__main__":
    main()