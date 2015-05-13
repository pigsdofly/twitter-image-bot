"""primary runtime actions for the bot"""
import local_settings
from boorugrabber import BooruGrabber
from bot_actions import Bot
import requests
import os


def main():
    bot = Bot()
     
    grabber = BooruGrabber()
    
    bot.followback(local_settings.source)
    grabber.download_image()

    bot.make_image_post(grabber.filename,grabber.get_source())
    os.remove(grabber.filename)

main()
