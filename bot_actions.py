"""Contains all the basic bot actions"""
import tweepy
import local_settings

class Bot(object):
    """all the tweepy api calls and such"""
    def __init__(self):
        pub = local_settings.pub_key
        priv = local_settings.priv_key
        key = local_settings.access_key
        secret = local_settings.secret_key

        auth = tweepy.OAuthHandler(pub, priv)
        auth.set_access_token(key, secret)
        self.api = tweepy.API(auth)

    def make_post(self, content):
        """makes a text post"""
        self.api.update_status(content)

    def make_image_post(self, image, content):
        """makes an image post"""
        self.api.update_with_media(image, content)

    def followback(self, userid):
        """checks followers and follows new ones"""
        followers = self.api.followers_ids(userid)
        following = self.api.friends_ids(userid)
        fans = set(followers) - set(following)
        not_fans = set(following) - set(followers)
        for fan in fans:
            self.api.create_friendship(fan)
        for not_fan in not_fans:
            self.api.destroy_friendship(not_fan)

    def last_status(self, userid):
        """returns last status posted by the bot, 
           used to prevent duplicate tweets"""
        timeline = self.api.user_timeline(userid)
        if len(timeline):
            last_tweet = timeline[0].text
        else:
            last_tweet = ""
        return last_tweet

