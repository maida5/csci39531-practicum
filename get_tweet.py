# requests for api
import requests

# get variables from .env
import os
from dotenv import load_dotenv

# json to save the twt data
import json

# prettier printing...
from pprint import pprint

# load env var
load_dotenv()

#LOOK INTO THIS!!!
# https://docs.x.com/x-api/users/get-posts

PROFILE_ID = {
   "berriefan":"1362687730631598080",
}

# OLDEST_CHECKED_TWT = 

headers = {"Authorization": f"Bearer {os.getenv("TWT_KEY")}"}

# call api -> parse request -> get needed data for each tweet from DATA ->
# get media key for retweeted tweets -> replace media key with the actual image -> 
# FINISH AND SEND!!!

############# LOOK BACK TO SEE WHAT YOU CAN PUT IN SMALLER FUNCTIONS!!!
def get_post(user):
   # query using the start_id to get tweets after a certain date...

   # change start time so we can convert it instead.. but lets see how it goes first
   params = {
      "start_time": "2026-04-24T00:00:00Z",
      "tweet.fields": "attachments,created_at",
      "expansions": "article.cover_media,article.media_entities,attachments.media_keys,attachments.media_source_tweet,attachments.poll_ids,author_id,edit_history_tweet_ids,entities.mentions.username,geo.place_id,in_reply_to_user_id,entities.note.mentions.username,referenced_tweets.id,referenced_tweets.id.attachments.media_keys,referenced_tweets.id.author_id",
      "media.fields": "alt_text,duration_ms,height,media_key,non_public_metrics,organic_metrics,preview_image_url,promoted_metrics,public_metrics,type,url,variants,width",
   }
   
   url = f"https://api.x.com/2/users/{PROFILE_ID[user]}/tweets"
   response = requests.get(url, headers=headers, params=params)

   tweet_data = response.json()

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
   media_keys_to_images = {}
   for images in tweet_data['includes']['media']:
      media_keys_to_images[images['media_key']] = images['url']
      
   # replacing the keys with the urls
   ## Could Make Into It's Own Function: replace_key_with_url
   for twt in tweets:
      urls_for_key = []
      if twt['attachments']:
         for key in twt['attachments']:
            urls_for_key.append(media_keys_to_images[key])
      twt['attachments'] = urls_for_key

   pprint(tweets)
   return tweets


####### SAVING DATA AND STUFF...

# # saving the tweet into a json! so that we can check if 
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
get_post("berriefan")