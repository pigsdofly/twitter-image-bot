"""Does all the downloading stuff"""
import requests
import local_settings
from PIL import Image
from StringIO import StringIO
from random import randint

class BooruGrabber(object):
    """Class for downloading an image from danbooru"""
    danbooru = "http://danbooru.donmai.us"

    def __init__(self):
        """grabs 100 newest images from booru"""
        tags = local_settings.tags

        url = self.danbooru + "/posts.json?limit=100&tags="+str.join("+", tags)
        request = requests.get(url)
        if request.status_code == 200:
            self.r = request.json()[randint(0, len(request.json()))]

    def download_image(self):
        """downloads the image"""
        response = requests.get(self.danbooru + self.r["large_file_url"])
        rtype = self.r["source"].split(".")[-1]
        filename = "img."+rtype
        i = Image.open(StringIO(response.content))
        i.save(filename)
        return filename

    def get_source(self):
        """returns source (booru) of image"""
        return self.danbooru + "/posts/"+str(self.r["id"])


