class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        result = ""
        for key in self.props:
            result += f'{key}="{self.props[key]}", '
        return result[:-2]
    
    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (
            self.tag == other.tag and
            self.value == other.value and
            self.children == other.children and
            self.props == other.props
        )

    def __repr__(self):
        return f"HTMLNode(Tag={self.tag}, Value={self.value}, Children={self.children}, Props={self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("leaf nodes must have a value")
        if self.tag == None:
            return f"{self.value}"
        
        html_string = f"<{self.tag}"
        if self.props != None:
            for key in self.props:
                html_string += f' {key}="{self.props[key]}"'
        
        html_string += f">{self.value}</{self.tag}>"
        return html_string

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("parent nodes must have a value")
    
        if self.children == None:
            raise ValueError("parent nodes must have children")
        
        parent_html = f"<{self.tag}"
        if self.props != None:
            for key in self.props:
                parent_html += f' {key}="{self.props[key]}"'
        parent_html += ">"

        for child in self.children:
            parent_html += child.to_html()

        parent_html += f"</{self.tag}>"

        return parent_html
