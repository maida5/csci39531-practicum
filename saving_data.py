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

def save_posts(posts):
   try:
      with open("posts.json", 'r') as f:
         data = json.load(f)
      data.extend(posts)
      with open("posts.json", "w") as f:
         json.dump(data,f)
   except Exception as e:
      print(f"error: {e}")
      with open('posts.json', 'w') as f:
         json.dump(posts,f)

def remove_repeated_data(new_posts):
   try:
      print("trying stuff")
      with open("posts.json", 'r') as f:
         old_posts = json.load(f)

      for new_post in list(new_posts):
         for old_post in old_posts:
            if new_post['text'] == old_post['text']:
               new_posts.remove(new_post)
   except:
      print("epic fail")
   return new_posts