import urwid
from pages import Story, get_stories

class Listing(urwid.FlowWidget):
    """contains a single story and manages its events"""
    def __init__(self, story):
        self.story = story
        self.lines = story.format_lines()
    def selectable(self):
        return True
    def rows(self, size, focus=False):
        return 2
    def render(self, size, focus=False):
        (maxcol,) = size
        if focus:
            pass
        # pad lines to column width
        fill = lambda x: x.ljust(maxcol)
        return urwid.TextCanvas(text=list(map(fill, self.lines)))
    def keypress(self, size, key):
        return key

class MainWindow(object):
    """manages main window elements"""
    def __init__(self):
        self.listings = []
        self.load_stories()
        
    def load_stories(self, subreddit=None):
        """load or update stories from specified subreddit"""
        self.listings = []
        for s in get_stories(subreddit):
            current = Listing(s)
            self.listings.append(urwid.Padding(current, left=1, right=1))
        
    def get_widget(self):
        """return widget comprised of all listings"""
        listings_formatted = self.listings[:]
            
        # Separate stories with blank line & highlight on focus
        for (i, l) in enumerate(listings_formatted):
            filled = urwid.Filler(urwid.AttrMap(l, None, 'focus'))
            listings_formatted[i] = urwid.BoxAdapter(filled, 3)
        listings_formatted.append(urwid.Divider("*"))
        
        self.listings_active = urwid.ListBox(urwid.SimpleListWalker(listings_formatted))
        return self.listings_active


def main():
    palette =   [
                ('header', 'dark magenta,bold', 'default'),
                ('footer', 'white,bold', 'dark red'),
                ('body', 'light gray', 'default'),
                ('focus', 'black', 'dark cyan', 'standout')
                ]

    # Set up header and footer ui widgets 
    header_content = urwid.Text(('header', "reddit-cli - http://github.com/cev/reddit-cli"), align='center')
    footer_content = urwid.Text(('footer', "status: reddit gold required")) 
    footer_content = urwid.Padding(footer_content, left=1, right=1)
        
    body = MainWindow()
    body.load_stories()
    
    # Create frame for main window layout
    main_widget = body.get_widget()
    frame = urwid.Frame(    main_widget,
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
            return keys

    # Start ui 
    loop = urwid.MainLoop(frame, palette, input_filter=input_handler)
    loop.run()

if __name__ == "__main__":
    main()