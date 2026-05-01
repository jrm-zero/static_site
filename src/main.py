from textnode import TextNode
from functions import src_to_destination, generate_page

def main():
    src_to_destination("./static", "./public")
    generate_page("./content/index.md", "./template.html", "./public/index.html")
    generate_page("./content/blog/glorfindel/index.md", "./template.html", "./public/blog/glorfindel.html")
    generate_page("./content/blog/majesty/index.md", "./template.html", "./public/blog/majesty.html")
    generate_page("./content/blog/tom/index.md", "./template.html", "./public/blog/tom.html")
    generate_page("./content/contact/index.md", "./template.html", "./public/contact.html")
main()