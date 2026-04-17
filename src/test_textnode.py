import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_not_eq_type(self):
        node = TextNode("This is barely a text node", TextType.ITALIC)
        node2 = TextNode("This is barely a text node", TextType.CODE)
        self.assertNotEqual(node, node2)
    def test_not_eq_text(self):
        node = TextNode("Whoop!", TextType.TEXT)
        node2 = TextNode("Whoa!", TextType.TEXT)
        self.assertNotEqual(node, node2)
    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "www.google.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "www.google.com")
        self.assertEqual(node, node2)
    def test_not_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "www.google.com")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()