# Papers

This program was built under Python 3 and Linux.

Has not been tested on Windows.

Fetches posts from subreddits for imgur links. Parses the post title for resolution infomation. If the resolution meets
requirements, it is downloaded. Downloaded images are stored in a temp folder. After all downloading is done, the new
images are renamed with its resolution and a number then moved to a different folder. Program then goes to sleep for a
certain for a certain time. Repeats process when waken. 

This also cycles through the images downloaded as wallpapers. Currently only supports the GNOME, Unity, and Cinnamon desktop enviroment. 

#### How To:

This uses the Pillow package, to install on Linux follow these [instructions](http://pillow.readthedocs.org/en/3.1.x/installation.html#linux-installation), or: 

`` sudo apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk ``

To install the required packages:
> pip install -r requirements.txt

To run the program:
> python main.py

To change settings modify the `config.ini`.

*NOTE* You must set your background alignment option to "spanned" or something simliar for the image to span amoung the monitors. 

Currently log does nothing. Most of the testing for this has only been done with unit tests. These are found in `tests.py`.

This hasn't not gone through a lot of testing. Run this in isolated folders. 

#### To Do:

- Plan to add a full GUI.
- More settings
- Implement changing wallpaper for other DEs
- Image extentions are dropped. Windows probably won't like that. 

