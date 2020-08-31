import os
import logging
import i18n
import json
# [IMPORT MORE PACKAGES if any]

# [IMPORT EXTERNAL FILES if any]

# [ENVIRONMENT VARIABLES if any]

# [CONSTANT VALUES if any]
DEFAULT_LANG = 'ja'

# Logging
logging.getLogger().setLevel(logging.INFO)

# i18n Configuration
base_path = os.path.dirname(os.path.abspath(__file__))
i18n.load_path.append(os.path.join(base_path, './locales'))
i18n.set('filename_format', '{locale}.{format}')
i18n.set('file_format', 'yaml')
i18n.set('skip_locale_root_data', True)

# Set locale
def set_locale(lang):
  i18n.set('locale', lang)
  i18n.set('fallback', DEFAULT_LANG)

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
  set_locale(params['lang'])

  # Response - Post Slack Message
  return json.dumps({
    'slack': True,
    'type': 'message',
    'message': i18n.t('MESSAGE_HELLO_WORLD'),
    'channel': params['channel']['id']
  })
  
  # # Response - Open Slack Dialog
  # # <Refer `Sample payload` for Response Format - Open Slack Dailog section in README.md
  # # and create dialog component>
  # DIALOG = {}
  # return json.dumps({
  #   'slack': True,
  #   'type': 'dialog',
  #   'dialog': DIALOG,
  #   'trigger_id': params['trigger_id'],
  #   'channel': params['channel']['id]
  # })

  # # Response - No response to return 
  # return json.dumps({})

  # # Go through README.md to get more clarity on Response Format




