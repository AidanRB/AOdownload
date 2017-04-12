# AOdownload

Note: it currently only works with Python 2.  Python 3 will crash.  To check your version, run "python --version".  "sudo apt-get install python2" should install the correct version, if you have 3.

Note: It depends on requests and BeautifulSoup4.  To install these, run "pip install requests bs4".

To use the script, either download [this file](https://github.com/AidanRB/AOdownload/blob/master/downloadThread.py) or clone the repository.

To download a thread:

zero. Now theme-independent!

1. Run the script.
2. Put in the thread number you want it to download.
3. Put in what page you want to start downloading at.
4. Put in what page you want to stop downloading at.
  * NOTE: It now works with however many posts there are on a page, unless you have a custom number of posts per page (it'll still download, just with messed up post numbers).  However, the last page should download even if it has less than 10 posts.
5. Put in username/password as requested.
6. Put in whether you want a text file or a CSV.
6. If all goes well, it will download to a CSV/TXT.

If this doesn't work, gimme a holler.  The text file lands in the same folder as the script is in (probably Downloads or wherever you put it).
