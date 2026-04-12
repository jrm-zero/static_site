from enum import Enum

class TextType(Enum):
    plain_text = None
    bold_text = None
    italic_text = None
    code_text = None
    links = None
    images = None

class TextNode:
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, object):
        if {
            self.text == object.text and
            self.text_type == object.text_type and
            self.url == object.url
        }:
            return True
        else:
            return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"