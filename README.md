# # csci39531-practicum

# Key Features

-  [x] Emailing

# Emailing

Basic Logic:

-  we use the smtp and email libraries provided by Python! thanks python >\_<
-  takes in: subject, content, link, LIST of photo attachments
-  set subject, recipient, content...
-  add LINK IF PROVIDED as an "attachment" \*\* This could have a better method
-  go through list of images and use requests library to get the BINARY DATA of the image, and attach it as an attachment
-  if any image processing fails... we note that in the email
-  once all of that is DONE...
-  open an SMTP server to GMAIL on port 465 \*\* i got this from lecture but some sources say another port is more secure, however the other port was not working with the method i was going for for some reason so i stuck with this
-  send the message!
-  print if fail...

IMPORTANT Features TBD:

-  Logging!
-  go through the double starred items idk

Fun... Features:

-  perhaps make the email format cuter haha. just some fun
