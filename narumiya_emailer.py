from get_tweet import get_post
from send_email import send_email
from translation import translate
from announcement_type import find_announcement_type

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
   for author in authors:
      tweets = get_post(author) # get their posts

      # go through each post individually to email them individually
      for tweet in tweets:
         # find announcement type to append it to subject line
         email_subject = find_announcement_type(tweet) + f"NEW POST BY {author}"

         translated_tweet = translate(tweet['text'])

         try:
            send_email(email_subject, translated_tweet, "", tweet['attachments'])
         except Exception as e:
            print(f"failed to send email: {e}")

narumiya_emailer()

