from PIL import Image
import configparser
import random
import os
import shutil


class WallHandler:
    """ Displays downloaded pictures as wallpapers """
    def __init__(self):
        """ Constructor """
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.picture_dir = self.config.get('FILEMANAGER', 'FinalLocation')
        self.display_dir = self.config.get('FILEMANAGER', 'DisplayLocation')
        self.width = self.config.get('SETTINGS', 'MonitorWidth')
        self.height = self.config.get('SETTINGS', 'MonitorHeight')
        self.monitors = self.config.get('SETTINGS', 'NumberMonitors')
        self.resolution = (int(self.width) * int(self.monitors), int(self.height))
        self.desktopenviroment = self.config.get('SETTINGS', 'DestopEnviroment')

    def run(self):
        """ Called every set amount of time. Checks how many monitors there are, if 1, skips the merging. If more than one. Merges pictures and sets that new picture as wallpaper"""
        if int(self.monitors) > 1:
            self.merge_images()
            self.set_wallpaper()
        else:
            self.set_wallpaper(self.get_image())

    def get_image(self):
        """ Chooses a random file from the picture_dir, returns it to be merged """
        image = None
        while(not image or os.path.isfile(image)):
            image = random.choice(os.listdir(self.picture_dir))
        return "/" + image

    def merge_images(self):
        """ Takes two images and merges them together side-to-side
            This is for dual monitors. """
        new_image = Image.new('RGB', (self.resolution))
        with open(self.picture_dir + self.get_image(), 'rb') as file1:
            with open(self.picture_dir + self.get_image(), 'rb') as file2:
                image1 = Image.open(file1)
                image2 = Image.open(file2)
                new_image.paste(image1, (0, 0))
                new_image.paste(image2, (int(self.width), 0))
        new_image.save("paper.jpg")
        shutil.move("paper.jpg", self.display_dir + "/paper.jpg")

    def set_wallpaper(self, image=None):
        """ Checks were DE is running. Sets the wallpaper for that DE """
        if self.desktopenviroment == ("GNOME" or "Unity"):
            if image:
                self.command_call("gnome", image)
            else:
                self.command_call("gnome")
        if self.desktopenviroment == "Cinnamon":
            if image:
                self.command_call("Cinnamon", image)
            else:
                self.command_call("Cinnamon")

    def command_call(self, de, image=None):
        if image:
            os.system("gsettings set org.{}.desktop.background picture-uri file://{}/{}".format(de, self.display_dir, image))
        else:
            os.system("gsettings set org.{}.desktop.background picture-uri file://{}/paper.jpg".format(de, self.display_dir))

