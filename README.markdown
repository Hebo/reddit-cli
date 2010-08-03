reddit-cli
==========

reddit-cli is a tool that lets you browse reddit.com and follow links from a command line shell. reddit-cli supports subreddits and even has a boss key!

Usage
----- 
run `python2.7 reddit-cli.py`

Keys
----

 * `o,Enter` : open link in system default webbrowser
 * `O` : open link in lynx
 * `q` : quit
 * `b` : boss mode (executes `man python` by default)
 * `u` : refresh
 * `s` : open subreddit
 * `j,k` or arrow keys : scroll


While unfinished at present, reddit-cli will eventually allow you to:

 * read comments

Requirements:

 * [python 2.7](http://www.python.org/download/releases/2.7/)
 * lynx if you want the ability to open links with it
 * "light on dark" terminal color scheme