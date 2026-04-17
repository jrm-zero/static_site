import unittest
from htmlnode import *
from textnode import *
from functions import *

class TestFunctions(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node") 
    def test_error_text(self):
        node = TextNode("This is a nothing node", "Blue")
        with self.assertRaises(Exception) as cm:
            html_node = text_node_to_html_node(node)
        the_exception = str(cm.exception)
        self.assertIn("does not exist", the_exception)
    def test_link(self):
        node = TextNode("Link is here", TextType.LINK, "www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertIsNotNone(html_node.props)
    def test_image(self):
        node = TextNode("picture of a pretty flower", TextType.IMAGE, "pictures/where/server")
        html_node = text_node_to_html_node(node)
        self.assertIsNotNone(html_node.props)
        self.assertIn("src", html_node.__repr__())
    

