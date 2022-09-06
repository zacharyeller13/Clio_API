def parse_calendar_entries(entries: list[dict]) -> list[dict]:
    """Parses JSON response of calendar entries and returns a list of dicts for future processing"""
    attendees = []

    for entry in entries:
        attendees.extend(
            [{
                'attendees': entry['attendees'][i],
                'calendar_owner_id': entry['calendar_owner']['id'],
                'activity_id': entry['id']
            }
            for i in range(len(entry['attendees']))]
        )

    return attendees

attendees = [{'attendees': [],
  'calendar_owner': {'etag': '"2d72eb630fcf396a68f6d0d2c3633492"',
                     'id': 2978539,
                     'permission': 'editor'},
  'id': '1750624234'},
 {'attendees': [3, 4, 5],
  'calendar_owner': {'etag': '"2d72eb630fcf396a68f6d0d2c3633492"',
                     'id': 2978539,
                     'permission': 'editor'},
  'id': '1750624264'}]

def test_parse_calendar_entries():
    assert parse_calendar_entries(attendees) == [
        {'attendees': 3, 'calendar_owner_id': 2978539, 'activity_id': '1750624264'}, 
        {'attendees': 4, 'calendar_owner_id': 2978539, 'activity_id': '1750624264'}, 
        {'attendees': 5, 'calendar_owner_id': 2978539, 'activity_id': '1750624264'}
    ]