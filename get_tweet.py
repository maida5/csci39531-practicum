# requests for api
import requests

# get variables from .env
import os
from dotenv import load_dotenv

# json to save the twt data
import json

# prettier printing...
from pprint import pprint

# if this is the first time running the automation or
# if there's an error, we will fall back on datetime
from datetime import datetime

# load env var
load_dotenv()

PROFILE_ID = {
   "berriefan":"1362687730631598080",
   "trying_stuff": "1387796452152422400"
}



# get it at midnight so if it fails in the middle... we can consider that
TODAYS_DATE = (datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + "Z")

headers = {"Authorization": f"Bearer {os.getenv("TWT_KEY")}"}

# call api -> parse request -> get needed data for each tweet from DATA ->
# get media key for retweeted tweets -> replace media key with the actual image -> 
# FINISH AND SEND!!!
# using: https://docs.x.com/x-api/users/get-posts

def get_post(user):
   data = query_api(user)
   return clean_data(data)

############# LOOK BACK TO SEE WHAT YOU CAN PUT IN SMALLER FUNCTIONS!!!
def query_api(user):
   # query using the start_id to get tweets after a certain date...
   start_time = get_date(TODAYS_DATE)

   # change start time so we can convert it instead.. but lets see how it goes first
   params = {
      "start_time": start_time,
      "tweet.fields": "attachments,created_at",
      "expansions": "article.cover_media,article.media_entities,attachments.media_keys,attachments.media_source_tweet,attachments.poll_ids,author_id,edit_history_tweet_ids,entities.mentions.username,geo.place_id,in_reply_to_user_id,entities.note.mentions.username,referenced_tweets.id,referenced_tweets.id.attachments.media_keys,referenced_tweets.id.author_id",
      "media.fields": "alt_text,duration_ms,height,media_key,non_public_metrics,organic_metrics,preview_image_url,promoted_metrics,public_metrics,type,url,variants,width",
   }

   try:
      url = f"https://api.x.com/2/users/{PROFILE_ID[user]}/tweets"
      response = requests.get(url, headers=headers, params=params, timeout=10)
      
      # checking to make sure the request was successful
      response.raise_for_status()
   except requests.exceptions.RequestException as e:
      pprint(f"ERROR FETCHING TWEETS: {e}")
      return []


   tweet_data = response.json()
   return tweet_data

def clean_data(tweet_data):
   if tweet_data['meta']['result_count'] == 0:
      pprint("no tweets fetched...")
      return []

   # pprint(tweet_data)


   tweets = []
   rt_tweets = []
   # to get easy access to the tweets that are retweeted
   rt_ids = []

   # # parsing through just the data to get each post separate!
   # i separate the rt and authored tweets so i can get the media
   # for the rt tweets and add them...

   # could put this in it's own function: create list of tweets
   for post in tweet_data['data']:
      id = post['id']
      text = post['text']
      date_created = post['created_at']

      # some posts don't have attachments
      try:
         attachments = post['attachments']['media_keys']
      except:
         attachments = []

      # some posts are retweeted, and when they are... the media isn't 
      # included so i need to go and get that posts media -_-
      try:
         type_of_tweet = post['referenced_tweets'][0]['type']
         rt_twt_id = post['referenced_tweets'][0]['id']
      except:
         rt_twt_id = None
         type_of_tweet = "authored"
         
      new_post = {
         "id": id,
         "text": text,
         "date_created": date_created,
         "attachments": attachments,
         "type_of_tweet": type_of_tweet,
         "rt_twt_id": rt_twt_id
      }

      if type_of_tweet != "authored":
         rt_tweets.append(new_post)
         rt_ids.append(rt_twt_id)
      else:
         tweets.append(new_post)

   pprint(tweet_data)

   # this is a long and probably roundabout way to find the media attachment
   # of retweets without having to call the API again...
   ## Could Put In Its Own Function: Replace RT Attachments with Keys
   for post in tweet_data['includes']['tweets']:
      if post['id'] in rt_ids:
         for rt_post in rt_tweets:
            if post['id'] == rt_post['rt_twt_id']:
               rt_post['attachments'] = post['attachments']['media_keys']

   # adding the tweets back together on one list
   tweets.extend(rt_tweets)

   # matching the media_key to the url for easier access woohoo
   ## Could make it into it's own function: media_keys_to_images_dict
   try:
      media_keys_to_images = {}
      for images in tweet_data['includes']['media']:

         # this satisifies the use case of potential gifs, videos just link to the tweet
         if images['type'] != 'animated_gif':
            media_keys_to_images[images['media_key']] = images['url']
         else:
            media_keys_to_images[images['media_key']] = images['preview_image_url']
   except (KeyError, TypeError) as e:
      pprint(f"Tweet has no media OR issue with getting media keys: {e}")
      
   # replacing the keys with the urls
   ## Could Make Into It's Own Function: replace_key_with_url
   for twt in tweets:
      urls_for_key = []
      if twt['attachments']:
         for key in twt['attachments']:
            try:
               urls_for_key.append(media_keys_to_images[key])
            except Exception as e:

               twt['text'] = twt['text'] + "\nMEDIA FOUND BUT NOT ATTACHED TO EMAIL"
               print(f"key not found: {e}")
      twt['attachments'] = urls_for_key

   return tweets

####### SAVING DATA AND STUFF...

# get the date of the last tweet, and if the json doesn't exist, then make it!
def get_date(todays_date):
   try:
      with open("date.json", 'r') as f:
         data = json.load(f)
   except:
      data = {"last_twt_date" : todays_date}
      with open('date.json', 'w') as f:
         json.dump(data,f)

   # pprint(data)
   return data['last_twt_date']

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

# # saving the tweets into a json! so that we can check if 
# def save_last_seen_twt(twt_id, twt_txt, date):
#    twt_data = {
#       "twt_id": twt_id,
#       "date_made": date,
#       "twt_txt": twt_txt 
#    }

#    if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
#         # checks if file exists
#         print ("File exists and is readable")
#    else:
#       print ("Either file is missing or is not readable, creating file...")
#       with io.open(os.path.join(PATH, 'seen_twt.json'), 'w') as db_file:
#          db_file.write(json.dumps({}))

## TESTING
get_post("trying_stuff")