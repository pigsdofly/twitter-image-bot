"""Does all the downloading stuff"""
import requests
import local_settings
from PIL import Image
from StringIO import StringIO
import random
import os
import json

class BooruGrabber(object):
    """Class for downloading an image from danbooru"""
    danbooru = "http://danbooru.donmai.us"

    def __init__(self):
        """grabs last x(defined in local_settings) images from booru"""
        tags = local_settings.tags

        if(os.path.exists("requests.json")):
        #if there already exists a file of requests, use that
            f = open("requests.json", "rw")
            request = json.load(f)
            f.close()
        else:
        #otherwise renew the list of requests
            for i in range(0,local_settings.pages):
                url = self.danbooru + "/posts.json?page="+str(i)+"&tags="+str.join("+", tags)
                if not request:
                    request = requests.get(url).json()
                else:
                    request += requests.get(url).json()
            #randomise the list
            random.shuffle(request)

        #pop off the top request from the list
        self.r = request.pop()

        if len(request) <= (local_settings.pages*10):
        #if the requests are getting "stale", remove them
            os.remove("requests.json")
        else:
        #writes changed requests to file
            f = open("requests.json", "w")
            json.dump(request, f)
            f.close()
        print "Downloading image with id "+str(self.r["id"])+"!"

    def download_image(self):
        """downloads the image"""
        response = requests.get(self.danbooru + self.r["large_file_url"])
        rtype = self.r["large_file_url"].split(".")[-1].decode()
        if rtype == "jpg":
            rtype = "jpeg"
        filename = "img."+rtype

        print "Saving image to "+filename+"!"
        i = Image.open(StringIO(response.content))
        i.save(filename,format=rtype)
        self.filename = filename
        print "Image saved at "+filename+"!"

    def get_source(self):
        """returns source (booru) of image"""
        return (self.danbooru + "/posts/"+str(self.r["id"])).decode().encode("UTF-8")

