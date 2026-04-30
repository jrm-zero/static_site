from textnode import *
from htmlnode import *
from blocks import *
import re

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
        if node.text == "":
            continue
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        node_split_value = node.text.split(delimiter, maxsplit=2)
        if len(node_split_value) == 1:
            new_nodes.append(node)
            continue
        if len(node_split_value) % 2 == 0:
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

def extract_markdown_images(text):
    images = []
    matches = re.findall(r"!\[[^\[\[]*\]\([^\)\(]*\)", text)
    for match in matches:
        alt_text = re.findall(r"!\[(.*?)\]", match)
        src = re.findall(r"\(([^\)\(]*)\)", match)
        images.append((alt_text[0], src[0]))
    return images

def extract_markdown_links(text):
    links = []
    matches = re.findall(r"(?<!\!)\[[^\[\[]*\]\([^\)\(]*\)", text)
    for match in matches:
        alt_text = re.findall(r"\[([^\[\[]*)\]", match)
        src = re.findall(r"\(([^\)\(]*)\)", match)
        links.append((alt_text[0], src[0]))
    return links

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        running_text = node.text
        if len(images) == 0:
            new_nodes.append(node)
        for i in range(len(images)):
            sections = running_text.split(f"![{images[i][0]}]({images[i][1]})", 1)
            new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(images[i][0],TextType.IMAGE, images[i][1]))
            if i == (len(images) - 1) and sections[1] != "":
                if sections[1] != "":
                    new_nodes.append(TextNode(sections[1], TextType.TEXT))
            running_text = sections[1]
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        running_text = node.text
        if len(links) == 0:
            new_nodes.append(node)
        for i in range(len(links)):
            sections = running_text.split(f"[{links[i][0]}]({links[i][1]})", 1)
            new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(links[i][0],TextType.LINK, links[i][1]))
            if i == (len(links) - 1) and sections[1] != "":
                if sections[1] != "":
                    new_nodes.append(TextNode(sections[1], TextType.TEXT))
            running_text = sections[1]
    return new_nodes

def text_to_textnodes(text):
    if len(text.strip()) == 0:
        return []
    node = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_delimiter(
        split_nodes_delimiter(
            split_nodes_delimiter(
                split_nodes_image(
                    split_nodes_link(
                        [node]
                    )
                ),
                "**", TextType.BOLD
            ),
            "_", TextType.ITALIC
        ), "`", TextType.CODE
    )
    return new_nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    for i in range(len(blocks)):
        blocks[i] = blocks[i].strip(" \n")
        if blocks[i] == "":
            blocks.pop(i)
    return blocks

def markdown_to_html_node(markdown):
    converted_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                nodes = text_to_children(combine_newlines(block, block_type))
                converted_node = ParentNode("p", nodes)
            case BlockType.HEADING:
                heading = heading_type(block)
                block = block.strip("# ")
                nodes = text_to_children(block)
                converted_node = ParentNode(f"h{heading}", nodes)
            case BlockType.CODE:
                block = block.strip("`\n")
                converted_node = ParentNode("pre",[LeafNode("code", block)])
            case BlockType.QUOTE:
                nodes = text_to_children(strip_leading_indicators(block, block_type))
                converted_node = ParentNode("block", nodes)
            case BlockType.UNORDERED_LIST:
                nodes = list_to_html(block, block_type)
                converted_node = ParentNode("ul", nodes)
            case BlockType.ORDERED_LIST:
                nodes = list_to_html(block, block_type)
                converted_node = ParentNode("ol", nodes)

        converted_nodes.append(converted_node)

    parent = ParentNode("div", converted_nodes)
    
    return parent

def text_to_children(text):
    nodes = text_to_textnodes(text)
    children = []
    for node in nodes:
        new_node = text_node_to_html_node(node)
        children.append(new_node)
    return children

def list_to_children(text, block_type):
    if block_type is BlockType.UNORDERED_LIST:
        lines = text.split("\n-")
    elif block_type is BlockType.ORDERED_LIST:
        lines = re.findall(r"(\n.{2})", text)
    for line in lines:
        children = text_to_textnodes(line)
        if len(children) > 1:
            new_node = ParentNode("li", children)
            continue
        new_node = LeafNode("li", line)

def heading_type(block):
    count = 0
    for char in block:
        if char == "#":
            count += 1
        elif char == " ":
            break
    return count

def combine_newlines(text, block_type):
    if block_type != BlockType.PARAGRAPH and block_type.QUOTE != BlockType.QUOTE:
        raise Exception(f"{text} is not a paragraph or quote type")
    lines = text.split("\n")
    return " ".join(lines)


def list_to_html(text, block_type):
    if block_type != BlockType.ORDERED_LIST:
        if block_type != BlockType.UNORDERED_LIST:
            raise Exception(f"{text} is not a list block type")
    lines = strip_leading_indicators(text, block_type)    
    list_items = []
    for line in lines:
        if len(text_to_children(line)) == 1:
            list_item = LeafNode("li", line)
        else:
            list_item = ParentNode("li", text_to_children(line))
        list_items.append(list_item)
    return list_items

def strip_leading_indicators(text, block_type):
    lines = text.split("\n")
    match block_type:
        case BlockType.ORDERED_LIST:
            for i in range(len(lines)):
                tmp = lines[i]
                to_strip = re.findall(r"(^\d\.)", tmp)[0]
                lines[i] = tmp.lstrip(to_strip)
        case BlockType.UNORDERED_LIST:
            for i in range(len(lines)):
                tmp = lines[i]
                lines[i] = tmp.lstrip("-")
        case BlockType.QUOTE:
            for i in range(len(lines)):
                tmp = lines[i]
                lines[i] = tmp.lstrip(">")
            stripped_line = " ".join(lines)
            return stripped_line
    return lines