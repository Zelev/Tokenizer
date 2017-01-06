"""Created by all."""
# Script to facilitate the creation of tokens for tabletop gaming
from PIL import Image


# The raw prefix will be about the original image
raw_name = input("Please input the name of the image:")
raw_image = Image.open(raw_name)
raw_image.show()
