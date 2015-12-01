import unittest
import configparser
import praw
import requests
import os
import re
from PIL import Image, ImageChops


class TestConfig(unittest.TestCase):
    """ Tests for config file """
    def test_open(self):
        """ Tests by openning the config. Getting the sections in the
            config. Comparing sections to the known sections. """
        config = configparser.ConfigParser()
        config.read('../config.ini')
        config_sections = config.sections()
        correct_sections = ("FILEMANAGER", "SETTINGS", "REDDIT")
        self.assertEqual(set(config_sections), set(correct_sections))


class TestReddit(unittest.TestCase):
    """ Tests for Reddit API"""
    def test_connnection(self):
        reddit = praw.Reddit(user_agent="Testing connection")
        self.assertIsNotNone(reddit)

    def test_is_imgur(self):
        """ Tests if the post URL has imgur in it. """
        reddit = praw.Reddit(user_agent="Testing connection")
        subreddit = reddit.get_subreddit("earthporn")
        submissions = subreddit.get_hot(limit=5)
        for submission in submissions:
            if "imgur.com" in submission.url:
                self.assertTrue(True)

    def get_five_posts(self):
        """ Gets the top five posts on /r/earthporn """
        reddit = praw.Reddit(user_agent="Testing connection")
        subreddit = reddit.get_subreddit("earthporn")
        submissions = subreddit.get_new(limit=5)
        return submissions

    def test_unique(self):
        """ Writes the post IDs to a file. Checks if ID is in file."""
        if os.path.isfile("test_post_ids"):
            os.remove("test_post_ids")
        with open("test_post_ids", 'w') as writer:
            for submission in self.get_five_posts():
                writer.write(submission.id + '\n')
        with open("test_post_ids", 'r') as reader:
            for submission in self.get_five_posts():
                if submission.id in reader:
                    self.assertTrue(True)

    def test_get_resolution(self):
        """ Rules on most subreddits have posting the resolution
            within the title. Use regex to pull the resolution"""
        post_title = """Autumn and Winter Collide - Massive Storm Damage - Illinois, US [OC] [4264x2431]"""
        post_title2 = """Autumn and Winter Collide - Massive Storm Damage - Illinois, US [OC] [4264 * 2431]"""
        # Checks for 4 digits. 0 or 1 spaces. An x, X or *. Checks
        # another 4 digits
        pattern = re.compile("(\d\d\d\d\s?[x|X|*]\s?\d\d\d\d)")
        self.assertEqual("4264x2431", pattern.search(post_title).group())
        res = pattern.search(post_title2).group()
        res = res.replace(" ", "")
        res = res.replace("*", "x")
        self.assertEqual("4264x2431", res)


class TestImageHandling(unittest.TestCase):
    """ Tests downloading an image. Checking uniques. Resolution Check
        before downloading """
    @unittest.skip("Skipping downloading: time to download")
    def test_download(self):
        """ Downloads an image using requests. Deletes it after
            checking if the file exists. """
        response = requests.get("https://i.imgur.com/fVkcDBD.jpg")
        if response.status_code == 200:
            with open("picture", 'wb') as picture:
                for chunk in response.iter_content(4096):
                    picture.write(chunk)
        self.assertTrue(os.path.isfile("picture"))
        os.remove("picture")

    def test_merge_images(self):
        """ Merges x number of images for x number of monitors. With width of 1920 pixels. """
        x = 3
        test_image = Image.new('RGB', (1920 * x, 1080))
        for i in range(x):
            with open("pic{}.jpg".format(i), 'rb') as picture:
                image = Image.open(picture)
                test_image.paste(image, (1920 * i, 0))
        test_image.save("test.jpg")
        with open("correct.jpg", 'rb') as image1:
            with open("test.jpg", 'rb') as image2:
                correct_image = Image.open(image1)
                test_image = Image.open(image2)
                self.assertTrue(ImageChops.difference(test_image, correct_image).getbbox() is None)

if __name__ == '__main__':
    unittest.main()
