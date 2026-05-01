class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        html = ""
        for i in self.props:
            html = f"{html} {i}={self.props[i]}"
        return html
    
    def __repr__(self):
        return f"Tag={self.tag}, Value={self.tag}, Children={self.children}, Props={self.props}"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("No value provided")
        if self.tag is None:
            return self.value
        
        if self.props != None:
            html_string = f"<{self.tag}"
            for prop in self.props:
                html_string = f"{html_string} {prop}=\"{self.props[prop]}\""
            html_string = f"{html_string}>{self.value}</{self.tag}>"
        else:
            html_string = f"<{self.tag}>{self.value}</{self.tag}>"
        
        return html_string
    
    def __repr__(self):
        return f"Tag={self.tag}, Value={self.value}, Props={self.props}"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("A parent node has no tag")        
        if self.children is None:
            raise ValueError(f"A parent node has no child")
        
        if self.props != None:
            html_string = f"<{self.tag}"
            for prop in self.props:
                html_string = f"{html_string} {prop}=\"{self.props[prop]}\""
            html_string = f"{html_string}>"
        else:
            html_string = f"<{self.tag}>"
        
        for child in self.children:
            html_string = f"{html_string}{child.to_html()}"
        
        return f"{html_string}</{self.tag}>"