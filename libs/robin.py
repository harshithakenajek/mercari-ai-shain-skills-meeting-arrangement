import os
import logging
import requests
import json

# Libs
import libs.time

# Env vars
ROBIN_API_ORG_NAME = os.environ.get('ROBIN_API_ORG_NAME')
ROBIN_ACCESS_TOKEN = os.environ.get('ROBIN_ACCESS_TOKEN')

logging.info(ROBIN_API_ORG_NAME)
logging.info(ROBIN_ACCESS_TOKEN)

# Constant vars
SPACE_API = 'https://api.robinpowered.com/v1.0/free-busy/spaces'
LOCATION_API = 'https://api.robinpowered.com/v1.0/organizations/{}/locations'
BOOK_ROOM_API = 'https://api.robinpowered.com/v1.0/spaces/{}/events'
MEETING_TITLE = 'Meeting booked for {}'
HEADERS = {
    'Authorization': 'Access-Token {}'.format(ROBIN_ACCESS_TOKEN),
    'Content-Type': 'application/json'
}


def get_locations(floor):
  params = {
      'query': floor
  }
  location = json.loads(
      requests.get(
          LOCATION_API.format(ROBIN_API_ORG_NAME),
          headers=HEADERS,
          params=params).text)
  logging.info(location)
  return location['data']


def get_free_spaces(floors, start, end):
  query = {
      'scope': {
          'location_ids': floors
      },
      'filters': {
          # 'min_capacity': 1,
          'types': [],
          'include_unbookable': False
      },
      'view_options': {
          'bounds': {
              'from': start,
              'to': end,
              'time_zone': libs.time.TIMEZONE_AREA
          },
          'prioritization_type': 'specific_time'
      }
      # 'paging_info': {'page': 1,'per_page': 2}
  }
  query = json.dumps(query)
  logging.info(query)
  spaces = json.loads(
      requests.post(
          SPACE_API,
          data=query,
          headers=HEADERS).text)
  logging.info(spaces)
  free_spaces = []
  for space in spaces['data']:
    if space['busy'] == []:
      free_spaces.append(space)

  logging.info(free_spaces)
  return free_spaces


def get_free_space(floors, start, end, capacity):
  query = {
      'scope': {
          'location_ids': floors
      },
      'filters': {
          'min_capacity': capacity,
          # 'max_capacity': capacity,
          'types': [],
          'include_unbookable': False
      },
      'view_options': {
          'bounds': {
              'from': start,
              'to': end,
              'time_zone': libs.time.TIMEZONE_AREA
          },
          'prioritization_type': 'specific_time'
      },
      # 'paging_info': {'page': 1,'per_page': 1}
  }

  query = json.dumps(query)
  logging.info(query)
  spaces = json.loads(
      requests.post(
          SPACE_API,
          data=query,
          headers=HEADERS).text)
  logging.info(spaces)

  for space in spaces['data']:
    if space['busy'] == []:
      return space

  return {}


def book_space(space_id, start, end, user_name, email):
  query = {
      'start': {
          'date_time': start,
          'time_zone': libs.time.TIMEZONE_AREA
      },
      'end': {
          'date_time': end,
          'time_zone': libs.time.TIMEZONE_AREA
      },
      'title': MEETING_TITLE.format(user_name),
      'include_in_demand': True,
      'invitees': [
          {
              'email': email
          }
      ]
  }

  query = json.dumps(query)
  logging.info(query)
  meeting = json.loads(
      requests.post(
          BOOK_ROOM_API.format(space_id),
          data=query,
          headers=HEADERS).text)
  logging.info(meeting)

  return meeting
