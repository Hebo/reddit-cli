reddit-cli
==========

reddit-cli is a tool that lets you browse reddit.com and follow links from a command line shell. reddit-cli supports subreddits, reading comments and even has a boss key!

Usage
----- 
Run with `./reddit-cli`

Keys
----

 * `o,Enter` : open link in system default webbrowser
 * `O` : open link in lynx
 * `c` : open comment thread in browser
 * `C` : open comment thread in lynx
 * `q` : quit
 * `b` : boss mode (executes `man python` by default)
 * `u` : refresh
 * `s` : switch subreddit
 * `j,k` or arrow keys : scroll

Requirements
------------

 * python 2.6 or higher (unit tests require [2.7](http://www.python.org/download/releases/2.7/))
 * lynx if you want the ability to open links with it
 * "light on dark" terminal color scheme