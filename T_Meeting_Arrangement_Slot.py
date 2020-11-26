import logging
import i18n
import json


# Book the slot and send the DM to the users
def start(params):
    logging.info('T_Meeting_Arrangement_Slot....[START]')
    i18n.set('locale', params['data']['lang'])
    # Fetch the data from the previous modal submission
