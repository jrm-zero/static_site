import unittest
from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_print_node(self):
        node = HTMLNode("h1", "All of the Best Stuff", None , {"href": "https://www.google.com",})
        node2 = HTMLNode("p", "I lied, there is nothing in here", None , {"size": "32"})
        self.assertIn("Tag=", node.__repr__())
    def test_props_to_html(self):
        props = {
            "href": "https://www.google.com",
            "link_text": "This is google",
            "color": "red"
        }
        node = HTMLNode("h1", "All of the Best Stuff", None , props)
        html_node = node.props_to_html()
        self.assertIn("=", html_node) 
    def test_error(self):
        node2 = HTMLNode("p", "I lied, there is nothing in here", None , {"size": "32"})
        with self.assertRaises(NotImplementedError):
            node2.to_html()

if __name__ == "__main__":
    unittest.main()
