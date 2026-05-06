from get_tweet import query_api, clean_data
from saving_data import save_date, save_posts, remove_repeated_data
from send_email import send_email
from translation import translate
from announcement_type import find_announcement_type

import logging
import json
logging.basicConfig(
    filename="logs/emailer.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

authors = [
   "berriefan",
   "trying_stuff",
   "trying_stuff2",
   "nakamurakunfan",
   "pomponette_MINT"
]

def narumiya_emailer():
   # go through each author
   logging.info("--- STARTING PROCESS ---")

   for author in authors:
      logging.info(f"--- {author.upper()} ---")

      # attempting to get api data, retrying if fails
      attempts = 0
      for attempts in range(3):
         try: 
            uncleaned_data = query_api(author) # get their posts
            break
         except Exception as e:
            logging.error(f"{attempts+1} ATTEMPT. ERROR GETTING TWT DATA: {e}. RETRYING...")

      # if failed 3 times, just break out the loop since we can't get twt data
      if attempts == 2:
         logging.error("FAILED TO GET TWT DATA")
         send_email("Automation Failed", "FAILED TO GET TWT DATA, check Twitter API/Logs", "", [])
         break

      tweets = clean_data(uncleaned_data)
      logging.info(f"{author}: {len(tweets)} new tweets")

      # removing repeated tweets
      tweets = remove_repeated_data(tweets)

      if tweets == []:
         logging.info(f"no new tweets from {author}, skipping...")
         continue
  
      # twts that are successfully emailed to update json
      successfully_sent_twts = []

      # go through each post individually to email them individually
      for tweet in tweets:
         # find announcement type to append it to subject line
         email_subject = find_announcement_type(tweet) + f"NEW POST BY {author}"

         attempts = 0
         for attempts in range(3):
            try:
               translated_tweet = translate(tweet['text'])
               break
            except Exception as e:
               logging.error(f"{attempts+1} ATTEMPT. ERROR TRANSLATING: {e}. RETRYING...")

         # even if translation fails, still send the text...
         if attempts == 2:
            logging.error(f"FAILED TO TRANSLATE TWT WITH ID: {tweet["id"]}")
            translated_tweet = tweet['id']
               
         attempts = 0
         for attempts in range(3):
            try:
               send_email(email_subject, translated_tweet, "", tweet['attachments'])
               save_date(uncleaned_data, tweets)
               successfully_sent_twts.append(tweet)
               break
            except Exception as e:
               logging.error(f"{attempts+1} ATTEMPT. failed to send email: {e}. RETRYING...")

         if attempts == 2:
            logging.error(f"FAILED TO SEND EMAIL FOR TWT WITH ID: {tweet["id"]}")
            break

      # saving posts if emailed successfully
      save_posts(successfully_sent_twts)

narumiya_emailer()

