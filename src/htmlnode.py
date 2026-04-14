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