import json
import logging

logger = logging.getLogger(__name__)

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

def save_posts(posts):
   try:
      with open("posts.json", 'r') as f:
         data = json.load(f)
      data.extend(posts)
      with open("posts.json", "w") as f:
         json.dump(data,f)
   except FileNotFoundError:
      logging.warning(f"file not found. creating file: {e}")
      with open('posts.json', 'w') as f:
         json.dump(posts,f)
   except Exception as e:
      logging.error(f"error occurred with saving posts to json: {e}")

def remove_repeated_data(new_posts):
   try:
      with open("posts.json", 'r') as f:
         old_posts = json.load(f)

      old_texts = set()
      for post in old_posts:
         old_texts.add(post['text'])

      non_repeating_posts = []

      for post in new_posts:
         if post['text'] not in old_texts:
            non_repeating_posts.append(post)

      logging.info(f"{len(new_posts) - len(non_repeating_posts)} posts removed")
      return non_repeating_posts
   except FileNotFoundError:
      logging.warning(f"No previous posts found.")
   except Exception as e:
      logging.error(f"error occurred with removing repeated posts: {e}")

   return new_posts