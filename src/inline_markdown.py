from textnode import TextNode, TextType
import re
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        occurrences = node.text.count(delimiter)
        if occurrences == 0:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        if occurrences % 2 != 0:
            if node.text.strip() == delimiter:
                new_nodes.append(node)
                continue
            else:
                raise ValueError(f"Unmatched delimiter '{delimiter}' in text: {node.text}")
        else:
            for i, part in enumerate(parts):
                if part == "":
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(part, text_type))
    return new_nodes
def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)
def split_nodes_image(old_nodes):
    new_nodes = []
    image_pattern = r'!\[[^\[\]]*\]\([^\(\)]*\)'

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = re.split(f'({image_pattern})', node.text)

        for part in parts:
            if not part:
                continue

            match = re.fullmatch(image_pattern, part)
            if match:
                extracted = extract_markdown_images(part)
                if extracted:
                    alt_text, url = extracted[0]
                    new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
                    continue

            new_nodes.append(TextNode(part, TextType.TEXT))

    return new_nodes
def split_nodes_link(old_nodes):
    new_nodes = []
    link_pattern = re.compile(r'(?<!!) \[([^\[\]]*)\]\(([^\(\)]*)\)', re.VERBOSE)

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        last_index = 0

        for match in link_pattern.finditer(text):
            start, end = match.span()

            # Text before the link
            if start > last_index:
                new_nodes.append(TextNode(text[last_index:start], TextType.TEXT))

            link_text, url = match.groups()
            new_nodes.append(TextNode(link_text, TextType.LINK, url))

            last_index = end

        # Remaining text after the last match
        if last_index < len(text):
            new_nodes.append(TextNode(text[last_index:], TextType.TEXT))

    return new_nodes
def text_to_text_nodes(text):
    if not text:
        return []
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
