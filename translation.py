# get variables from .env
import os
from dotenv import load_dotenv

import logging
logger = logging.getLogger(__name__)

# load env var
load_dotenv()

import deepl

# translate tweet using DEEPL
def translate(tweet):
   auth_key = os.getenv("DEEPL_KEY")
   deepl_client = deepl.DeepLClient(auth_key)

   try:
      result = deepl_client.translate_text(tweet, target_lang="EN-US", source_lang="JA")
      return result.text
   except Exception as e:
      logging.error(f"failed to translate: {e}")
      raise Exception(e)
