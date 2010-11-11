import urwid
import webbrowser
import os
from pages import Story, RedditHandler, BadSubredditError, Navigation
from optparse import OptionParser # argparse is 2.7-only

# Main loop is global so MainWindow can update the screen asynchronously
main_loop = None

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
        # Handles page downloads and cookies                            
        self.handler = RedditHandler()
        self.listings = []
        self.__subreddit = None
        self.nav = None
        self.__load_stories()
        
        # Prep header and footer ui widgets 
        self.__update_header()
        self.footer_content = urwid.Text(('footer', ""), wrap='clip') 
        self.footer = urwid.Padding(self.footer_content, left=1, right=1)
        
        self.frame = urwid.Frame(   self.__get_widget(),
                                    header=self.header, 
                                    footer=self.footer )

    
    def login(self, username, password):
        """attempt to login"""
        login_result = self.handler.login(username, password)
        if login_result:
            self.__update_header()
        return login_result
      
        
    def set_subreddit(self, subreddit):
        """switch subreddits"""
        self.nav = None
        old_subreddit = self.__subreddit
        if subreddit == "fp":
            self.__subreddit = None
        else:
            self.set_status("Loading subreddit: /r/{0}".format(subreddit))
            self.__subreddit = subreddit
        try:
            self.__load_stories()
        except BadSubredditError:
            self.set_status("Error loading subreddit /r/{0}!".format(subreddit))
            self.__subreddit = old_subreddit
            self.__load_stories()
        main_widget = self.__get_widget()
        self.frame.set_body(main_widget)
        self.set_status()
    
    def __update_header(self):
        """set the titlebar to the currently logged in user"""
        if self.handler.user:
            header_text = "[{0}] - reddit-cli - github.com/cev/reddit-cli".format(self.handler.user)
        else:
            header_text = "reddit-cli - github.com/cev/reddit-cli"
        self.header = urwid.Text(('header',
                                header_text),
                                align='center')
        if hasattr(self, 'frame'):
            self.frame.set_header(self.header)                                   
 
    def __load_stories(self, direction=None):
        """load stories from (sub)reddit and store Listings"""
        self.listings = []
        data = self.handler.download_stories(self.__subreddit, self.nav, direction)
        
        self.nav = data[1]
        for s in data[0]:
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
        status = "[{0}] ({1}) ?: help n/m:pagination".format(self.nav.count/25+1, subreddit_text)
        return status
    
    def switch_page(self, direction):
        """load stories from the previous or next page"""
        if direction == "prev":
            self.set_status("(<) Loading...")
            self.__load_stories(direction=direction)
        elif direction == "next":
            self.set_status("(>) Loading...")
            self.__load_stories(direction=direction)
        else:
            raise Exception, "Direction must be 'prev' or 'next'"
        main_widget = self.__get_widget()
        self.frame.set_body(main_widget)
        self.set_status()
    
    def set_status(self, message=None):
        """write message on footer or else default status string"""
        if message is None:
            status = self.__format_status()
        else:
            status = message
        self.footer_content.set_text(('footer', status))
        
        global main_loop
        if not main_loop is None:
            main_loop.draw_screen()
        
    def refresh(self):
        """reload stories in main window"""
        self.set_status("Reloading...")
        self.nav = None
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
    
    parser = OptionParser()
    parser.add_option("-u", "--username")
    parser.add_option("-p", "--password")
    (options, args) = parser.parse_args()
    
    if options.username and not options.password:
        print "If you specify a username, you must also specify a password"
        exit()
        
    print "Loading..."
    
    body = MainWindow()
    if options.username:
        print "[Logging in]"
        if body.login(options.username, options.password):
            print "[Login Successful]"
        else:
            print "[Login Failed]"
            exit()
            
    body.refresh()
        
    def edit_handler(keys, raw):
        """respond to keys while user is editing text"""      
        if keys in (['enter'],[]):
            if keys == ['enter']:
                if textentry.get_text()[0] != '':
                    # We set the footer twice because the first time we
                    # want the updated status text (loading...) to show 
                    # immediately, and the second time as a catch-all
                    body.frame.set_footer(body.footer)
                    body.set_subreddit(textentry.edit_text)
                    textentry.set_edit_text('')
            # Restore original status footer
            body.frame.set_footer(body.footer)
            body.frame.set_focus('body')
            global main_loop
            main_loop.input_filter = input_handler
            return
        return keys
        
    def input_handler(keys, raw):
        """respond to keys not handled by a specific widget"""
        for key in keys:
            if key == 's':
                # Replace status footer wth edit widget
                textentry.set_caption(('textentry', ' [subreddit?] ("fp" for the front page) :>'))
                body.frame.set_footer(urwid.Padding(textentry, left=4))
                body.frame.set_focus('footer')
                global main_loop
                main_loop.input_filter = edit_handler
                return
            elif key in ('j','k'):
                direction = 'down' if key == 'j' else 'up'
                return [direction]
            elif key in ('n','m'):
                direction = 'prev' if key == 'n' else 'next'
                body.switch_page(direction)
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
    global main_loop
    main_loop = urwid.MainLoop(body.frame, palette, input_filter=input_handler)
    main_loop.run()

if __name__ == "__main__":
    main()