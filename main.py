from packs import Reddit
from packs import ImgHandler
import time
import configparser


def main():
    reddit = Reddit()
    imghandler = ImgHandler()
    config = configparser.ConfigParser()
    config.read('config.ini')
    sleep_time = config.get('SETTINGS', 'SleepTime')
    print("Starting")
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
        print("Going to sleep for: {} minutes.".format(sleep_time))
        time.sleep(int(sleep_time)*60*60)
        print("Waking up...")

if __name__ == "__main__":
    main()
