# -*- coding: utf-8 -*-
import os
import logging
import i18n
import json
from datetime import datetime, timezone, timedelta
import slack

# Libs
import libs.robin
import libs.time

# Env vars
SLACK_BOT_USER_TOKEN = os.environ.get('SLACK_BOT_USER_TOKEN')
SLACK_SUPPORT_CHANNEL = os.environ.get('SLACK_SUPPORT_CHANNEL')

# Slack client
slack_client = slack.WebClient(token=SLACK_BOT_USER_TOKEN)

def get_start_time():
  now = datetime.now(libs.time.JST)
  start = now.strftime('%Y-%m-%dT%H:%M:%S' + libs.time.TIMEZONE_TIME)
  return start


def get_end_time(duration_min):
  now = datetime.now(libs.time.JST)
  end = (now + timedelta(minutes=duration_min)
         ).strftime('%Y-%m-%dT%H:%M:%S' + libs.time.TIMEZONE_TIME)
  return end


def start(params):
  logging.info('Meeting Room Booking...[Start]')

  # receive the parameters from dialogflow
  floor = params['params']['floor']
  duration = params['params']['duration']
  capacity = params['params']['capacity']

  logging.info(floor)
  logging.info(duration)
  logging.info(capacity)

  if duration['unit'] == '分' or duration['unit'] == 'min':
    duration_min = duration['amount']
  elif duration['unit'] == '時' or duration['unit'] == 'hour':
    duration_min = duration['amount'] * 60
  elif duration['unit'] == '日' or duration['unit'] == 'day':
    duration_min = duration['amount'] * 60 * 24
  else:
    return json.dumps({
        'slack': True,
        'type': 'message',
        'message': i18n.t('MESSAGE_DURATION_UNIT_NOT_SUPPORTED'),
        'channel': params['channel']['id']
    })

  start = get_start_time()
  end = get_end_time(duration_min)

  if floor == '15F':
    floor = '15'
  elif floor == '18F':
    floor = '18'
  elif floor == '21F':
    floor = '21'
  elif floor == '25F':
    floor = '25'
  elif floor == '43F':
    floor = '43'
  else:
    return json.dumps({
        'slack': True,
        'type': 'message',
        'message': i18n.t('MESSAGE_FLOOR_UNRECOGNIZED'),
        'channel': params['channel']['id']
    })
  logging.info(floor)

  locations = libs.robin.get_locations(floor)
  logging.info(locations)

  # No location retrieved
  if locations == []:
    return json.dumps({
        'slack': True,
        'type': 'message',
        'message': i18n.t('MESSAGE_FLOOR_UNRECOGNIZED'),
        'channel': params['channel']['id']
    })

  floors = []
  for location in locations:
    floors.append(location['id'])
  logging.info(floors)

  space = libs.robin.get_free_space(floors, start, end, capacity)
  logging.info(space)

  # No available meeting room
  if space == {}:
    return json.dumps({
        'slack': True,
        'type': 'message',
        'message': i18n.t('MESSAGE_NO_MEETINGROOM_AVAILABLE'),
        'channel': params['channel']['id']
    })

  # Extract an email address to send the generated template
  try:
    user_data = slack_client.users_info(
        user=params['user']['id']
    )
    user_name = user_data['user']['name']
    email = user_data['user']['profile']['email']
  except BaseException:
    return json.dumps({
        'slack': True,
        'type': 'message',
        'message': i18n.t(
            'MESSAGE_TEMPLATE_NO_SLACK_ACCOUNT',
            channel=SLACK_SUPPORT_CHANNEL
        ),
        'channel': params['channel']['id'],
    })

  # Book a meeting room
  try:
    meeting = libs.robin.book_space(
        space['space']['id'],
        start,
        end,
        user_name,
        email)
    logging.info(meeting)
    return json.dumps({
        'slack': True,
        'type': 'message',
        'message': i18n.t(
            'MESSAGE_MEETING_BOOKING',
            space=space['space']['name']),
        'channel': params['channel']['id']
    })
  except BaseException:
    return json.dumps({
        'slack': True,
        'type': 'message',
        'message': i18n.t('MESSAGE_FLOOR_UNRECOGNIZED'),
        'channel': params['channel']['id']
    })
