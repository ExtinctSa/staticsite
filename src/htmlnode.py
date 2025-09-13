import html

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def props_to_html(self):
        if not self.props:
            return ""
        return " " + " ".join(f'{key}="{html.escape(str(value), quote=True)}"' for key, value in self.props.items())


    def __repr__(self):
        return (
            f"HTMLNode(tag={self.tag!r}, value={self.value!r}, "
            f"children={self.children!r}, props={self.props!r})"
        )

class LeafNode(HTMLNode):
    def __init__(self, value, tag=None, props=None, is_raw=False):
        super().__init__(tag=tag, value=value, children=[], props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        props_str = self.props_to_html()
        escaped_value = html.escape(str(self.value))
        if self.tag:
            return f"<{self.tag}{props_str}>{escaped_value}</{self.tag}>"
        return escaped_value

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if not tag:
            raise ValueError("ParentNode must have a tag")
        if children is None or not isinstance(children, list):
            raise ValueError("ParentNode must have children")
        for child in children:
            if not isinstance(child, HTMLNode):
                raise ValueError("Children must be instances of HTMLNode")
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        props_str = self.props_to_html()
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{props_str}>{children_html}</{self.tag}>"

def html_escape(text):
    return html.escape(text)