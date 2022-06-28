"""
This module will run various tests on 4 functions from "project.py".
    1. project.model_exists(...)
    2. project.process_img_path(...)
    3. project.check_image_type(...)
    4. project.load_img(...)
"""

from multiprocessing.pool import ThreadPool
from tkinter import Tk
import pytest
import project


@pytest.mark.parametrize(
    "model_path",
    [
        "",
        "cat",
        "dog",
        "100",
        "CS50",
        "u2net",
        "u2net_human_seg",
        "u2net_human_seg.pthhah",
        "u2net_human_seg.pth.png",
        "u2net_human_seg.pth/png",
        ".pth.",
        ".pth.pth!",
        ".pth\\",
        "u2net_human_seg.pth and ML",
        False,
        True,
        0,
        1,
        2,
        2.2,
        None,
    ],
)
def test_model_exists_value_errors(model_path: str) -> None:
    """
    Asserting ValueErros are raised.
    """

    # Asserting were getting the correct error.
    with pytest.raises(ValueError):
        project.model_exists(model_path)


@pytest.mark.parametrize(
    "model_path",
    [
        "./model.pth",
        "./u2net.pth",
        "./u2net_human_seg.pth",
        "./models/u2net_human_seg.pth",
        project.os.path.expanduser(
            project.os.path.join(
                "~", ".u2net", "there_should_not_be_any_model_with_this_name.pth"
            )
        ),
    ],
)
def test_model_exists_returns_false(
    model_path: str,
) -> None:
    """
    Asserting project.model_exists returns False for nonexistent models.
    """
    # Making it clear what is being asserted.
    expected_output: bool = False
    # Asserting were getting the expected output
    assert project.model_exists(model_path) == expected_output


def test_model_exists() -> None:
    """
    Asserting project.model_exists returns True. This will attempt to download the model
    if it doesn't exist yet.
    """
    # Creating model name.
    model_path: str = project.os.path.expanduser(
        project.os.path.join("~", ".u2net", "u2net_human_seg.pth")
    )
    # Downloading model.
    project.download_model(model_path=model_path)

    # Making it clear what is being asserted.
    expected_output: bool = True
    # Asserting were getting the expected output
    assert project.model_exists(model_path=model_path) == expected_output


@pytest.mark.parametrize(
    "image_path",
    [
        "",
        "cat",
        "dog",
        "100",
        "CS50",
        "u2net",
        "u2net_human_seg",
        "u2net_human_seg.pthhah",
        "u2net_human_seg.pthpng",
        "u2net_human_seg.pth/png",
        ".pth.",
        ".pth.pth!",
        ".pth\\",
        "u2net_human_seg.pth and ML",
        False,
        True,
        0,
        1,
        2,
        2.2,
        None,
        "jpg",
        "jpeg",
        "png",
        "catpng",
        "dog.png.",
        "./dog.png.mov",
        "./somefolder/dog.png.gif",
        "dog.mov",
    ],
)
def test_process_img_path_value_errors(image_path: str) -> None:
    """
    Asserting ValueErros are raised.
    """

    # Asserting were getting the correct error.
    with pytest.raises(ValueError):
        project.process_img_path(image_path)


@pytest.mark.parametrize(
    "image_path_input, image_path_output",
    [
        ("my_image.jpg", ("my_image.jpg", "my_image_NO_BG.jpg")),
        ("my_image.jpeg", ("my_image.jpeg", "my_image_NO_BG.jpeg")),
        ("my_image.png", ("my_image.png", "my_image_NO_BG.png")),
        ("path/to/myimg.jpg", ("path/to/myimg.jpg", "path/to/myimg_NO_BG.jpg")),
        ("path/to/myimg.jpeg", ("path/to/myimg.jpeg", "path/to/myimg_NO_BG.jpeg")),
        ("path/to/myimg.png", ("path/to/myimg.png", "path/to/myimg_NO_BG.png")),
        ("./my_image.jpg", ("./my_image.jpg", "./my_image_NO_BG.jpg")),
        ("./my_image.jpeg", ("./my_image.jpeg", "./my_image_NO_BG.jpeg")),
        ("./my_image.png", ("./my_image.png", "./my_image_NO_BG.png")),
        (".\\my_image.jpg", ("./my_image.jpg", "./my_image_NO_BG.jpg")),
        (".\\my_image.jpeg", ("./my_image.jpeg", "./my_image_NO_BG.jpeg")),
        (".\\my_image.png", ("./my_image.png", "./my_image_NO_BG.png")),
        (".\\my.image.jpg", ("./my.image.jpg", "./my.image_NO_BG.jpg")),
        (".\\my.image.jpeg", ("./my.image.jpeg", "./my.image_NO_BG.jpeg")),
        (".\\my.image.png", ("./my.image.png", "./my.image_NO_BG.png")),
        (".\\etc\\my.img.jpg", ("./etc/my.img.jpg", "./etc/my.img_NO_BG.jpg")),
        (".\\etc\\my.img.jpeg", ("./etc/my.img.jpeg", "./etc/my.img_NO_BG.jpeg")),
        (".\\etc\\my.img.png", ("./etc/my.img.png", "./etc/my.img_NO_BG.png")),
    ],
)
def test_process_img_path(image_path_input, image_path_output) -> None:
    """
    Asserting project.model_exists returns False for inexistent models.
    """
    # Asserting were getting the expected output
    assert project.process_img_path(image_path_input) == image_path_output


@pytest.mark.parametrize(
    "image_path",
    [
        "",
        "cat",
        "dog",
        "100",
        "CS50",
        "u2net",
        "u2net_human_seg",
        "u2net_human_seg.pthhah",
        "u2net_human_seg.pthpng",
        "u2net_human_seg.pth/png",
        ".pth.",
        ".pth.pth!",
        ".pth\\",
        "u2net_human_seg.pth and ML",
        False,
        True,
        0,
        1,
        2,
        2.2,
        None,
        "jpg",
        "jpeg",
        "png",
        "cat.png.mp4",
        "dog.png.mov",
        "./dog.png.",
        "./somefolder/dog.png.",
        "dog.mov",
    ],
)
def test_check_image_type_value_errors(image_path: str) -> None:
    """
    Asserting ValueErros are raised.
    """

    # Asserting were getting the correct error.
    with pytest.raises(ValueError):
        project.check_image_type(image_path)


@pytest.mark.parametrize(
    "image_path, output",
    [
        ("my_image.jpg", ("my_image.jpg".rfind("."), "jpg")),
        ("my_image.jpeg", ("my_image.jpeg".rfind("."), "jpeg")),
        ("path/to/myimg.jpg", ("path/to/myimg.jpg".rfind("."), "jpg")),
        ("path/to/myimg.jpeg", ("path/to/myimg.jpeg".rfind("."), "jpeg")),
        ("./my_image.jpg", ("./my_image.jpg".rfind("."), "jpg")),
        ("./my_image.jpeg", ("./my_image.jpeg".rfind("."), "jpeg")),
        (".\\my_image.jpg", (".\\my_image.jpg".rfind("."), "jpg")),
        (".\\my_image.jpeg", (".\\my_image.jpeg".rfind("."), "jpeg")),
        (".\\my.image.jpg", (".\\my.image.jpg".rfind("."), "jpg")),
        (".\\my.image.jpeg", (".\\my.image.jpeg".rfind("."), "jpeg")),
        (".\\etc\\my.img.jpg", (".\\etc\\my.img.jpg".rfind("."), "jpg")),
        (".\\etc\\my.img.jpeg", (".\\etc\\my.img.jpeg".rfind("."), "jpeg")),
    ],
)
def test_check_image_type(image_path, output) -> None:
    """
    Asserting project.check_image_type works properly.
    """
    # Asserting were getting the expected output
    assert project.check_image_type(image_path) == output


@pytest.mark.parametrize(
    "image_path",
    [
        "",
        "cat",
        "dog",
        "100",
        "CS50",
        "u2net",
        "u2net_human_seg",
        "u2net_human_seg.pthhah",
        "u2net_human_seg.pthpng",
        "u2net_human_seg.pth/png",
        ".pth.",
        ".pth.pth!",
        ".pth\\",
        "u2net_human_seg.pth and ML",
        False,
        True,
        0,
        1,
        2,
        2.2,
        None,
        "jpg",
        "jpeg",
        "png",
        "cat.png.gif",
        "dog.png.gif",
        "./dog.png.gif",
        "./somefolder/dog.png.gif",
        "dog.mov",
    ],
)
def test_load_img_path_value_errors(image_path: str) -> None:
    """
    Asserting ValueErros are raised for wrong path inputs.
    """

    # Asserting were getting the correct error.
    with pytest.raises(ValueError):
        project.load_img(image_path)


@pytest.mark.parametrize(
    "image_path, size",
    [
        ("./images/cs50cat.png", (1.1, 1.1)),
        ("./images/cs50cat.png", (1.1, 1)),
        ("./images/cs50cat.png", (1, 1.1)),
        ("./images/cs50cat.png", (0, 0)),
        ("./images/cs50cat.png", (0, 1)),
        ("./images/cs50cat.png", (1, 0)),
        ("./images/cs50cat.png", (-1, -1)),
        ("./images/cs50cat.png", (-1, 1)),
        ("./images/cs50cat.png", (1, -1)),
        ("./images/cs50cat.png", (None, None)),
        ("./images/cs50cat.png", (None, 1)),
        ("./images/cs50cat.png", (1, None)),
        ("./images/cs50cat.png", (False, False)),
        ("./images/cs50cat.png", (False, 1)),
        ("./images/cs50cat.png", (1, False)),
        ("./images/cs50cat.png", (True, True)),
        ("./images/cs50cat.png", (True, 1)),
        ("./images/cs50cat.png", (1, True)),
        ("./images/cs50cat.png", ("1", "1")),
        ("./images/cs50cat.png", ("1", 1)),
        ("./images/cs50cat.png", (1, "1")),
        ("./images/cs50cat.png", ("", "")),
        ("./images/cs50cat.png", ("", 1)),
        ("./images/cs50cat.png", (1, "")),
        ("./images/cs50cat.png", True),
        ("./images/cs50cat.png", False),
        ("./images/cs50cat.png", 0),
        ("./images/cs50cat.png", -1),
        ("./images/cs50cat.png", "two"),
        ("./images/cs50cat.png", "2"),
        ("./images/cs50cat.png", "2.2"),
        ("./images/cs50cat.png", "2.2"),
    ],
)
def test_load_img_size_value_errors(image_path: str, size) -> None:
    """
    Asserting ValueErros are raised for wrong size inputs.
    """

    # Asserting were getting the correct error.
    with pytest.raises(ValueError):
        project.load_img(image_path, size)


@pytest.mark.parametrize(
    "image_path, size",
    [
        ("./images/cs50cat.png", None),
        ("./images/cs50cat.png", (1, 1)),
        ("./images/cs50cat.png", 1),
        ("./images/cs50cat.png", 1.0),
        ("./images/cs50cat.png", 2),
        ("./images/cs50cat.png", 2.5),
    ],
)
def test_load_img(image_path: str, size) -> None:
    """
    Asserting correct behavior.
    """

    def run_tk(image_path: str, size):
        """
        This function will get the img_tk_size. This should be ran using threading to
        reduce chances of a bug I couldn't understand how it happens nor a better way
        to handle it.
        """
        # Creating Tk instance as it is necessary for ImageTk to work properly.
        root = Tk()

        # Processing image with load_img function.
        img_tk = project.load_img(image_path, size)

        # Getting image size.
        img_tk_size = (img_tk.width(), img_tk.height())

        # Closing window.
        root.after(0, root.destroy)
        root.mainloop()
        del root

        return img_tk_size

    # Getting img_tk_size asynchronously:
    pool = ThreadPool(processes=1)
    async_result = pool.apply_async(run_tk, (image_path, size))
    img_tk_size = async_result.get()

    # This should work the same as the above "async code", but it results in a pytest error
    # that I don't really understand (an error when calling "Tk()"):
    # img_tk_size = run_tk(image_path, size)

    # Getting original image size
    img_pil_size = project.Image.open(image_path).size

    # Asserting were getting the expected output
    if size is None:
        assert img_tk_size == img_pil_size
        return

    if isinstance(size, tuple):
        assert img_tk_size == size
        return

    assert img_tk_size == (int(img_pil_size[0] * size), int(img_pil_size[1] * size))
