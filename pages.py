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
    def __init__(self, next, count, stack):
        self.next = next
        self.count = count
        self.stack = stack # store id of the last story on each page in a stack
        
    
def download_stories(subreddit, nav=None, direction=None):
    """download json from reddit and return list of stories"""
    if subreddit is None: 
        url = "http://www.reddit.com/.json"
    else: 
        url = "http://www.reddit.com/r/" + subreddit + "/.json"
    
    if nav is None:
        nav = Navigation(None, 0, ["start"])
    
    if not direction is None:
        if direction == "prev":
            # the end of the stack marks the start of the current page,
            # so we discard it and get a reference to the last page
            if not nav.stack[-1] == "start":
                nav.count -= 25
                nav.stack.pop()
                prev = nav.stack[-1]
                url += "?count={0}&after={1}".format(nav.count, prev)
        elif direction == "next":
            nav.stack.append(nav.next)
            nav.count += 25
            url += "?count={0}&after={1}".format(nav.count, nav.next)
        else:
            raise Exception, "Bad paging direction given"
        
    stream = None
    json_data = None
    try:
        stream = urllib2.urlopen(url)
        json_data = stream.read()
    except urllib2.HTTPError as err:
        if err.getcode() in (400,404):
            raise BadSubredditError
        else:
            raise
    if json_data == "{error: 404}":
        raise BadSubredditError
    elif re.search(r'/search\?q=', stream.url):
        raise BadSubredditError
    
    stories_raw = json.loads(json_data)
    stories = []
    for i in stories_raw['data']['children']:
        stories.append(Story(i['data']))
    
    # Identifier for last/first story on the page for pagination
    nav.next = stories_raw['data']['after']
    return ( stories, nav )
    
    