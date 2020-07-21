import os
import logging
import i18n
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
def hello_world(request):
  # Locale setting
  set_locale(DEFAULT_LANG)

  # return the text
  text = i18n.t('MESSAGE_HELLO_WORLD')
  logging.info(text)
  return text




