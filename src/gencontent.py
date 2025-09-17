import os
from conversion import markdown_to_html_node
def extract_title(markdown):
        lines = markdown.split('\n')
        for line in lines:
            if line.startswith("# "):
                return line[2:].strip()
        raise Exception("No title found in markdown")


def generate_page(from_path, template_path, dest_path, basepath):
    
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
    full_html = full_html.replace('href="/', f'href="{basepath}')
    full_html = full_html.replace('src="/', f'src="{basepath}')
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for root, dirs, files in os.walk(dir_path_content):
        for filename in files:
            if filename.endswith('.md'):
                from_path = os.path.join(root, filename)
                rel_path = os.path.relpath(from_path, dir_path_content)
                dest_rel_path = os.path.splitext(rel_path)[0] + '.html'
                dest_path = os.path.join(dest_dir_path, dest_rel_path)

                # Delegate the actual page generation
                generate_page(from_path, template_path, dest_path, basepath)

