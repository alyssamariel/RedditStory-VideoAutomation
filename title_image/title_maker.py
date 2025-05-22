import imgkit
from bs4 import BeautifulSoup
import html
import os
import configparser
import re
from pathlib import Path

config = configparser.ConfigParser()
config.read('config.ini')

# settings
options = {
    'format': 'png',
    'width': '850',
    'enable-local-file-access': None,
    'transparent': ''
}

def format_number(num):
    if num >= 1000:
        return f"{num/1000:.1f}k"
    return str(num)

def generate_reddit_title_image (submission):
    # get file directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    html_template_path = os.path.join(script_dir, "title_image.html")

    # open html file
    with open(html_template_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    # select title, upvotes and comments and reassign value
    fields = {
        "title": submission.title,
        "upvotes": format_number(submission.score) if submission.upvote_ratio is not None else "99+",
        "comments": format_number(submission.num_comments) if submission.num_comments is not None else "99+",
    }

    for field_id, value in fields.items():
        p = soup.find("p", id=field_id)
        if p:
            p.string = html.escape(str(value))

    title_p = soup.find("p", id="title")
    if title_p:
        title_p.string = html.escape(submission.title)
    
    # save changes
    with open(html_template_path, "w", encoding="utf-8") as file:
        file.write(str(soup))

    # create folder for post if not exists
    folder_path = Path("post_files") / submission.name
    folder_path.mkdir(parents=True, exist_ok=True)

    output_path = folder_path / f"{submission.name}_title-image.png"

    # generate the image
    imgkit.from_file(html_template_path, str(output_path), options=options)

    for field_id, value in fields.items():
        p = soup.find("p", id=field_id)
        if p:
            p.string = ""

    with open(html_template_path, "w", encoding="utf-8") as file:
        file.write(str(soup))

    return output_path


        
