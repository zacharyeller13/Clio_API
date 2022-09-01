import requests
from requests.structures import CaseInsensitiveDict
import csv

from pprint import pprint as pp
import time

def set_headers() -> CaseInsensitiveDict:
    """Sets and returns request headers necessary for Clio endpoints"""

    headers = CaseInsensitiveDict()
    headers["Host"] = "app.clio.com"
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    headers["Authorization"] = ""
    #headers["Cookie"] = ""

    return headers

def get_calendar_entries(url: str, headers: CaseInsensitiveDict) -> list[dict]:
    """
    Sends get request to /calendar_entries.json endpoint and returns the JSON of all entries.
    Navigates paginated results if response includes a 'next' url.
    """
    # calendar_entries/####.json for specific entry
    # e.g. 2524822026

    # base url
    # url = "https://app.clio.com/api/v4/calendar_entries.json"

    entries = []

    resp = requests.get(url, headers=headers, params={
        "fields": "id,attendees,calendar_owner",
        "order" : "id(asc)"
        }
    )

    print(resp.status_code)
    entries.extend(resp.json()['data'])

    while resp.json()['meta']['paging'].get('next'):
        
        url = resp.json()['meta']['paging'].get('next')
        print(f"Requesting: {url}")
        resp = requests.get(url, headers=headers)
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
    """Parses JSON response of calendar entries and returns a list of dicts for future processing"""
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

    with open(csv_file, 'w', newline="") as csvfile:
        fieldnames = attendees[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(attendees)

def get_csv_filepath() -> str:
    csv_file = input("Please enter the fully-qualified (absolute) path to the CSV file for this data: ")

    return csv_file

def main() -> None:

    headers = set_headers()
    csv_file = get_csv_filepath()

    base_calendar_url = "https://app.clio.com/api/v4/calendar_entries.json"

    calendar_entries = get_calendar_entries(base_calendar_url, headers)
    attendees = parse_calendar_entries(calendar_entries)

    write_csv(attendees, csv_file)

if __name__ == "__main__":
    main()