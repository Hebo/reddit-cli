import urwid
import webbrowser
import os
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
        if key in ('o', 'enter'):
            webbrowser.open(self.story.url)
        elif key == 'O':
            os.system("lynx " + self.story.url)
        else:
            return key

class MainWindow(object):
    """manages main window elements"""
    def __init__(self):
        self.listings = []
        self.subreddit = None
        self.load_stories()
                
    def load_stories(self):
        """load or update stories from (sub)reddit"""
        self.listings = []
        for s in get_stories(self.subreddit):
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
                ('footer', 'black', 'light gray'),
                ('textentry', 'white,bold', 'dark red'),
                ('body', 'light gray', 'default'),
                ('focus', 'black', 'dark cyan', 'standout')
                ]

    # Set up header and footer ui widgets 
    header = urwid.Text(('header', "reddit-cli - http://github.com/cev/reddit-cli"), align='center')
    footer_content = urwid.Text(('footer', "o/O:open s:subreddit u:refresh j,k: scroll q:quit")) 
    footer = urwid.Padding(footer_content, left=1, right=1)
    textentry = urwid.Edit()
    assert textentry.get_text() == ('', []), textentry.get_text()
        
    body = MainWindow()
    
    # Create frame for main window layout
    main_widget = body.get_widget()
    frame = urwid.Frame(    main_widget,
                            header=header, 
                            footer=footer )
    def refresh():
        """reload stories in main window"""
        body.load_stories()
        main_widget = body.get_widget()
        frame.set_body(main_widget)
        
    def edit_handler(keys, raw):
        """respond to keys while user is editing text"""      
        if keys in (['enter'],[]):
            if keys == ['enter']:
                if textentry.get_text()[0] != '':
                    # Parse actual input out of get_text amalgamation
                    # user_input = textentry.get_text()[0][textentry.get_text()[1][0][1]:]
                    body.subreddit = textentry.edit_text
                    body.load_stories()
                    textentry.set_edit_text('')
                    refresh() 
            # Restore original footer
            frame.set_footer(footer)
            frame.set_focus('body')
            loop.input_filter = input_handler
            return
        return keys
        
    def input_handler(keys, raw):
        """respond to keys not handled by a specific widget"""
        for key in keys:
            if key == 's':
                # Replace status footer wth edit widget
                textentry.set_caption(('textentry', ' [subreddit] ?>'))
                frame.set_footer(urwid.Padding(textentry, left=4))
                frame.set_focus('footer')
                loop.input_filter = edit_handler
                return
            elif key in ('j','k'):
                direction = 'down' if key == 'j' else 'up'
                return [direction]
            elif key == 'u':
                refresh()
            elif key == 'b': # boss mode
                os.system("man python")
            elif key == 'q':
                raise urwid.ExitMainLoop()
            return keys

    # Start ui 
    loop = urwid.MainLoop(frame, palette, input_filter=input_handler)
    loop.run()

if __name__ == "__main__":
    main()