import unittest
import reddit, pages

class TestMainWindow(unittest.TestCase):
    
    def setUp(self):
        self.main_window = reddit.MainWindow()
        self.main_window.listings = []
        
    def testLoadStories(self):
        """tests type of loaded stories"""
        self.main_window._MainWindow__load_stories()
        self.assertIsInstance(self.main_window.listings, list)
        
    def testSetStatus(self):
        """should create a status of the word 'firefly'"""
        self.main_window.set_status("firefly")
        self.assertEquals(self.main_window.footer_content.text, "firefly")
    
    def testRefresh(self):
        """should populate listings"""
        self.main_window.refresh()
        self.assertNotEquals(self.main_window.listings, [])
    
    def testSubreddit(self):
        """should switch subreddits"""
        self.main_window.refresh()
        before = self.main_window.listings
        self.main_window.subreddit = "gaming"
        self.main_window.refresh()
        after = self.main_window.listings
        self.assertNotEquals(before, after)

        
class TestStory(unittest.TestCase):
    pass


class TestGetStories(unittest.TestCase):
    
    def testBadSubredditError(self):
        """should raise a BadSubredditError"""
        self.assertRaises(pages.BadSubredditError, pages.get_stories, "qwer345g63")
        self.assertRaises(pages.BadSubredditError, pages.get_stories, "qwer3 45g 63")
        self.assertRaises(pages.BadSubredditError, pages.get_stories, "78b@$@#$@#   @ 42 4 7cs")

    def testReturnList(self):
        """should return a list"""
        self.assertIsInstance(pages.get_stories(None), list)

    def testReturnStories(self):
        """should return a list of stories"""
        for s in pages.get_stories(None):
            self.assertIsInstance(s, pages.Story)
     
        
if __name__ == "__main__":
    unittest.main()