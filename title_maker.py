import imgkit
from reddit_api import get_reddit_post_title
from bs4 import BeautifulSoup
import html

# settings
options = {
    'format': 'png',
    'width': '850',
    'enable-local-file-access': None,
    'transparent': ''
}

url = input("Enter the URL: ")
title_reddit = get_reddit_post_title(url)

print (title_reddit)
# open html file
with open("title_image.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

# select title and reassign value
title_p = soup.find("p", id="title")
if title_p:
    title_p.string = html.escape(title_reddit)

# save changes
with open("title_image.html", "w", encoding="utf-8") as file:
    file.write(str(soup))

imgkit.from_file('title_image.html', 'output.png', options=options)

# reset value 
title_p.string = ""
with open("title_image.html", "w", encoding="utf-8") as file:
    file.write(str(soup))
