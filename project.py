"""
Main script for loading this app.
Display loading screen -> Load app in the "background" -> Destroy loading screen and display main
screen.
"""


import io
import os
import threading
from tkinter import messagebox
from typing import Union, Callable
from ctypes import windll

import requests  # type: ignore[import]
from PIL import Image, ImageTk  # type: ignore[import]

import main_window  # type: ignore[import]
from loading_screen import LoadingScreen  # type: ignore[import]


def importer():
    """
    This import is really slow when loading the app. Importing it either inside the function that
    uses it or in a different thread feels like it makes for a better user experience.
    """
    # pylint: disable=invalid-name, global-variable-not-assigned
    global bg
    # pylint: disable=import-outside-toplevel
    from rembg import bg  # type: ignore[import]


windll.shcore.SetProcessDpiAwareness(1)


def main() -> int:
    """
    This function will start the app.
    """
    # This will force loading screen to stay up until rembg is imported (it is a slow import).
    loading_screen = LoadingScreen(
        wait_for=[imp_th],
        load_img=load_img,
    )
    loading_screen.mainloop()

    root = main_window.MainWindow(functions=functions)
    root.mainloop()

    return 0


def load_img(
    image_path: str, size: Union[tuple[int, int], float | int] = None
) -> ImageTk.PhotoImage:
    """
    This should load images.
    The size parameter can be:
        A tuple of ints, for resizing;
        A float or int, for indicating a percentage to resize; or
        None, to keep original size.
    """

    # Reusing checks
    check_image_type(image_path)

    if size is None:
        return ImageTk.PhotoImage(Image.open(image_path))

    if (
        isinstance(size, tuple)
        and isinstance(size[0], int)
        and isinstance(size[1], int)
        and not isinstance(size[0], bool)
        and not isinstance(size[1], bool)
    ):
        if size[0] <= 0 or size[1] <= 0:
            raise ValueError("Size should have positive values.")
        return ImageTk.PhotoImage(Image.open(image_path).resize(size))

    if isinstance(size, (float, int)) and not isinstance(size, bool):
        if size <= 0:
            raise ValueError("Size should be a positive value.")
        img = Image.open(image_path)
        new_size = tuple(int(length * size) for length in img.size)
        return ImageTk.PhotoImage(img.resize(new_size))

    raise ValueError(
        "Expected size to be either a tuple of ints, a float, int or None."
    )


def rm_bg(
    image_path: str,
    # model_name: str = "u2net_human_seg",
    alpha_matting: bool = True,
) -> None:
    """
    This function will remove the background of a given image. It should receive a JPG image path.
    It will create and save a JPG image with white background.
    """

    input_img_path, output_img_path = process_img_path(image_path)

    # Opening/reading image as bytes.
    with open(input_img_path, "rb") as input_as_bytes:
        input_img = input_as_bytes.read()

    model_name: str = "u2net_human_seg"
    # Removing background from image using u2net_human_seg.
    output_as_bytes = bg.remove(  # type: ignore[name-defined]  # pylint: disable=undefined-variable
        input_img,
        alpha_matting=alpha_matting,
        model_name=model_name,
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


def check_image_type(image_path: str) -> tuple[int, str]:
    """
    Reusable function for checking image type.
        - Receives a string with the path to an image.
        - Outputs the position of the last dot and the extension of the file.
        - Raises a value error if the image type isn't in the accepted image
        types list.
    """
    accepted_image_types = ["jpg", "jpeg", "png"]
    if (
        not isinstance(image_path, str)
        or (dot_pos := image_path.rfind(".")) == -1
        or not (file_type := image_path[dot_pos + 1 :].lower()) in accepted_image_types
    ):
        raise ValueError("Expected a JPG or PNG image path.")

    return dot_pos, file_type


def process_img_path(image_path: str) -> tuple[str, str]:
    """
    Expects an image path. If it isn't one of the expected extensions, it will raise a ValueError.
    Outputs the processed input image path and output path (to save final image).
    """
    # Making sure we got the correct input.
    dot_pos, file_type = check_image_type(image_path)

    # Replacing "\" to "/" because *Windows*.
    input_img_path = image_path.replace("\\", "/")
    output_img_path = input_img_path[:dot_pos] + "_NO_BG." + file_type

    return (input_img_path, output_img_path)


def model_exists(
    model_path: str = os.path.expanduser(
        os.path.join("~", ".u2net", "u2net_human_seg.pth")
    )
) -> bool:
    """
    Expects a "model_path" to check if the file exists.
    Raises value error if the path isn't of the correct expected type
    """
    if not isinstance(model_path, str) or model_path.split(".")[-1] != "pth":
        raise ValueError(
            'Wrong file type. Expected ".pth". eg.: "path/to/u2model.pth".'
        )

    return os.path.exists(model_path)


def download_model(
    model_path: str = os.path.expanduser(
        os.path.join("~", ".u2net", "u2net_human_seg.pth")
    ),
    file_id_to_dowload_model_from: str = "1-Yg0cxgrNhHP-016FPdp902BR-kSsA4P",
    parent_window=None,
) -> None:
    """
    Expects a "model_path" to check if the file exists.
    Current version of rembg expects all models to be in "~/.u2net".
    If the file doesn't exist it will download from "file_id_to_dowload_model_from" and save it.
    The file ID is a google drive ID.

    If a parent_window is passed in, it will open a message box over it with more info.
    """

    def model_from_google_drive(file_id: str, destination: str) -> None:
        """
        Expects a (google drive) file ID and a destination to save it.
        Reference: https://stackoverflow.com/a/39225039
        """
        url = "https://docs.google.com/uc?export=download"

        session = requests.Session()
        response = session.get(url, params={"id": file_id}, stream=True)
        response = session.get(url, params={"id": file_id, "confirm": "t"}, stream=True)

        chunk_size = 32768
        with open(destination, "wb") as file:
            for chunk in response.iter_content(chunk_size):
                if chunk:  # filters out keep-alive new chunks
                    file.write(chunk)

    if model_exists(model_path):
        message = "Model has already been downloaded."
        if parent_window is not None:
            messagebox.showinfo(
                parent=parent_window,
                title="Done!",
                message=message,
            )
        else:
            print(message)
        return

    model_path = model_path.replace("\\", "/")
    pos = model_path.rfind("/")
    folder_path = model_path[:pos]

    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    download_model_thread = threading.Thread(
        target=model_from_google_drive,
        args=(file_id_to_dowload_model_from, model_path),
    )
    download_model_thread.start()

    message = (
        "Downloading can take a few minutes depending on your internet connection."
        + " Please be patient!"
    )
    if parent_window is not None:
        messagebox.showinfo(
            parent=parent_window,
            title="Download has started.",
            message=message
            + " The program will purposefully stop responding until download is complete. "
            + "Another pop up message will show up when it's done.",
        )
    else:
        print(message)

    download_model_thread.join()

    message = "Download finished successfully!"
    if parent_window is not None:
        messagebox.showinfo(
            parent=parent_window,
            title="Done.",
            message=message,
        )
    else:
        print(message)


functions: dict[str, Callable] = {
    "load_img": load_img,
    "rm_bg": rm_bg,
    "model_exists": model_exists,
    "download_model": download_model,
}


if __name__ == "__main__":
    imp_th = threading.Thread(target=importer)
    imp_th.start()
    raise SystemExit(main())
