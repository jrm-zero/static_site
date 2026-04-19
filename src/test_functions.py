import unittest
import re
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
    def test_bold(self):
        node = TextNode("Hello **World**, it is I **Golgeram**!", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertTrue(len(new_nodes) == 5)
    def test_italics(self):
        node = TextNode("Hello _World, it is I_ Golgeram!", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertTrue(len(new_nodes) == 3)
        for i in range(len(new_nodes)):
            self.assertNotIn("_", new_nodes[i].text)
    def test_bold_and_italics(self):
        node = TextNode("Hello _World, it is I_ a weird **Golgeram**!", TextType.TEXT)
        new_nodes_2 = split_nodes_delimiter(split_nodes_delimiter([node], "_", TextType.ITALIC), "**", TextType.BOLD)
        self.assertTrue(len(new_nodes_2) == 5)
        for i in range(len(new_nodes_2)):
            self.assertNotIn("_", new_nodes_2[i].text)
            self.assertNotIn("**", new_nodes_2[i].text)
    def test_code(self):
        node = TextNode("Hello World, it is I a weird Golgeram! see my code: `crazy indeed`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertTrue(len(new_nodes) == 2)
        for i in range(len(new_nodes)):
            self.assertNotIn("`", new_nodes[i].text)
    def test_error(self):
        node = TextNode("Hello World, this is `mess up", TextType.TEXT)
        with self.assertRaises(Exception) as cm:
            split_node = split_nodes_delimiter([node], "`", TextType.CODE)
        the_exception = str(cm.exception)
        self.assertIn("dip shit", the_exception)
    def test_extract_image(self):
        node = TextNode("Crazy times for all involved... ![crazy text for sure](www.google.com/fdwioti) different, well me", TextType.TEXT)
        images = extract_markdown_images(node.text)
        self.assertTrue(len(images) == 1)
        self.assertIn("google.com", images[0][1])
    def test_extract_multiple_images(self):
        node = TextNode(
            '''
            Crazy times for all involved ![crazy text for sure](www.google.com/fdwioti) and 
            ![this is wild!](www.whatsapp.com/what's up my log jams)"
            ''',
            TextType.TEXT
            )
        images = extract_markdown_images(node.text)
        self.assertTrue(len(images) == 2) 
        self.assertIn("google.com", images[0][1])
    def test_extract_links(self):
        node = TextNode("Crazy times for all involved... [linky being links](www.google.com) different, well me", TextType.TEXT)
        links = extract_markdown_links(node.text)
        self.assertTrue(len(links) == 1)
        self.assertIn("google.com", links[0][1])
    def test_extract_multiple_links(self):
        node = TextNode(
            '''
            Crazy times for all involved [linky being links](www.google.com/whatisup) and 
            [so wild!](www.whatsapp.com/what's up my what's ups)"
            ''',
            TextType.TEXT
            )
        links = extract_markdown_links(node.text)
        self.assertTrue(len(links) == 2)
        self.assertIn("what's", links[1][1])
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    def test_extract_markdown_both(self):
        node = TextNode(
            '''
            Crazy times for all involved [linky being links](www.google.com/whatisup) and 
            ![so wild!](src/myworld/images)"
            ''',
            TextType.TEXT
            )
        links = extract_markdown_links(node.text)
        images = extract_markdown_images(node.text)
        self.assertTrue(len(links) == 1)
        self.assertTrue(len(images) == 1)
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_split_links(self):
        node = TextNode(
            "This is a hyperlink [please click here](https://i.imgur.com/zjjcJKZ.png) and another [nope, click here!](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is a hyperlink ", TextType.TEXT),
                TextNode("please click here", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "nope, click here!", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_split_both(self):
        node = TextNode(
            "This is a hyperlink [please click here](https://i.imgur.com/zjjcJKZ.png) and this is an image ![image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link(split_nodes_image([node]))
        self.assertListEqual(
            [
                TextNode("This is a hyperlink ", TextType.TEXT),
                TextNode("please click here", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and this is an image ", TextType.TEXT),
                TextNode(
                    "image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_split_mixed(self):
        node = TextNode(
            "**This** is a hyperlink [clickety, click](www.google.com) and _this_ is an image ![clackety, clack](www.reddit.com)",
            TextType.TEXT
        )
        new_nodes = split_nodes_delimiter(
            split_nodes_delimiter(
                split_nodes_image(
                    split_nodes_link([node])
                    ), "**", TextType.BOLD
                ), "_", TextType.ITALIC
            )
        self.assertListEqual(
            [
                TextNode("This", TextType.BOLD),
                TextNode(" is a hyperlink ", TextType.TEXT),
                TextNode("clickety, click", TextType.LINK, "www.google.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("this", TextType.ITALIC),
                TextNode(" is an image ", TextType.TEXT),
                TextNode("clackety, clack", TextType.IMAGE, "www.reddit.com")

            ],
            new_nodes,
        )
    def test_split_mixed_error(self):
        node = TextNode(
            "**This** is a hyperlink [clickety, click](www.google.com) and _this is an image ![clackety, clack](www.reddit.com)",
            TextType.TEXT
        )
        with self.assertRaises(Exception) as cm:
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_image(
                        split_nodes_link([node])
                        ), "**", TextType.BOLD
                    ), "_", TextType.ITALIC
                )
        the_exception = str(cm.exception)
        self.assertIn("dip shit", the_exception)
    def test_text_to_textnodes(self):
        test_text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        converted_nodes = text_to_textnodes(test_text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            converted_nodes
        )
    def test_text_to_textnodes_error(self):
        test_text = "This is **text* with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        with self.assertRaises(Exception) as cm:
            converted_nodes = text_to_textnodes(test_text)
        the_exception = str(cm.exception)
        self.assertIn("dip shit", the_exception)
    def test_text_to_textnodes_nothing(self):
        test_text = ""
        converted_nodes = text_to_textnodes(test_text)
        self.assertTrue(len(converted_nodes) == 0)
    def test_text_to_textnodes_spaces(self):
        test_text = "          "
        converted_nodes = text_to_textnodes(test_text)
        self.assertTrue(len(converted_nodes) == 0)