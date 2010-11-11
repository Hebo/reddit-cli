reddit-cli
==========

reddit-cli is a tool that lets you browse reddit.com and follow links from a command line shell. reddit-cli supports logins, subreddits, reading comments and even has a boss key!

Usage
----- 
Run with `./reddit-cli`

Login with `./reddit-cli -u yourusername -p yourpassword`

Keys
----

 * `o,Enter` : open link in system default webbrowser
 * `O` : open link in lynx
 * `h` : open comment thread in browser
 * `l` : open comment thread in lynx
 * `q` : quit
 * `b` : boss mode (executes `man python` by default)
 * `u` : refresh
 * `s` : switch subreddit
 * `j,k` or arrow keys : scroll
 * `n,m` : previous and next page, respectively

Requirements
------------

 * python 2.6 or higher (unit tests require [2.7](http://www.python.org/download/releases/2.7/))
 * lynx if you want the ability to open links with it
 * "light on dark" terminal color scheme