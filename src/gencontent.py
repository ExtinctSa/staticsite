import os
from conversion import markdown_to_html_node
def extract_title(markdown):
        lines = markdown.split('\n')
        for line in lines:
            if line.startswith("# "):
                return line[2:].strip()
        raise Exception("No title found in markdown")


def generate_page(from_path, template_path, dest_path):
    
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, 'r', encoding='utf-8') as f:
        markdown = f.read()
    
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    
    html_node = markdown_to_html_node(markdown)
    html_content = html_node.to_html()
    
    title = extract_title(markdown)
    
    full_html = template.replace('{{ Title }}', title)
    full_html = full_html.replace('{{ Content }}', html_content)
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
