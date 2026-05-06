# csci39531-practicum

---

# Narumiya Automated Tweet Emailer

---

## Overview

This project automates getting tweet data for three accounts: berriefan, nakamurakunfan, and pomponette_MINT, translates that data, then emails it to me. It is scheduled through Windows Task Scheduler.

## Key Features

-  [x] Extract Twitter data through Twitter API
-  [x] Translation
-  [x] Emailing

## Structure

```
announcement_type.py: checks text for keywords to determine the type of announcement
get_tweet.py: queries twitter API and cleans the data returned
narumiya_emailer.py: main file that does the automation
saving_data.py: saves tweets into json and removes repeated posts
send_email.py: composes and sends the email through smtp servers
translation.py: translates text using DeepL API.
```

## Requirements

`pip install deepl requests`

### Environment Variables

In your `.env` file in the root directory, add these variables:

```
TWT_KEY=your_twitter_api_key
SENDER_EMAIL=your_email@gmail.com
SENDER_APP_PASS=your_gmail_app_password
RECIPIENT_EMAIL=recipient@example.com
DEEPL_KEY=your_deepl_api_key
```

Disclaimer: gmail app password is NOT the same as your gmail password
For more info: https://support.google.com/mail/answer/185833?hl=en

### Log folder

Create a logs folder in the root directory, this is where the logs will be.

## Logic

### Translation

### Emailing

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
-  log if fail...
