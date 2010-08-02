import urllib2
import json

def smart_truncate(content, length=100, suffix='...'):
	"""truncate on word boundaries"""
	if len(content) <= length:
		return content
	else:
		return ' '.join(content[:length+1].split(' ')[0:-1]) + suffix


class Story:
	"""listing of a single reddit story"""
	def __init__(self, object):
		"""create story from dict object representation"""
		self.object = object
		

	def __getattr__(self, name):
		"""pull elements directly from the stored object"""
		if self.object.has_key(name):
			return self.object.get(name)
		else:
			raise AttributeError, name


	def format_lines(self):
		"""prepare story as a two-string tuple"""
		line1 = "{0}".format(smart_truncate(self.title.encode('utf-8'), length=76))
		line2 = "{0} points	  {1} comments	 {2}   {3}".format(
									self.score,
									self.num_comments,
									self.domain,
									"/r/" + self.subreddit,
									)
		return (line1, line2)

		
def get_stories(subreddit):
	"""download json from reddit and return list of stories"""
	if subreddit is None: 
		url = "http://www.reddit.com/.json"
	else: 
		url = "http://www.reddit.com/r/" + subreddit + "/.json"
	req = urllib2.Request( url )
	opener = urllib2.build_opener()
	try:
		f = opener.open(req)
		stories_raw = json.loads(f.read())

		stories = []
		for i in stories_raw['data']['children']:
			stories.append(Story(i['data']))
		return stories
	except Exception as e:
		raise Exception, "Error getting reddit listings"
	
	