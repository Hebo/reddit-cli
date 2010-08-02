import urwid
from pages import Story, get_stories

class MainWindow(object):
	"""manages main window elements"""
	def __init__(self):
		self.stories = []
		self.load_stories()
		
	def load_stories(self, subreddit=None):
		"""load or update stories from specified subreddit"""
		self.stories = []
		for s in get_stories(subreddit):
			current = urwid.Text( ('body', str(s)), wrap='clip' )
			self.stories.append( urwid.Padding(current, left=1, right=1) )
		
	def get_widget(self):
		"""return widget comprised of all stories"""
		stories_formatted = self.stories[:]
		# Separate stories with blank line
		for story in stories_formatted[:]:
			index = stories_formatted.index(story)
			if index != len(stories_formatted) - 1:
				stories_formatted.insert(index + 1, urwid.Divider(" "))
		stories_formatted.insert(0, urwid.Divider(" "))
		# Highlight stories when focused
		self.stories_active = urwid.ListBox( urwid.SimpleListWalker(
							[urwid.AttrMap(w, None, 'focus') for w in stories_formatted]
							))
		return self.stories_active


def main():
	palette =	[
				('header', 'dark magenta,bold', 'default'),
				('footer', 'white,bold', 'dark red'),
				('body', 'light gray', 'default'),
				('focus', 'black', 'dark cyan', 'standout')
				]

	# Set up header and footer ui widgets 
	header_content = urwid.Text(('header', "RedditCLI - http://github.com/cev/redditcli"), align='center')
	footer_content = urwid.Text(('footer', "status: reddit gold required")) 
	footer_content = urwid.Padding(footer_content, left=1, right=1)
		
	body = MainWindow()
	body.load_stories()
	
	# Create frame for main window layout
	main_widget = body.get_widget()
	frame = urwid.Frame(	main_widget,
							header=header_content, 
							footer=footer_content )

	def input_handler(keys, raw):
		for key in keys:
			if key in ('j','k'):
				focus = main_widget.get_focus()
				print focus
				if key == 'j':
					raise Exception, (focus.index(), dir(focus.index))
			if key == 'enter':
				raise urwid.ExitMainLoop()
			#return keys

	# Start ui 
	loop = urwid.MainLoop(frame, palette, input_filter=input_handler)
	loop.run()

if __name__ == "__main__":
	main()