import imgkit
from bs4 import BeautifulSoup
import html
import os
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# settings
options = {
    'format': 'png',
    'width': '850',
    'enable-local-file-access': None,
    'transparent': ''
}

def generate_reddit_title_image (title: str):
    # get file directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    html_template_path = os.path.join(script_dir, "title_image.html")

    # open html file
    with open(html_template_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    # select title and reassign value
    title_p = soup.find("p", id="title")
    if title_p:
        title_p.string = html.escape(title)

    # save changes
    with open(html_template_path, "w", encoding="utf-8") as file:
        file.write(str(soup))

    imgkit.from_file(html_template_path, 'output.png', options=options)

    # reset value 
    title_p.string = ""
    with open(html_template_path, "w", encoding="utf-8") as file:
        file.write(str(soup))
