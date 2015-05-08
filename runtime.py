"""primary runtime actions for the bot"""
import local_settings
from boorugrabber import BooruGrabber
from bot_actions import Bot


def main():
    bot = Bot()
    grabber = BooruGrabber()
    
    bot.followback(local_settings.source)
    filename = grabber.download_image()

    bot.make_image_post(filename,grabber.get_source)

main()
