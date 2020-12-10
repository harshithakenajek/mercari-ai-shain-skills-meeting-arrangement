# -*- coding: utf-8 -*-
import os
import logging
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Env vars
FIREBASE_URL = os.environ.get('FIREBASE_URL')
FIREBASE_KEY = os.environ.get('FIREBASE_KEY')
FIREBASE_REF_MEETING = os.environ.get('FIREBASE_REF_MEETING')
FIREBASE_AUTH_UID = os.environ.get('FIREBASE_AUTH_UID')

logging.info(FIREBASE_URL)
logging.info(FIREBASE_KEY)
logging.info(FIREBASE_REF_MEETING)

# Connect to Firebase Database
if not len(firebase_admin._apps):
  base_path = os.path.dirname(os.path.abspath(__file__))
  cred = credentials.Certificate(base_path + FIREBASE_KEY)
  # Initialize the app with a None auth variable, limiting the server's
  # access
  firebase_admin.initialize_app(cred, {
      'databaseURL': FIREBASE_URL,
      'databaseAuthVariableOverride': {
          'uid': FIREBASE_AUTH_UID
      }
  })

ref_meeting = db.reference(FIREBASE_REF_MEETING)
