from textnode import TextNode
from functions import src_to_destination, generate_page

def main():
    src_to_destination("./static", "./public")
    generate_page("./contents/index.md", "./template.html", "./public/index.html")
main()