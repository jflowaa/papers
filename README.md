# Papers
## Gets new pictures on subreddits.

This program was built under Python 3 and Linux.

Has not been ran on Windows.

Fetches posts from subreddits for imgur links. Parses the post title for resolution infomation. If the resolution meets
requirements, it is downloaded. Downloaded images are stored in a temp folder. After all downloading is done, the new
images are renamed with its resolution and a number then moved to a different folder. Program then goes to sleep for a
certain for a certain time. Repeats process when waken. 

#### How To:

To install the required packages:
> pip install -r requirements.txt

To run the program:
> python main.py

To change settings modify the `config.ini`.

Currently log does nothing. Most of the testing for this has only been done with unit tests. These are found in `tests.py`.

This hasn't not gone through a lot of testing. Run this in isolated folders. 

#### To Do:

- Plan to add a GUI.
- Organize/clean code better.
- I don't like how handling image resolution is handled. This includes the degrading.
- More settings
- Implement changing wallpaper. This will probably be for GNOME only
- Dual monitor support for wallpaper changing. May require merging images into one.
- Image extentions are dropped. Windows probably won't like that. Need to get them back.
