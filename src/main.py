from textnode import *
def main():
    node = TextNode("This is a link", TextType.LINK, "http://www.boot.dev")
    print(node)

if __name__ == "__main__":
    main()