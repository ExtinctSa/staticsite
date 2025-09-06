from enum import Enum
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

