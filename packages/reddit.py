import praw
import configparser
import re


class Reddit:
    """ Wrapper for Reddit. Gets URL for unique images """
    def __init__(self):
        """ Constructor """
        self.cursor = praw.Reddit(user_agent="Papers")
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")
        self.subreddits = self.config.get('REDDIT', 'Subreddits').split(',')
        try:
            with open("post_ids.txt", "r") as reader:
                self.post_ids = [line.strip('\n') for line in reader]
        except FileNotFoundError:
            self.post_ids = []
        self.MinRes = self.config.get('REDDIT', 'MinRes')
        self.post_limt = self.config.get('REDDIT', 'PostsPerSubLimit')
        self.ids_change = False
        self.download_list = []

    def run(self):
        """ Gets new post from subreddits configured in config. Gets the imgur links.
            Saves post id for future runnings """
        for subreddit in self.subreddits:
            for post in self.get_posts(subreddit.strip()):
                if self.is_unique(post.id):
                    imgur_link = self.get_imgur_link(post)
                    if imgur_link:
                        res = self.get_resolution(post.title)
                        if res and self.check_res(res):
                            self.update_download_list(imgur_link)
                    self.add_post_id(post.id)
        if self.ids_change:
            self.update_post_id_file()

    def get_posts(self, subreddit):
        """ Gets a number of new posts on a subreddit """
        subcursor = self.cursor.get_subreddit(subreddit)
        submissions = subcursor.get_new(limit=int(self.post_limt))
        return submissions

    def get_resolution(self, title):
        """ Parses post title and gest resolution """
        # Checks for 4 digits. 0 or 1 spaces. An x, X or *. Checks
        # another 4 digits
        pattern = re.compile("(\d\d\d\d\s?[×|x|X|*]\s?\d\d\d\d)")
        try:
            res = pattern.search(title).group()
            return res
        except AttributeError:
            return None

    def check_res(self, res):
        """ Checks if the res on the title is past the minimum allowed resolution"""
        return int(self.MinRes) <= int(res[-4:])

    def get_imgur_link(self, post):
        """ Gets the imgur link. THe direct image link.
            Most likely will crash on albums """
        if "imgur.com" in post.url:
            if post.url.endswith(".jpg"):
                return post.url
            else:
                return post.url + ".jpg"
        return None

    def update_download_list(self, imgur_link):
        """ This class runs a list of links to be downloaded """
        self.download_list.append(imgur_link)

    def add_post_id(self, id):
        """ A new post is found. Appends the id to the list of IDs. Also sets the
            change flag. This flag is for writing to a file. """
        self.post_ids.append(id)
        self.ids_change = True

    def is_unique(self, id):
        """ Checks if post_id is a unique ID """
        return id not in self.post_ids

    def update_post_id_file(self):
        """ Change flag popped, so the new ID(s) need to be saved to a file for future
            runnings"""
        with open("post_ids.txt", "w") as writer:
            for id in self.post_ids:
                writer.write("{}\n".format(id))
