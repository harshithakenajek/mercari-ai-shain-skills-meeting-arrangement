import logging
import i18n
import libs.firebase


# Book the slot and send the DM to the users
def start(params):
    logging.info('T_Meeting_Arrangement_Slot....[START]')
    logging.info(params)
    i18n.set('locale', params['data']['lang'])

    # Fetch the data from the previous modal submission - firestore
    meeting_data = libs.firebase.ref_meeting.child(params['user']).get()
    logging.info(meeting_data)
