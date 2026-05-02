from textnode import TextNode
from functions import src_to_destination, generate_pages_recursively
import sys

def main():
    args = sys.argv
    basepath = args[1]
    if basepath == "":
        basepath = "/"
    src_to_destination("./static", "./docs")
    generate_pages_recursively("./content", "./template.html", "./docs", basepath)
main()