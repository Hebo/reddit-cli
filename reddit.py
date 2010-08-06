import urwid
import webbrowser
import os
from pages import Story, download_stories, BadSubredditError

class Listing(urwid.FlowWidget):
    """contains a single story and manages its events"""
    def __init__(self, story):
        self.story = story
        
    def selectable(self):
        return True
        
    def rows(self, size, focus=False):
        return 2

    def render(self, size, focus=False):
        (maxcol,) = size
        lines = self.story.format_lines(maxcol)
        if focus:
            pass
        # pad lines to column width
        fill = lambda x: x.ljust(maxcol)
        return urwid.TextCanvas(text=list(map(fill, lines)))

    def keypress(self, size, key):
        if key in ('o', 'enter'):
            webbrowser.open(self.story.url)
        elif key == 'O':
            if self.story.domain[:5] == "self.":
                # Lynx renders mobile reddit better
                url = "http://m.reddit.com" + self.story.permalink
            else:
                url = self.story.url
            os.system("lynx -accept_all_cookies " + url)
        elif key == 'h':
            webbrowser.open("http://www.reddit.com" + self.story.permalink)
        elif key == 'l':
            url = "http://m.reddit.com" + self.story.permalink
            os.system("lynx -accept_all_cookies " + url)
        else:
            return key


class MainWindow(object):
    """manages main window elements"""
    def __init__(self):
        self.listings = []
        self.__subreddit = None
        self.__load_stories()
        
        # Prep header and footer ui widgets 
        self.header = urwid.Text(('header', "reddit-cli - http://github.com/cev/reddit-cli"), align='center')
        self.footer_content = urwid.Text(('footer', "")) 
        self.footer = urwid.Padding(self.footer_content, left=1, right=1)
        
        self.frame = urwid.Frame(   self.__get_widget(),
                                    header=self.header, 
                                    footer=self.footer )
    
    def set_subreddit(self, subreddit):
        """switch subreddits"""
        self.__subreddit = subreddit
        self.set_status("Loading subreddit: /r/{0}".format(subreddit))
        self.refresh()
                                           
    def __load_stories(self):
        """load stories from (sub)reddit and store Listings"""
        self.listings = []
        for s in download_stories(self.__subreddit):
            current = Listing(s)
            self.listings.append(urwid.Padding(current, left=1, right=1))
        
    def __get_widget(self):
        """return TextBox widget containing all Listings"""
        listings_formatted = self.listings[:]
            
        # Separate stories with blank line & highlight on focus
        for (i, l) in enumerate(listings_formatted):
            filled = urwid.Filler(urwid.AttrMap(l, None, 'focus'))
            listings_formatted[i] = urwid.BoxAdapter(filled, 3)
        listings_formatted.append(urwid.Divider("*"))
        
        self.listings_active = urwid.ListBox(urwid.SimpleListWalker(listings_formatted))
        return self.listings_active
        
    def __format_status(self):
        """format status text for use in footer"""
        if self.__subreddit is None:
            subreddit_text = "/r/front_page"
        else:
            subreddit_text = "/r/" + self.__subreddit
        status = "[{0}] ?: help".format(subreddit_text)
        return status
    
    def set_status(self, message=None):
        """write message on footer or else default status string"""
        if message is None:
            status = self.__format_status()
        else:
            status = message
        self.footer_content.set_text(('footer', status))
        
    def refresh(self):
        """reload stories in main window"""
        try:
            self.__load_stories()
        except BadSubredditError:
            self.set_status("Error loading subreddit!")
            return
        main_widget = self.__get_widget()
        self.frame.set_body(main_widget)
        self.set_status()
        
            

def main():
    palette =   [
                ('header', 'dark magenta,bold', 'default'),
                ('footer', 'black', 'light gray'),
                ('textentry', 'white,bold', 'dark red'),
                ('body', 'light gray', 'default'),
                ('focus', 'black', 'dark cyan', 'standout')
                ]

    textentry = urwid.Edit()
    assert textentry.get_text() == ('', []), textentry.get_text()   
    
    print "Loading..."
    body = MainWindow()
    body.refresh()
        
    def edit_handler(keys, raw):
        """respond to keys while user is editing text"""      
        if keys in (['enter'],[]):
            if keys == ['enter']:
                if textentry.get_text()[0] != '':
                    body.set_subreddit(textentry.edit_text)
                    textentry.set_edit_text('')
            # Restore original status footer
            body.frame.set_footer(body.footer)
            body.frame.set_focus('body')
            loop.input_filter = input_handler
            return
        return keys
        
    def input_handler(keys, raw):
        """respond to keys not handled by a specific widget"""
        for key in keys:
            if key == 's':
                # Replace status footer wth edit widget
                textentry.set_caption(('textentry', ' [subreddit] ?>'))
                body.frame.set_footer(urwid.Padding(textentry, left=4))
                body.frame.set_focus('footer')
                loop.input_filter = edit_handler
                return
            elif key in ('j','k'):
                direction = 'down' if key == 'j' else 'up'
                return [direction]
            elif key == 'u':
                body.refresh()
            elif key == 'b': # boss mode
                os.system("man python")
            elif key == '?': # help mode
                os.system("less -Ce README.markdown")
            elif key == 'q': # quit
                raise urwid.ExitMainLoop()
            return keys

    # Start ui 
    loop = urwid.MainLoop(body.frame, palette, input_filter=input_handler)
    loop.run()

if __name__ == "__main__":
    main()