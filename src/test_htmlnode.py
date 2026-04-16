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
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_leaf_print(self):
        node = LeafNode("h1", "Hello, World!?")
        node2 = LeafNode("h2", "no, says I", {"bold": "yes","italics": "no"})
        self.assertIn("Hello", node.__repr__())
        self.assertIn(": ", node2.__repr__())
    def test_parent_access(self):
        node = LeafNode("h2", "no, says I", {"bold": "yes","italics": "no"})
        self.assertIn("bold=",node.props_to_html())


    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_missing_child(self):
        child_node = None
        parent_node = ParentNode("p", child_node)
        with self.assertRaises(ValueError) as cm:
            parent_node.to_html()
        the_exception = cm.exception
        self.assertIn("has no child", str(the_exception))
    def test_missing_tag(self):
        child_node = LeafNode("b", "grandchild")
        parent_node = ParentNode(None, child_node)
        with self.assertRaises(ValueError) as cm:
            parent_node.to_html()
        the_exception = cm.exception
        self.assertIn("parent node has no tag", str(the_exception))
    def test_nested_parents(self):
        child_node = ParentNode("p", None)
        parent_node = ParentNode("p", [child_node])
        with self.assertRaises(ValueError) as cm:
            parent_node.to_html()
        the_exception = cm.exception
        self.assertIn("has no child", str(the_exception))
    def test_multi_children(self):
        child_node = LeafNode("span", "child")
        child_node_2 = LeafNode("b", "child_2")
        child_node_3 = ParentNode("p", [child_node])
        child_node_4 = LeafNode("italics", "child_3")
        parent_node = ParentNode("div", [child_node_2, child_node_3, child_node_4])
        self.assertEqual(
            parent_node.to_html(), 
            "<div><b>child_2</b><p><span>child</span></p><italics>child_3</italics></div>"
            )

if __name__ == "__main__":
    unittest.main()
