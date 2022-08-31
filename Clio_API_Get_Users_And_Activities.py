import requests
from requests.structures import CaseInsensitiveDict
from pprint import pprint as pp

def set_headers() -> CaseInsensitiveDict:

    headers = CaseInsensitiveDict()
    headers["Host"] = "app.clio.com"
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    # headers["Authorization"] = ""
    headers["Cookie"] = ""

    return headers

def get_calendar_entries(headers: CaseInsensitiveDict) -> requests.Response:

    url = "https://app.clio.com/api/v4/calendar_entries/2524822026.json"

    resp = requests.get(url, headers=headers, params={
        "fields": "id,etag,attendees,reminders,calendars,calendar_owner"
        }
    )

    print(resp.status_code)
    return resp

# Calendar Response

# pp(resp.json()['data'])
# pp(resp.json()['data']['calendar_owner'])

# for attendee in resp.json()['data']['attendees']:
#     print(attendee)

def get_users(headers: CaseInsensitiveDict) -> requests.Response:

    url = "https://app.clio.com/api/v4/users.json"

    resp = requests.get(url, headers=headers, params={
        "fields": "id,name,default_calendar_id"
        }
    )

    print(resp.status_code)
    return resp

# Users Response
# pp(users.json()['data'])

# for line in users.json()['data']:
#     print(f"{line['id']} | {line['name']} | {line['default_calendar_id']}")

def main() -> None:

    headers = set_headers()
    calendar_entries = get_calendar_entries(headers)
    users = get_users(headers)

    pp(calendar_entries.json())
    pp(users.json())

if __name__ == '__main__':
    main()