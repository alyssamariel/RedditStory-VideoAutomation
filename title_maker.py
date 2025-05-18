import imgkit
from PIL import Image, ImageChops

options = {
    'format': 'png',
    'width': '850',
    'enable-local-file-access': None,
    'transparent': ''
}

imgkit.from_file('title_image.html', 'output.png', options=options)