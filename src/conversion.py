from htmlnode import HTMLNode, LeafNode, ParentNode
from blocks import BlockType, markdown_to_blocks, block_to_block_type
from inline_markdown import text_to_text_nodes
from textnode import text_node_to_html_node
def text_to_children(text):
    text_nodes = text_to_text_nodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]

def markdown_to_html_node(markdown):
    if not markdown.strip():
        return ParentNode("div", [])

    blocks = markdown_to_blocks(markdown)
    block_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            joined_text = " ".join(line.strip() for line in block.split("\n"))
            node = ParentNode("p", children=text_to_children(joined_text))

        elif block_type == BlockType.HEADING:
            level = block.count("#", 0, block.find(" "))
            content = block[level + 1:].strip()
            node = ParentNode(f"h{level}", children=text_to_children(content))

        elif block_type == BlockType.CODE:
            code_lines = block.split('\n')[1:-1]  
            code_text = '\n'.join(line.strip() for line in code_lines) + '\n'

            node = ParentNode("pre", [LeafNode(code_text, "code")])

        elif block_type == BlockType.QUOTE:
            raw_lines = block.split("\n")
            # Remove leading '>' and optional space
            stripped = []
            for line in raw_lines:
                if line.startswith(">"):
                    s = line[1:]
                    if s.startswith(" "):
                        s = s[1:]
                    stripped.append(s)
                else:
                    stripped.append(line)

            # Take only lines up to the first empty line
            quote_lines = []
            remaining_lines = []
            found_blank = False

            for s in stripped:
                if not found_blank and s.strip() == "":
                    found_blank = True
                    continue
                if not found_blank:
                    quote_lines.append(s)
                else:
                    remaining_lines.append(s)

            # Build the blockquote node
            quote_content = " ".join(quote_lines)
            block_nodes.append(ParentNode("blockquote", children=text_to_children(quote_content)))

            # If there's remaining attribution (non-empty), render as paragraph
            if any(line.strip() for line in remaining_lines):
                remaining_text = " ".join(line.strip() for line in remaining_lines)
                block_nodes.append(ParentNode("p", children=text_to_children(remaining_text)))
            continue
        elif block_type == BlockType.UNORDERED_LIST:
            items = [line[2:].strip() for line in block.split("\n")]
            children = [ParentNode("li", children=text_to_children(item)) for item in items]
            node = ParentNode("ul", children)

        elif block_type == BlockType.ORDERED_LIST:
            items = []
            for line in block.split("\n"):
                dot_index = line.find(".")
                if dot_index != -1:
                    items.append(line[dot_index + 1:].strip())
            children = [ParentNode("li", children=text_to_children(item)) for item in items]
            node = ParentNode("ol", children)

        else:
            # Fallback: treat as paragraph
            node = ParentNode("p", children=text_to_children(block))

        block_nodes.append(node)

    return ParentNode("div", block_nodes)

