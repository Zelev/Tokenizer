"""Created by all."""
# Script to facilitate the creation of tokens for tabletop gaming
from PIL import Image, ImageFilter, ImageOps


sizes = {
    # Lists all the pixels siz for the height, the rest is aspect ratio conservation
    # Assuming always a 300 dpi for al source images.
    'medium': 330,
    'small': 200,
    'large': 500,
    'tiny': 100,
    'Huge': 700
}


def do_io(action):
    if action == 'img_name':
        return input("Please input the name of the image:\n")
    elif action == 'img_scale':
        size_msg = "Please select the size from the list: \n"
        for idx, size in enumerate(sizes):
            size_msg += f"{idx + 1}. {size}\n"
        desired_size = int(input(size_msg))
        while desired_size not in range(1, len(sizes.keys())+1):
            desired_size = input(f"Please select a value in the list: \n")
        desired_size = list(sizes)[desired_size - 1]
        return desired_size

# The raw prefix will be about the original image
raw_name = do_io('img_name')
desired_size = do_io('img_scale')
print(f"desired size: {desired_size}")
raw_image = Image.open(raw_name)
w, h = raw_image.size
raw_image.thumbnail(size=(w,sizes[desired_size]), resample=Image.LANCZOS)
raw_image.show()
# The image to use in the back of the mini will be a pure contour of the original.
contour_image = raw_image.filter(ImageFilter.CONTOUR)
crotated_image = ImageOps.flip(contour_image)
crotated_image.show()
# https://note.nkmk.me/en/python-pillow-concat-images/
