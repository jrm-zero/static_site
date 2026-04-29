from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "PARAGRAPH"
    HEADING = "HEADING"
    CODE = "CODE"
    QUOTE = "QUOTE"
    UNORDERED_LIST = "UNORDERED_LIST"
    ORDERED_LIST = "ORDERED_LIST"


def block_to_block_type(block):
    if block.startswith("#"):
        for i in range(0,7):
            if block[i+1] != "#" or block[i+1] != " ":
                continue
        return BlockType.HEADING
    elif block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        line_breaks = re.findall(r"(\n.)", block)
        for line_break in line_breaks:
            if line_break[1] != ">":
                continue
        return BlockType.QUOTE
    elif block.startswith("-"):
        line_breaks = re.findall(r"(\n.)", block)
        for line_break in line_breaks:
            if line_break[1] != "-":
                continue
        return BlockType.UNORDERED_LIST
    elif re.search(r"(^\d\.)", block):
        line_breaks = re.findall(r"(\n.{2})", block)
        for line_break in line_breaks:
            if line_break[1:3] != r"\d\.":
                continue
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH