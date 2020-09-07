# -*- coding: utf-8 -*-
import logging
import i18n
import json

# Const vars
GOOGLE_MAP_URL = 'https://www.google.com/maps?hl=en&q={room}&source=calendar'
GOOGLE_CHROME_MAP_EXTENSION_URL = 'https://chrome.google.com/webstore/detail/mercari-map/ehbficidalfbaepebmgkggkchidoekej'


def start(params):
  logging.info('Meeting Room Location...[Start]')

  # Determine a floor
  room_param = params['params']['room']
  logging.info(room_param)

  # Replace spaces with + for URL
  room_param = room_param.replace(' ', '+')
  logging.info(room_param)

  return json.dumps({
        'slack': True,
        'type': 'message',
        'message': i18n.t(
          'MESSAGE_MEETINGROOM_LOCATION',
          url=GOOGLE_MAP_URL.format(room=room_param),
          ext_url=GOOGLE_CHROME_MAP_EXTENSION_URL),
        'channel': params['channel']['id']
    })
