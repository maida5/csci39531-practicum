# get variables from .env
import os
from dotenv import load_dotenv

# load env var
load_dotenv()

import deepl

# translate tweet using DEEPL
def translate(tweet):
   auth_key = os.getenv("DEEPL_KEY") # replace with your key
   deepl_client = deepl.DeepLClient(auth_key)

   result = deepl_client.translate_text(tweet, target_lang="EN-US", source_lang="JA")
   return result.text
   # print(result.text)
   
# translate("【オンライン発売のお知らせ】\nナルミヤハッピーパークで大好評のフラット刺しゅうポーチと、新作のカラーミニぬいぐるみチャームがナルミヤオンラインにて発売決定！\n発売日時：4/15（水）10:00〜 \n※ミミリーちゃんは新宿ルミネエスト店限定キャラクターのため、オンラインでのお取り扱いはございません\n▼オンライン販売アイテムはこちら")