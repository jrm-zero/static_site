from textnode import *
from htmlnode import *

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text, None)
        case TextType.BOLD:
            return LeafNode("b", text_node.text, None)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text, None)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": f"{text_node.url}"})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": f"{text_node.url}", "alt": f"{text_node.text}"})
        case _:
            raise Exception(f"{text_node.text_type} does not exist as a type")
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        node_split_value = node.text.split(delimiter, maxsplit=2)
        if len(node_split_value) == 1:
            new_nodes.append(node)
            continue
        if len(node_split_value) != 3:
            raise Exception("Not Markdown ya dip shit")
        new_nodes.extend(split_nodes_delimiter(
            [
                TextNode(node_split_value[0], TextType.TEXT),
                TextNode(node_split_value[1], text_type),
                TextNode(node_split_value[2], TextType.TEXT)
            ],
            delimiter,
            text_type
        )
        )
    return new_nodes


