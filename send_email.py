import smtplib
from email.message import EmailMessage

# get variables from .env
import os
from dotenv import load_dotenv

import requests

# load env var
load_dotenv()

def send_email(subject, content, link, photo_attachments):
   msg = EmailMessage()

   msg["Subject"] = subject
   msg["To"] = os.getenv("RECIPIENT_EMAIL")

   msg.set_content(content)

   if link:
      msg.add_attachment(f"link to the product: {link}")

   # ### NEED TO ADD BETTER ERROR HANDLING HERE
   # want to keep track of failed images sent!
   failed_images = 0

   # going through list of attachments...
   for photo in photo_attachments:
      try:
         # as a with statement to not worry about releasing resources
         with requests.get(photo, stream=True) as response:
            response.raise_for_status()

            # this is to get the type of img it is (jpg, etc)
            types = response.headers['Content-Type'].split('/')
            maintype, subtype = types[0], types[1]

            # binary data of the image
            img_data = response.content
            msg.add_attachment(img_data, maintype=maintype, subtype=subtype)
      except Exception as e:
         failed_images+=1
         print(f"Error attaching image: {e}")

   # let me know if there are any fail images in the email itself! wow
   if failed_images:
      msg.add_attachment(f"{failed_images} image/s failed to be attached T_T")

   try:
      # i got this from the lecture! but many sources online use another port. we can investigate. later...
      with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
         smtp.login(os.getenv("SENDER_EMAIL"), os.getenv("SENDER_P"))
         smtp.send_message(msg)
         print("msg sent!")
   except Exception as e:
      print(f"message failed...: {e}")
   
   
# # TESTING
# link = "https://t.co/Kt7VzDRdKq"
# imgs = ["https://pbs.twimg.com/media/HFVNWlEa8AAl0c9?format=jpg&name=medium", "https://pbs.twimg.com/media/HFRJz1mbEAARfuB?format=jpg&name=medium"]

# send_email("test","test",link,imgs)