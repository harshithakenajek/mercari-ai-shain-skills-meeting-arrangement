import os
import logging
import i18n
import json

import T_Meetingroom_Availability
import T_Meetingroom_Booking
import T_Meetingroom_Location

# Const Vars
INTENT_MEETINGROOM_AVAILABILITY = 'T_Meetingroom - Availability'
INTENT_MEETINGROOM_BOOKING = 'T_Meetingroom - Booking'
INTENT_MEETINGROOM_LOCATION = 'T_Meetingroom - Location'

# Logging
logging.getLogger().setLevel(logging.INFO)

# i18n Configuration
base_path = os.path.dirname(os.path.abspath(__file__))
i18n.load_path.append(os.path.join(base_path, './locales'))
i18n.set('filename_format', '{locale}.{format}')
i18n.set('file_format', 'yaml')
i18n.set('skip_locale_root_data', True)

# Entry point
def main(request):
  logging.info('========[START]========')

  if not request.method == 'POST':
    return 'Service is Up and Running....'

  # Request parameters
  payload = request.get_data()
  params = json.loads(payload)
  logging.info(params)

  # Locale setting
  i18n.set('locale', params['data']['lang'])

  # Availability
  if 'intent' in params['data'] and params['data']['intent'] == INTENT_MEETINGROOM_AVAILABILITY:
    return T_Meetingroom_Availability.start(params)
  # Booking
  elif 'intent' in params['data'] and params['data']['intent'] == INTENT_MEETINGROOM_BOOKING:
    return T_Meetingroom_Booking.start(params)
  # Location
  elif 'intent' in params['data'] and params['data']['intent'] == INTENT_MEETINGROOM_LOCATION:
    return T_Meetingroom_Location.start(params)
  else:
    logging.info('Nothing to do....')
  
  return json.dumps({})
