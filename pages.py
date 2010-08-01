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

	def __str__(self):
		"""prepare story as a two-line string"""
		return "{0}\n{1} points   {2} comments   {3}   {4}".format(
									smart_truncate(self.title, length=76), 
									self.score,
									self.num_comments,
									self.domain,
									"/r/" + self.subreddit,
									)

		

def get_stories():
	"""download json from reddit and return list of stories"""
	try:
		req = urllib2.Request("http://www.reddit.com/.json")
		opener = urllib2.build_opener()
		f = opener.open(req)
		stories_raw = json.loads(f.read())
	
		stories = []
		for i in stories_raw['data']['children']:
			stories.append(Story(i['data']))
		return stories
	except Exception as e:
		raise
	
	