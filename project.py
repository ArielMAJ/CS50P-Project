"""
Main script for loading this app.
Display loading screen -> Load app in the "background" -> Destroy loading screen and display main
screen.
"""


import io
from ctypes import windll
import threading

from typing import Union, Callable
from PIL import Image, ImageTk  # type: ignore[import]

import main_window  # type: ignore[import]
from loading_screen import LoadingScreen  # type: ignore[import]


def importer():
    """
    This import is really slow when loading the app. Importing it either inside the function that
    uses it or in a different thread feels like it makes for a better user experience.
    """
    global bg
    from rembg import bg  # type: ignore[import]


imp_th = threading.Thread(target=importer)
imp_th.start()

windll.shcore.SetProcessDpiAwareness(1)


def main() -> int:
    """
    This function will start the app.
    """
    functions: dict[str, Callable] = {
        "load_img": load_img,
        "rm_bg": rm_bg,
    }
    root = main_window.MainWindow(functions=functions)
    # This will force loading screen to stay up until rembg is imported (it is a slow import).
    LoadingScreen(
        root,
        wait_for=[imp_th],
        load_img=load_img,
    )
    root.mainloop()
    return 0


def load_img(
    path: str, size: Union[tuple[int, int], float] = None
) -> ImageTk.PhotoImage:
    """
    This should load images.
    The size parameter can be:
        A tuple of ints, for resizing;
        A float, for indicating a percentage to resize; or
        None, to keep original size.
    """

    if size is None:
        return ImageTk.PhotoImage(Image.open(path))

    if isinstance(size, tuple):
        return ImageTk.PhotoImage(Image.open(path).resize(size))

    if isinstance(size, float):
        img = Image.open(path)
        new_size = tuple(int(length * size) for length in img.size)
        return ImageTk.PhotoImage(img.resize(new_size))

    raise ValueError("Expected size to be either a tuple of ints, a float or None.")


def rm_bg(
    img_path: str,
    model_path: str = "./models/u2net_human_seg.pth",
    alpha_matting: bool = True,
) -> None:
    """
    This function will remove the background of a given image. It should receive a JPG image path.
    It will create and save a JPG image with white background.
    """

    input_img_path, output_img_path = process_img_path(img_path)

    # Opening/reading image as bytes.
    with open(input_img_path, "rb") as input_as_bytes:
        input_img = input_as_bytes.read()

    # Removing background from image using u2net_human_seg.
    output_as_bytes = bg.remove(
        input_img, alpha_matting=alpha_matting, model_name=model_path
    )
    # Converting the output as bytes to a PIL Image.
    pil_img = Image.open(io.BytesIO(output_as_bytes))

    # Tuple representing the new RGB background color (the image we get from rembg is a transparent
    # PNG).
    fill_color = (255, 255, 255)
    pil_img = pil_img.convert("RGBA")
    if pil_img.mode in ("RGBA", "LA"):
        # Removing transparency and making background white.
        background = Image.new(pil_img.mode[:-1], pil_img.size, fill_color)
        background.paste(pil_img, pil_img.split()[-1])  # omit transparency
        pil_img = background

    # Saving the new image in the same folder with a similar name.
    pil_img.convert("RGB").save(output_img_path)


def process_img_path(img_path: str) -> tuple[str, str]:
    """
    Expects an image path. If it isn't one of the expected extensions, it will raise a ValueError.
    Outputs the processed input image path and output path (to save final image).
    """
    # Making sure we got the correct input.
    dot_pos = img_path.rfind(".")
    if dot_pos == -1 or not img_path[dot_pos + 1 :].lower() in ["jpg", "jpeg"]:
        raise ValueError("Expected JPG images.")

    # Replacing "\" to "/" because *Windows*.
    input_img_path = img_path.replace("\\", "/")
    output_img_path = img_path[:dot_pos] + "_NO_BG.jpg"

    return (input_img_path, output_img_path)


# def check_model(model_path: str) -> None:
# if not os.exists(model_path):


if __name__ == "__main__":
    raise SystemExit(main())
