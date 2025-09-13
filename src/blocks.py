import re
from enum import Enum
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    markdown = markdown.strip()
    raw_blocks = re.split(r'\n\s*\n', markdown)
    blocks = [block.strip() for block in raw_blocks if block.strip()]
    return blocks

def block_to_block_type(block):
    lines = block.split('\n')
    if (block.startswith("# ")
        or block.startswith("## ")
        or block.startswith("### ")
        or block.startswith("#### ")
        or block.startswith("##### ")
        or block.startswith("###### ")):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    is_ordered = True
    for idx, line in enumerate(lines):
        expected_prefix = f"{idx + 1}."
        if not line.startswith(expected_prefix):
            is_ordered = False
            break
    if is_ordered:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH