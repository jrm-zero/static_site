from textnode import TextNode
from functions import src_to_destination, generate_pages_recursively

def main():
    src_to_destination("./static", "./public")
    generate_pages_recursively("./content", "./template.html", "./public")
main()