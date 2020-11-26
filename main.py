import os
import logging
import i18n
import json

import T_Meetingroom_Arrangement
import T_Meeting_Arrangement_Slot

# Const Vars
# INTENT_MEETING_ARRANGEMENT = 'T_Meeting - Arrangement'
INTENT_MEETING_ARRANGEMENT_YES = 'T_Meeting - Arrangement - Yes'
INTENT_MEETING_ARRANGEMENT_SLOT = 'T_Meeting - Arrangement - Slot'

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

    # Availability
    # if 'intent' in params['data'] and params['data']['intent'] == INTENT_MEETING_ARRANGEMENT:
    #     return T_Meetingroom_Arrangement.open(params)
    if 'intent' in params['data'] and params['data']['intent'] == INTENT_MEETING_ARRANGEMENT_YES:
        i18n.set('locale', params['data']['lang'])
        return T_Meetingroom_Arrangement.open(params)
    elif 'intent' in params['data'] and params['data']['intent'] == INTENT_MEETING_ARRANGEMENT_SLOT:
        i18n.set('locale', params['data']['lang'])
        return T_Meeting_Arrangement_Slot.start(params)
    elif 'type' in params and params['type'] == 'view_submission':
        i18n.set('locale', params['data']['state'])
        return T_Meetingroom_Arrangement.start(params)
    else:
        i18n.set('locale', params['data']['lang'])
        logging.info('Nothing to do....')

    return json.dumps({})
