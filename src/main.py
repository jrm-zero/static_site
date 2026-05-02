from textnode import TextNode
from functions import src_to_destination, generate_pages_recursively
import sys

def main():
    basepath = sys.argv[0]
    if basepath == "":
        basepath = "/"
    src_to_destination("./static", "./public")
    generate_pages_recursively("./content", "./template.html", "./docs", basepath)
main()