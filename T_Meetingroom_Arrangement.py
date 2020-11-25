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

# Env Vars
SLACK_BOT_USER_TOKEN = os.environ.get('SLACK_BOT_USER_TOKEN')

# Slack Client
slack_client = slack.WebClient(token=SLACK_BOT_USER_TOKEN)

JST = timezone(timedelta(hours=+9), 'JST')
TIME_FORMAT = '%H:00'
DATE_FORMAT = '%Y-%m-%d'
tz = pytz.timezone('US/Central')


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
    duration = data['meeting_duration']['duration']['selected_option']['text']['text']
    logging.info(meeting_title)
    logging.info(meeting_date)
    logging.info(meeting_floor)
    logging.info(mandatory_users)
    logging.info(optional_users)
    logging.info(duration)
    logging.info('user info fetcch')
    # Get all the mandatory users emails
    mandatoryUser = []

    for user in mandatory_users:
        user_data = slack_client.users_info(
            user=mandatory_users[0]
        )
        logging.info(user_data)
        email = user_data['user']['profile']['email']
        logging.info(email)
        mandatoryUser.append(email)
    logging.info(mandatoryUser)

    # Get the free time of the mandatory users
    # timeSlots = getFreeTime(mandatoryUser)
    getFreeTime(mandatoryUser)
    return
    timeSlots = ['23/11 10:00-11:00', '23/11 20:00-21:00']
    actions = []
    # button = {}
    i = 0

    while i < len(timeSlots):
        logging.info("button")
        actions.append({
            'name': 'button',
            'text': timeSlots[i],
            'type': 'button',
            'value': timeSlots[i]
        })
        i += 1
    logging.info(actions)
    logging.info('-------------')

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


def getFreeTime(mandatoryUser):
    logging.info('Inside getFreetime function')
    creds = service_account.Credentials.from_service_account_file(
        'credentials.json',
        scopes=['https://www.googleapis.com/auth/calendar']
    )
    service = build('calendar', 'v3', credentials=creds)
    # Call the Calendar API
    now = datetime.utcnow().isoformat()
    to = datetime.utcnow() + timedelta(hours=9)
    logging.info(now)
    logging.info(to)
    print('Getting the upcoming 10 events')
    body = {
        "timeMin": now,
        "timeMax": to.isoformat(),
        "timeZone": 'US/Central'
    }
    user_free_slots = []
    for user in mandatoryUser:
        body["items"] = [{"id": user}]

        events_result = service.freebusy().query(body=body).execute()
        logging.info(events_result)
        cal_dict = events_result[u'calendars']
        user_free_slots.append(cal_dict)
    logging.info('free slots list')
    logging.info(user_free_slots)
    # Find the free slot convinient with all the mandatory users
    if not user_free_slots:
        print('No upcoming free slots found.')
    # events_result = service.events().list(calendarId='primary', timeMin=now,
    #                                       maxResults=10, singleEvents=True).execute()
    # events = events_result.get('items', [])
    # if not events:
    #     print('No upcoming events found.')
    # for event in events:
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     print(start, event['summary'])
    # Write code for accessing free time and put in timeSlots array
    # url = 'https://www.googleapis.com/calendar/v3/freeBusy'
    # parameters = {
    #     "timeMin": "2020-11-22 14:44:55.108088",
    #     "timeMax": "2020-11-23 20:44:55.108088",
    #     "items": [
    #         {
    #             "id": "harshitha.ks@digital.datamatics.com"
    #         }
    #     ]
    # }

    # res = requests.post(url, data=json.dumps(parameters))
    # logging.info(res)
