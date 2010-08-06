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
        self.main_window.set_subreddit("gaming")
        after = self.main_window.listings
        self.assertNotEquals(before, after)
        self.assertEquals(self.main_window._MainWindow__subreddit, "gaming")

        
class TestStory(unittest.TestCase):

    def setUp(self):
        self.main_window = reddit.MainWindow()

    def testFormatLineSize(self):
        """format_lines should adjust line width"""
        self.main_window.listings[0].original_widget.story.object['title'] = "123456789 " * 10
        lines = self.main_window.listings[0].original_widget.story.format_lines(70)
        self.assertLessEqual( len(lines[0]), 70, lines[0])
        lines = self.main_window.listings[0].original_widget.story.format_lines(40)
        self.assertLessEqual( len(lines[0]), 40, lines[0])
        self.assertLessEqual( len(lines[1]), 40, lines[1])
        


class TestDownloadStories(unittest.TestCase):
    
    def testBadSubredditError(self):
        """should raise a BadSubredditError"""
        self.assertRaises(pages.BadSubredditError, pages.download_stories, "qwer345g63")
        self.assertRaises(pages.BadSubredditError, pages.download_stories, "qwer3 45g 63")
        self.assertRaises(pages.BadSubredditError, pages.download_stories, "78b@$@#$@#   @ 42 4 7cs")

    def testReturnList(self):
        """should return a list"""
        self.assertIsInstance(pages.download_stories(None), list)

    def testReturnStories(self):
        """should return a list of stories"""
        for s in pages.download_stories(None):
            self.assertIsInstance(s, pages.Story)
     
        
if __name__ == "__main__":
    unittest.main()