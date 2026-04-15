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
        return f"<{self.tag}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"Tag={self.tag}, Value={self.value}, Props={self.props}"