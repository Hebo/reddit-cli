import urwid
import pages

class MainWindow(object):
	"""manages main window elements"""
	def __init__(self):
		self.stories = None
		self.load_stories()
		
	def load_stories(self, subreddit=None):
		"""load or update stories from specified subreddit"""
		story1 = urwid.Text(('body', "WHOA - neo, the matrix\n    500 votes    5 comments"))
		story2 = urwid.Text(('body', "neo enters the matrix\n    555 votes   1000 comments"))
		
		story1 = urwid.Padding(story1, left=1, right=1)
		story2 = urwid.Padding(story2, left=1, right=1)
		
		self.stories = [story1, story2]
		
	def get_widget(self):
		"""return widget comprised of all stories"""
		stories_formatted = self.stories[:]
		# Separate stories with blank line
		for story in stories_formatted[:]:
			index = stories_formatted.index(story)
			if index != len(stories_formatted) - 1:
				stories_formatted.insert(index + 1, urwid.Divider(" "))
		stories_formatted.insert(0, urwid.Divider(" "))
		return urwid.ListBox(urwid.SimpleListWalker(stories_formatted))
			

def main():
	palette = 	[
				('header', 'dark magenta,bold', 'default'),
				('footer', 'white,bold', 'dark red'),
				('body', 'light gray', 'default'),
				]

	# Set up header and footer ui widgets 
	header_content = urwid.Text(('header', "RedditCLI - http://github.com/cev/redditcli"), align='center')
	footer_content = urwid.Text(('footer', "status: reddit gold required"))	
	footer_content = urwid.Padding(footer_content, left=1, right=1)
		
		
	body = MainWindow()
	body.load_stories()
	
	# Ceate frame for main window layout
	frame = urwid.Frame(	body.get_widget(),
							header=header_content, 
							footer=footer_content )



	def input_handler(input):
	    if input is 'u':
			body.load_stories()
	    if input == 'enter':
	        raise urwid.ExitMainLoop()

	# Start ui 
	loop = urwid.MainLoop(frame, palette, unhandled_input=input_handler)
	loop.run()

if __name__ == "__main__":
    main()