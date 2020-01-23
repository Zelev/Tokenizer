"""Created by Zelev."""
# Script to facilitate the creation of tokens for tabletop gaming
from PIL import Image, ImageFilter, ImageOps, ImageEnhance


sizes = {
    # Lists all the pixels siz for the height, the rest is aspect ratio conservation
    # Assuming always a 300 dpi for al source images.
    'large': 500,
    'medium': 330,
    'small': 200,
    'tiny': 100,
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


def concat_images(img1, img2):
    img_result = Image.new('RGB', (img1.width, img1.height + img2.height))
    img_result.paste(img1, (0, 0))
    img_result.paste(img2, (0, img1.height))
    return img_result


def main():
    # The raw prefix will be about the original image
    raw_name = do_io('img_name')
    desired_size = do_io('img_scale')
    print(f"desired size: {desired_size}")
    raw_image = Image.open(raw_name)
    # Change the contrast so it looks fine printed
    enhancer = ImageEnhance.Brightness(raw_image)
    if desired_size == "tiny":
        bright_image = enhancer.enhance(1.6)
    elif desired_size == "small":
        bright_image = enhancer.enhance(1.5)
    else:
        bright_image = enhancer.enhance(1.3)
    # Resize the image
    bright_image.thumbnail(size=(bright_image.width,sizes[desired_size]), resample=Image.LANCZOS)
    # The image to use in the back of the mini will be a pure contour of the original.
    contour_image = bright_image.filter(ImageFilter.CONTOUR)
    crotated_image = ImageOps.flip(contour_image)
    binder = Image.new('RGB', (bright_image.width, 30))
    # Create a new image that will contain the final version and the horde
    coined = concat_images(concat_images(crotated_image, binder), bright_image)
    final = Image.new('RGB', ((coined.width * 5), coined.height))
    for i in range(5):
        final.paste(coined, (coined.width * i, 0))
    final.save(f"./{raw_name}_{desired_size}_coined_horde.jpg")
    coined.save(f"./{raw_name}_{desired_size}_coined.jpg")


if __name__ == '__main__':
    main()
