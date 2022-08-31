import requests
from requests.structures import CaseInsensitiveDict
from pprint import pprint as pp

url = "https://app.clio.com/api/v4/line_items.json"

headers = CaseInsensitiveDict()
headers["Host"] = "app.clio.com"
headers["Content-Type"] = "application/x-www-form-urlencoded"
# headers["Authorization"] = ""
headers["Cookie"] = ""

resp = requests.get(url, headers=headers, params={
    "activity_id": 3503771466,
    "fields": "id,bill,discount,activity"
})

line_items = resp.json()['data']

print(resp.status_code)

pp(line_items)