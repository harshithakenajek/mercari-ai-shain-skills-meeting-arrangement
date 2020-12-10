# -*- coding: utf-8 -*-
import logging
import i18n
import json
from datetime import datetime, timezone, timedelta
import slack
import os
import requests
from googleapiclient.discovery import build
from google.oauth2 import service_account
import pytz

import Arrangement_Modal
import libs.firebase

# Env Vars
SLACK_BOT_USER_TOKEN = os.environ.get('SLACK_BOT_USER_TOKEN')

# Slack Client
slack_client = slack.WebClient(token=SLACK_BOT_USER_TOKEN)

JST = timezone(timedelta(hours=+9), 'JST')
TIME_FORMAT = '%H:00'
DATE_FORMAT = '%Y-%m-%d'
tz = pytz.timezone('US/Central')
SLOT_LIST = ['09:00','09:15', '09:30', '09:45', '10:00', '10:15', '10:30', '10:45', '11:00', '11:15', '11:30', '11:45', \
   '12:00', '12:15', '12:30', '12:45', '13:00', '13:15', '13:30', '13:45', '14:00', '14:15', '14:30', '14:45', \
     '15:00', '15:15', '15:30', '15:40', '16:00', '16:15', '16:30', '16:45', '17:00', '17:15', '17:30', '17:45', '18:00']


def open(params):
  logging.info('Open dialog...[START]')
  logging.info(params)
  # Locale setting
  i18n.set('locale', params['data']['lang'])

  # Extract user profile details to set default contact name and phone
  try:
      logging.info('user info fetcch')
      user_data = slack_client.users_info(
          user=params['user']
      )
      logging.info(user_data)
      # user_name = user_data['user']['profile']['real_name']
      # user_phone = user_data['user']['profile']['phone']
  except BaseException:
      logging.error('Slack user not found...[ERROR]')
      # Return response
      return json.dumps({
          'client': 'slack',
          'type': 'message',
          'data': {
              'text': i18n.t('MESSAGE_GUEST_REGISTER_USER_NOT_FOUND')
          },
          'channel': params['channel']
      })

  # Set default time to 1 hour from now
  now = datetime.now(JST)
  date = now.strftime(DATE_FORMAT)

  # Dialog Box
  MODAL = Arrangement_Modal.adjustment_Modal(params, date)
  # Return response
  return json.dumps({
      'client': 'slack',
      'type': 'modal',
      'data': {
          'modal': MODAL,
          'trigger_id': params['data']['trigger_id']
      },
      'channel': params['channel']
  })


def start(params):
  logging.info('Meeting adjustment...[Start]')

  # Determine a floor
  logging.info(params)
  data = params['data']['submission']
  meeting_title = data['title']['meeting_title']['value']
  meeting_date = data['date']['meeting_date']['selected_date']

  meeting_floor = data['floor']['meeting_floor']['selected_option']['text']['text']
  # or ['value']
  mandatory_users = data['mandatory_users']['users']['selected_users']
  optional_users = data['optional_users']['users']['selected_users']
  duration = data['meeting_duration']['duration']['selected_option']['value']
  logging.info(meeting_title)
  logging.info(meeting_date)
  logging.info(meeting_floor)
  logging.info(mandatory_users)
  logging.info(optional_users)
  logging.info(duration)
  logging.info('user info fetcch')
  # Get all the mandatory users emails
  mandatoryUser = []

  # Save the data for the interactive messages to bypass the payloads
  try:
    table_data = {
      'user': params['user'],
      'title': meeting_title,
      'date': meeting_date,
      'floor': meeting_floor,
      'duration': duration,
      'mandatory_users': mandatory_users,
      'optional_users' : optional_users
    }
    meeting_data = libs.firebase.ref_meeting.child(params['user']).get()
    logging.info(meeting_data)
    logging.info(meeting_data)
    if meeting_data is not None:
      libs.firebase.ref_meeting.child(params['user']).update(table_data)
      logging.info('Meeting data is not none!!!1111')
    else:
      meeting_id = datetime.now(JST).timestamp()
      meeting_id = str(meeting_id).replace('.', '_')
      data['meeting_id'] = meeting_id
      libs.firebase.ref_meeting.child(params['user']).set(table_data)
  except BaseException as e:
    logging.info(str(e))
    return

  for user in mandatory_users:
      user_data = slack_client.users_info(
          user=user
      )
      email = user_data['user']['profile']['email']
      logging.info(email)
      mandatoryUser.append(email)
  logging.info(mandatoryUser)

  # Get the free time of the mandatory users
  # timeSlots = get_free_busy_time(mandatoryUser)
  parameters = []
  parameters.extend((meeting_date, meeting_title, duration, meeting_floor,
                      mandatory_users, optional_users))
  logging.info('---------------')
  logging.info(parameters)
  timeSlots = get_free_busy_time(mandatoryUser, duration)
  # timeSlots = ['12/10 10:00-11:00', '12/10 12:00-11:00']
  if not len(timeSlots):
      # Return the slack sorry message
      return json.dumps({
          'client': 'slack',
          'type': 'message',
          'data': {
              "text": "I was not able to arrange a meeting. I'm sorry... Please reschedule your request with a new deadline and time"
          },
          'channel': params['channel']
      })
  actions = []
  # button = {}
  i = 0

  while i < len(timeSlots):
      loopparam = parameters.copy()
      # logging.info(loopparam.insert(0, timeSlots[i]))
      actions.append({
          'name': 'button',
          'text': timeSlots[i],
          'type': 'button',
          'value': loopparam
      })
      i += 1

  return json.dumps({
      'client': 'slack',
      'type': 'message',
      'data': {
              "text": "I have checked the schedule! The following time slots could be arranged"
      },
      "attachments": [
          {
              "text": "Select a time slot",
              "fallback": "Unable to fetch free slot. Please contact support",
              "callback_id": "select_slot",
              "color": "#3AA3E3",
              "attachment_type": "default",
              "actions": actions
          }
      ],
      'channel': params['channel']
  })


# Get the users busy time and find the free time from it
def get_free_busy_time(mandatoryUser, duration):
  
  logging.info('Inside get_free_busy_time function')
  # creds = service_account.Credentials.from_service_account_file(
  #   'credentials.json',
  #   scopes=['https://www.googleapis.com/auth/calendar.readonly']
  # )
  # requester = 'harshitha.ks@digital.datamatics.com' # use requester's email
  # creds = creds.with_subject(requester)
  # service = build('calendar', 'v3', credentials=creds)
  creds = service_account.Credentials.from_service_account_file(
      'credentials.json',
      scopes=['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.readonly']
  )
  service = build('calendar', 'v3', credentials=creds)
  # Call the Calendar API
  user_busy_slots = get_busy_time(service, mandatoryUser)
  
  if not user_busy_slots:
      print('No upcoming free slots found.')
  # Find the free slot convinient with all the mandatory users
  free_slots = get_free_time(user_busy_slots, mandatoryUser, duration)
  return free_slots

# Get the busy time to extract the user's sfree time 
def get_busy_time(service, mandatoryUser):
  now = datetime.utcnow()
  to = datetime.utcnow() + timedelta(hours=9)
  # logging.info(now)
  # logging.info(to)
  print('Getting the upcoming 10 events')
  body = {
      "timeMin": now.isoformat() + 'Z',
      "timeMax": to.isoformat() + 'Z',
      "timeZone": '+0900'
  }
  user_busy_slots = []
  for user in mandatoryUser:
      body["items"] = [{"id": user}]
      events_result = service.freebusy().query(body=body).execute()
      logging.info(events_result)
      cal_dict = events_result[u'calendars']
      user_busy_slots.append(cal_dict)
  user_busy_slots = {
    "harshitha.ks@digital.datamatics.com": {
    "busy": [
      {
      "start": "2020-12-02T06:00:00Z",
      "end": "2020-12-02T07:00:00Z"
      }
    ]
    },
    "keito.fakuda@mercari.com": {
        "busy": [
          {
            "start": "2020-12-02T10:00:00Z",
            "end": "2020-12-02T11:00:00Z"
          },
          {
            "start": "2020-12-02T18:30:00Z",
            "end": "2020-12-02T20:30:00Z"
          }
    ]
    }
  }
  return user_busy_slots

def get_free_time(busy_slot, users, duration):
  logging.info('Extracting the free time...')
  slot_list = SLOT_LIST.copy()
  try:
    for busy_time in busy_slot.values():
      for time_list in busy_time.values():
        meeting_date1 = time_list[0]['start'].split('T')[0]
        meeting_date = meeting_date1.split('-')
        meeting_date = '/'.join([meeting_date[2],meeting_date[1]])
        for time in time_list:
          # start
          t = time['start'].split('T')[1].split(':')
          start = t[0] + ':' + t[1]
          # end
          t = time['end'].split('T')[1].split(':')
          end = t[0] + ':' + t[1]
          # Remove the slots in which the users are busy
          slot_list = [x for x in slot_list if not(start<=x<end)]
    # form the Slot in the format
    slots = []
    i=0
    while i < len(slot_list)-1:
      date_time_obj = datetime.strptime(meeting_date1 + ' ' + slot_list[i], '%Y-%m-%d %H:%M')
      date_time_obj = str(date_time_obj + timedelta(minutes = int(duration))) # Get the meeting time based on the meeting duration

      date_time_obj = date_time_obj.split()[1].split(':')
      time_obj = ':'.join([date_time_obj[0],date_time_obj[1]])
      print(time_obj)
      slots.append(meeting_date + ' ' + slot_list[i] + '-' + time_obj)
      i = i + 1
    logging.info('Free slots...')
    print(slots)
    return slots
  except BaseException as e:
    logging.error('Getting the Free Time Slots.. [ERROR]' + str(e))

  