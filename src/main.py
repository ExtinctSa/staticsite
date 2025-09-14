import os
import shutil
import logging
from gencontent import generate_page
def clear_directory(dir_path):
    """Deletes all contents inside the given directory. Recreates it if missing."""
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
        logging.info(f"Deleted directory: {dir_path}")
    os.makedirs(dir_path)
    logging.info(f"Recreated empty directory: {dir_path}")

def copy_recursive(src, dest):
    if not os.path.exists(dest):
        os.makedirs(dest)
        logging.info(f"Created directory: {dest}")

    for item in os.listdir(src):
        src_item = os.path.join(src, item)
        dest_item = os.path.join(dest, item)

        if os.path.isdir(src_item):
            copy_recursive(src_item, dest_item)
        else:
            shutil.copy(src_item, dest_item)
            logging.info(f"Copied file: {src_item} -> {dest_item}")

def main():
    static_dir = 'static'
    public_dir = 'public'
    content_path = 'content/index.md'
    template_path = 'template.html'
    output_path = os.path.join(public_dir, 'index.html')

    if not os.path.exists(static_dir):
        logging.error(f"Source directory '{static_dir}' does not exist. Aborting.")
        return
    logging.basicConfig(level=logging.INFO, format='%(message)s')

   
    logging.info(f"Clearing contents of: {public_dir}")
    clear_directory(public_dir)

    
    logging.info(f"Copying contents from {static_dir} to {public_dir}")
    copy_recursive(static_dir, public_dir)

    logging.info("Sync complete.")
    generate_page(content_path, template_path, output_path)

    logging.info("Site generation complete.")

if __name__ == "__main__":
    main()
