import requests
import os
import configparser
import random
import re
from PIL import Image


class ImgHandler:
    """ Handles downloading and file managment"""
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.temp_dir = self.config.get('FILEMANAGER', 'TempLocation')
        self.final_dir = self.config.get('FILEMANAGER', 'FinalLocation')
        self.display_dir = self.config.get('FILEMANAGER', 'DisplayLocation')
        self.check_dirs()
        self.number_pool = [number for number in range(0, 10000)]

    def check_dirs(self):
        """ Checks if the dirs from config exists. If not creates
            them """
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
        if not os.path.exists(self.final_dir):
            os.makedirs(self.final_dir)
        if not os.path.exists(self.display_dir):
            os.makedirs(self.display_dir)

    def get_number(self):
        """ Gets a random number out of a 10000"""
        number = random.choice(self.number_pool)
        self.number_pool.remove(number)
        return number

    def download_image(self, link):
        """ Downloads the image from imgur using requests """
        response = requests.get(link)
        if response.status_code == 200:
            with open("{}/picture_{}".format(self.temp_dir, self.get_number()), 'wb') as picture:
                for chunk in response.iter_content(4096):
                    picture.write(chunk)

    def restructure(self):
        """ Iterates through temp directory for images to be renamed and moved """
        for folder, subfolders, image_names in os.walk(self.temp_dir, topdown=False):
            for image_name in image_names:
                self.rename_image(self.make_image_name(image_name), image_name)

    def make_image_name(self, name):
        """ Creates a string like the following:
                wallpaper_1920x1080_20.jpg """
        with open(self.temp_dir + "/{}".format(name), 'rb') as image:
            res = str(Image.open(image).size)
        res = res.replace(" ", "").replace(",", "x")
        res = re.sub('[()]', '', res)
        return "wallpaper_{}_{}".format(res, str(self.get_number()))

    def rename_image(self, new_name, name):
        """ Takes the new image name and moves the picture to the final dir with new name. """
        while True:
            try:
                os.rename(self.temp_dir + "/{}".format(name), self.final_dir + "/{}".format(new_name))
                break
            except FileExistsError:
                new_name = self.make_image_name(name, self.get_number())
