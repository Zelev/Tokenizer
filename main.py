"""Created by Zelev."""
# Script to facilitate the creation of tokens for tabletop gaming

from enum import Enum
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps


class TokenSize(Enum):
    LARGE = 500
    MEDIUM = 330
    SMALL = 200
    TINY = 100

    @property
    def label(self) -> str:
        return self.name.lower()

    @classmethod
    def choices(cls) -> list[TokenSize]:
        return list(cls)

    @classmethod
    def from_index(cls, index: int) -> TokenSize:
        try:
            return cls.choices()[index - 1]
        except IndexError as exc:
            raise ValueError("Please select a value in the list.") from exc


RESAMPLING: int = Image.Resampling.LANCZOS
BRIGHTNESS_BY_SIZE: dict[TokenSize, float] = {
    TokenSize.TINY: 1.6,
    TokenSize.SMALL: 1.5,
}
TOKEN_REPEAT_COUNT = 5
TOKEN_BINDER_HEIGHT = 30


def prompt_for_image_name() -> str:
    raw_name = input("Please input the name of the image:\n").strip()
    if not raw_name:
        raise ValueError("Image name cannot be empty.")
    return raw_name


def prompt_for_size() -> TokenSize:
    size_msg = "Please select the size from the list:\n"
    for idx, size in enumerate(TokenSize.choices(), start=1):
        size_msg += f"{idx}. {size.label}\n"

    while True:
        try:
            choice = int(input(size_msg).strip())
        except ValueError:
            print("Please enter a valid number from the list.")
            continue
        try:
            return TokenSize.from_index(choice)
        except ValueError:
            print("Please select a value in the list.")


def concat_images(img1: Image.Image, img2: Image.Image) -> Image.Image:
    img_result = Image.new("RGB", (img1.width, img1.height + img2.height))
    img_result.paste(img1, (0, 0))
    img_result.paste(img2, (0, img1.height))
    return img_result


def apply_brightness(image: Image.Image, size: TokenSize) -> Image.Image:
    enhancer = ImageEnhance.Brightness(image)
    brightness = BRIGHTNESS_BY_SIZE.get(size, 1.3)
    return enhancer.enhance(brightness)


def resize_image(image: Image.Image, size: TokenSize) -> Image.Image:
    resized = image.copy()
    resized.thumbnail(
        size=(resized.width, size.value),
        resample=RESAMPLING,
    )
    return resized


def build_token_sheet(image: Image.Image) -> tuple[Image.Image, Image.Image]:
    contour_image = image.filter(ImageFilter.CONTOUR)
    rotated_image = ImageOps.flip(contour_image)
    binder = Image.new("RGB", (image.width, TOKEN_BINDER_HEIGHT))

    coined = concat_images(concat_images(rotated_image, binder), image)
    final = Image.new("RGB", (coined.width * TOKEN_REPEAT_COUNT, coined.height))
    for i in range(TOKEN_REPEAT_COUNT):
        final.paste(coined, (coined.width * i, 0))

    return final, coined


def save_outputs(image_name: str, size: TokenSize, final_image: Image.Image, coined_image: Image.Image) -> None:
    stem = Path(image_name).stem
    final_path = Path(f"./{stem}_{size.label}_coined_horde.jpg")
    coined_path = Path(f"./{stem}_{size.label}_coined.jpg")

    final_image.save(final_path)
    coined_image.save(coined_path)


def main() -> None:
    image_name = prompt_for_image_name()
    size = prompt_for_size()
    print(f"Desired size: {size.label}")

    with Image.open(image_name) as raw_image:
        prepared = resize_image(
            apply_brightness(raw_image, size),
            size,
        )
        final_image, coined_image = build_token_sheet(prepared)

    save_outputs(image_name, size, final_image, coined_image)


if __name__ == "__main__":
    main()
