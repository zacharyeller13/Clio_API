from Clio_API_Get_Users_And_Activities import parse_calendar_entries

# Test attendees list
attendees = [{'attendees': [],
  'calendar_owner': {'etag': '"2d72eb630fcf396a68f6d0d2c3633492"',
                     'id': 2978539,
                     'permission': 'editor'},
  'id': '1750624234'},
 {'attendees': [
        {'id': 3, 'type': 'Calendar'},
        {'id': 4, 'type': 'Calendar'},
        {'id': 5, 'type': 'Calendar'}
    ],
  'calendar_owner': {'etag': '"2d72eb630fcf396a68f6d0d2c3633492"',
                     'id': 2978539,
                     'permission': 'editor'},
  'id': '1750624264'}]

def test_parse_calendar_entries():
    assert parse_calendar_entries(attendees) == [
        {'attendee_id': 3, 'attendee_type': 'Calendar', 'calendar_owner_id': 2978539, 'activity_id': '1750624264'}, 
        {'attendee_id': 4, 'attendee_type': 'Calendar', 'calendar_owner_id': 2978539, 'activity_id': '1750624264'}, 
        {'attendee_id': 5, 'attendee_type': 'Calendar', 'calendar_owner_id': 2978539, 'activity_id': '1750624264'}
    ]