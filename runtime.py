"""primary runtime actions for the bot"""
import local_settings
from boorugrabber import BooruGrabber
from bot_actions import Bot
import requests
import os


def main():
    bot = Bot()
    
    last_tweet = bot.last_status(local_settings.source)
     
    if(last_tweet):
        last_id = requests.get(last_tweet.split(" ")[0]).url.split("/")[-1]
    else:
        last_id = ""
    grabber = BooruGrabber(last_id)
    
    bot.followback(local_settings.source)
    grabber.download_image()

    bot.make_image_post(grabber.filename,grabber.get_source())
    os.remove(grabber.filename)

main()
