from enum import Enum
from htmlnode import LeafNode
class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        if text_type in (TextType.LINK, TextType.IMAGE) and (not url or url.strip() == ""):
            raise ValueError(f"url must be a non-empty string for text_type '{text_type.value}'")

        self.text = text
        self.text_type = text_type
        self.url = url
    def __eq__(self, other):
        return (self.text == other.text and
                self.text_type == other.text_type and
                self.url == other.url)
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(text_node.text, None)

    elif text_node.text_type == TextType.BOLD:
        return LeafNode(text_node.text, "b")

    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(text_node.text, "i")

    elif text_node.text_type == TextType.CODE:
        return LeafNode(text_node.text, "code")

    elif text_node.text_type == TextType.LINK:
        if not text_node.url:
            raise ValueError("LINK type requires a URL")
        return LeafNode(text_node.text, "a", props={"href": text_node.url})

    elif text_node.text_type == TextType.IMAGE:
        if not text_node.url:
            raise ValueError("IMAGE type requires a URL")
        return LeafNode('', "img", props={"src": text_node.url, "alt": text_node.text})

    else:
        raise ValueError(f"Unsupported TextType: {text_node.text_type}")
