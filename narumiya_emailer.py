from get_tweet import query_api, clean_data
from saving_data import save_date
from send_email import send_email
from translation import translate
from announcement_type import find_announcement_type

import logging
logging.basicConfig(
    filename="logs/emailer.log",
    level=logging.INFO,
    format="%(asctime)s %(message)s"
)

authors = [
   "berriefan",
   "trying_stuff"
]

temp = [   
   "nakamurakunfan",
   "pomponette_MINT"
]

def narumiya_emailer():
   # go through each author
   logging.info("--- run started ---")

   for author in authors:
      uncleaned_data = query_api(author) # get their posts
      tweets = clean_data(uncleaned_data)
      logging.info(f"{author}: {len(tweets)} new tweets")

      # go through each post individually to email them individually
      for tweet in tweets:
         # find announcement type to append it to subject line
         email_subject = find_announcement_type(tweet) + f"NEW POST BY {author}"

         translated_tweet = translate(tweet['text'])

         try:
            send_email(email_subject, translated_tweet, "", tweet['attachments'])
            save_date(uncleaned_data, tweets)
         except Exception as e:
            print(f"failed to send email: {e}")

narumiya_emailer()

