# WE WANT TO find the type of announcement it is if it fits any of the predetermined
# announcement types I have found!!!! woohoo


def find_announcement_type(tweet):
   # i put multiple, because some announcements are multiple types! like something
   # that is yet to be released... and I didn't want that to mess up future logic!
   announcement_type = ""

   tweet_type, content = tweet["type_of_tweet"], tweet["text"]

   if(tweet_type != "authored"):
      announcement_type += "[COLLAB]"
      
   if("発売予定" in content):
      announcement_type += "[PLANNED RELEASE]"
      
   if("発売中" in content):
      announcement_type += "[ON SALE]"

   return announcement_type
   

