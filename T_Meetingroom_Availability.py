# -*- coding: utf-8 -*-
import logging
import i18n
import json
from datetime import datetime, timezone, timedelta

# Libs
import libs.robin
import libs.time


def start(params):
  logging.info('Meeting Room Availability...[Start]')

  # Determine a floor
  floor = params['data']['params']['floor']
  logging.info(floor)

  # TODO
  # Use regex to extract floor
  #
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
        'client': 'slack',
        'type': 'message',
        'data': {
          'text': i18n.t('MESSAGE_FLOOR_UNRECOGNIZED')
        },
        'channel': params['channel']
    })
  logging.info(floor)

  locations = libs.robin.get_locations(floor)
  logging.info(locations)

  # No location retrieved
  if locations == []:
    return json.dumps({
        'client': 'slack',
        'type': 'message',
        'data': {
          'text': i18n.t('MESSAGE_FLOOR_UNRECOGNIZED')
        },
        'channel': params['channel']
    })

  floors = []
  for location in locations:
    floors.append(location['id'])

  logging.info(floors)

  rooms_15 = get_free_rooms(floors, 15)
  rooms_30 = get_free_rooms(floors, 30)
  rooms_60 = get_free_rooms(floors, 60)

  logging.info(rooms_15)
  logging.info(rooms_30)
  logging.info(rooms_60)

  # Remove duplicates
  for room_60 in rooms_60:
    for room_15 in rooms_15:
      if room_60['name'] == room_15['name']:
        rooms_15.remove(room_15)
    for room_30 in rooms_30:
      if room_60['name'] == room_30['name']:
        rooms_30.remove(room_30)

  # Remove duplicates
  for room_30 in rooms_30:
    for room_15 in rooms_15:
      if room_30['name'] == room_15['name']:
        rooms_15.remove(room_15)

  text_15 = ''
  for room in rooms_15:
    text_15 += i18n.t('MESSAGE_MEETINGROOM_AVAILABILITY_FORMAT',
                      name=room['name'], capacity=room['capacity'])

  text_30 = ''
  for room in rooms_30:
    text_30 += i18n.t('MESSAGE_MEETINGROOM_AVAILABILITY_FORMAT',
                      name=room['name'], capacity=room['capacity'])

  text_60 = ''
  for room in rooms_60:
    text_60 += i18n.t('MESSAGE_MEETINGROOM_AVAILABILITY_FORMAT',
                      name=room['name'], capacity=room['capacity'])

  return json.dumps({
      'client': 'slack',
      'type': 'message',
      'data': {
        'text': i18n.t(
        'MESSAGE_MEETINGROOM_AVAILABILITY',
        floor=floor,
        text_15=text_15,
        text_30=text_30,
        text_60=text_60)
      },
      'channel': params['channel']
  })

def get_free_rooms(floors, minutes):
  free_rooms = []

  now = datetime.now(libs.time.JST)

  start = now.strftime(
      '%Y-%m-%dT%H:%M:%S' +
      libs.time.TIMEZONE_TIME)
  end = (now + timedelta(minutes=minutes)).strftime(
      '%Y-%m-%dT%H:%M:%S' +
      libs.time.TIMEZONE_TIME)

  spaces = libs.robin.get_free_spaces(floors, start, end)
  logging.info(spaces)
  for space in spaces:
    if space['busy'] == []:
      # free_rooms.insert(len(free_rooms) - 1, space['space']['name'] + ' ' + space['space']['capacity']+'人')
      # free_rooms.append(space['space']['name'] + '(' + str(space['space']['capacity']) + '人)')
      free_rooms.append({
          'name': space['space']['name'],
          'capacity': space['space']['capacity']
      })

  return free_rooms
