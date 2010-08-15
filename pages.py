import urllib2
import json
import re, htmlentitydefs #html escaping

def smart_truncate(content, length=100, suffix='...'):
    """truncate on word boundaries"""
    if len(content) <= length:
        return content
    else:
        return ' '.join(content[:length+1].split(' ')[0:-1]) + suffix


def unescape(text):
    """Remove HTML or XML character references and entities from a text string"""
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)
        
        
class Story:
    """holds json data of a single reddit story"""
    def __init__(self, object):
        """create story from dict object representation"""
        assert isinstance(object, dict), "json object is not a dict: %s" % type(object)
        self.object = object
        
    def __getattr__(self, name):
        """pull elements directly from the stored object"""
        if self.object.has_key(name):
            return self.object.get(name)
        else:
            raise AttributeError, name

    def format_lines(self, length):
        """prepare story as a two-string tuple of correct length"""
        line1 = "{0}".format(unescape(
                            smart_truncate(self.title.encode('utf-8'), length=length-3)
                            ))
        line2 = "{0} points   {1} comments   {2}   {3}".format(
                                    self.score,
                                    self.num_comments,
                                    self.domain,
                                    "/r/" + self.subreddit,
                                    )
        return (line1, line2[:length])


class BadSubredditError(Exception):
    pass

class Navigation:
    """handles the navigation properties of a single page"""
    def __init__(self, prev, next):
        self.next, self.prev = next, prev
        
    
def download_stories(subreddit, nav=None, direction=None):
    """download json from reddit and return list of stories"""
    if subreddit is None: 
        url = "http://www.reddit.com/.json"
    else: 
        url = "http://www.reddit.com/r/" + subreddit + "/.json"
    
    if not direction is None and not nav is None:
        if direction == "prev":
            url += "?before={0}".format(nav.prev)
        elif direction == "next":
            url += "?after={0}".format(nav.next)
        else:
            raise Exception, "Bad pagination direction given"    
        
    stream = None
    try:
        stream = urllib2.urlopen(url)
    except urllib2.HTTPError as err:
        if err.getcode() in (400,404):
            raise BadSubredditError
        else:
            raise
    if re.search(r'/search\?q=', stream.url):
        raise BadSubredditError
    
    stories_raw = json.loads(stream.read())
    stories = []
    for i in stories_raw['data']['children']:
        stories.append(Story(i['data']))
    
    # Identifier for last/first story on the page for pagination
    next = stories_raw['data']['after']
    prev = stories_raw['data']['before']
    return { "stories": stories, "next": next, "prev": prev }
    
    