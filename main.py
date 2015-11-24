from packages import Reddit
from packages import ImgHandler
from packages import WallHandler
import time
import configparser
import os
import threading

reddit = Reddit()
imghandler = ImgHandler()
wallhandler = WallHandler()
config = configparser.ConfigParser()
config.read('config.ini')
sleep_time = config.get('SETTINGS', 'SleepTime')
cycle_time = config.get('SETTINGS', 'WallpaperCycleTime')


def fetch_images():
    """ Runs in a seperate thread. Fetches images every set amount of time"""
    while(True):
        print("Fetching for new images on set subreddits.")
        reddit.run()
        # if reddit.download_list:  Not working, so checking length instead.
        if len(reddit.download_list) == 0:
            print("No new imgur links found.")
        else:
            print("List of imgur links acquired. Downloading images.")
            print("This could take awhile...")
            for link in reddit.download_list:
                imghandler.download_image(link)
                print("Imaged Downloaded.")
            print("All found images downloaded. Restructuring files...")
            imghandler.restructure()
            print("Files restructured.")
        print("Going to sleep for {} minutes.".format(sleep_time))
        reddit.download_list = []
        time.sleep(int(sleep_time) * 60)
        print("Waking up...")


def cycle_wallpaper():
    """ Runs in a seperate thread. Changes wallpaper every set amount of time"""
    while(True):
        print("Changing wallpaper. Next change in {} minutes".format(cycle_time))
        wallhandler.run()
        time.sleep(int(cycle_time) * 60)


def main():
    print("Starting")
    fetch = threading.Thread(target=fetch_images)
    fetch.start()
    picture_dir = config.get('FILEMANAGER', 'FinalLocation')
    while(len(os.listdir(picture_dir)) < 3):
        print("You currently have no wallpapers, please wait while some get fetched")
        time.sleep(30)
        if os.listdir(picture_dir) != []:
            imghandler.restructure()
            break
    cycle = threading.Thread(target=cycle_wallpaper)
    cycle.start()


if __name__ == "__main__":
    main()
