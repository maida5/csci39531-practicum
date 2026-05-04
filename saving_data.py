import json

def save_date(tweet_data, tweets):
   # getting last seen twt date
   newest_twt_id = tweet_data['meta']['newest_id']
   newest_twt_date = ""

   for twt in tweets:
      if twt['id'] == newest_twt_id:
         newest_twt_date = twt['date_created']
         break

   data = {"last_twt_date" : newest_twt_date}
   with open('date.json', 'w') as f:
      json.dump(data, f)