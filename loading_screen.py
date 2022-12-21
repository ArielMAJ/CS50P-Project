"""
This module implements the loading screen class.
"""

from tkinter import Tk, Label  # Toplevel
from typing import Callable, Union
from PIL import ImageTk  # type: ignore[import]


class LoadingScreen(Tk):
    """
    This top level will create a loading screen and display it for a given amount of seconds.
    It can accept a list of threads to wait for before closing itself and showing the main screen.
    """

    def __init__(
        self,
        # parent: Tk,
        *,
        seconds: float = 0.5,
        load_img: Callable[[str, Union[tuple[int, int], float]], ImageTk.PhotoImage],
        wait_for: list | None = None,
    ):
        super().__init__()
        # self.parent = parent
        self.seconds: float = seconds
        self.photo_image: ImageTk.PhotoImage = load_img("./images/cs50p.png", 0.6)

        if wait_for is None:
            wait_for = []
        self.wait_for: list = wait_for

        self._draw_window()
        self._wait()

    def _draw_window(self) -> None:

        label = Label(self, image=self.photo_image, bg="#010101")
        label.place(x=0, y=0)

        self.withdraw()
        self.geometry(f"{self.photo_image.width()}x{self.photo_image.height()}")
        # self.update()

        offset = {
            "x": int(0.5 * self.winfo_screenwidth() - self.photo_image.width() // 2),
            "y": int(0.5 * self.winfo_screenheight() - self.photo_image.height() // 2),
        }
        self.geometry(f"+{offset['x']}+{offset['y']}")

        self.overrideredirect(True)
        # self.attributes("-topmost", True)

        # The two following options don't seem to work on Ubuntu
        self.attributes("-disabled", True)
        self.attributes("-transparentcolor", "#010101")

        self.attributes("-alpha", 0.8)

        self.lift()
        self.deiconify()

    def _wait(self) -> None:
        # self.parent._load_window()
        # self.parent.withdraw()
        # self.parent.update()
        # self.parent.withdraw()
        self.lift()

        miliseconds = int(self.seconds * 1000)
        for thread in self.wait_for:
            self.after(miliseconds + 50, thread.join)

        # self.after(miliseconds + 100, self.parent.deiconify)
        # self.after(miliseconds + 150, self.parent.lift)
        self.after(miliseconds + 200, self.destroy)


def main() -> int:
    """
    This function exists for easily testing this module "directly". This will only shows the loading
    screen and then a blank screen (this won't load main screen).
    """
    # pylint: disable=import-error, import-outside-toplevel, cyclic-import
    # root = Tk()
    from project import load_img

    root = LoadingScreen(seconds=2, load_img=load_img)
    # root.after(4000, root.destroy)
    print("hi")
    root.mainloop()
    print("hello")

    # root = Tk()

    root = LoadingScreen(seconds=2, load_img=load_img)
    # root.after(4000, root.destroy)
    print("hi")
    root.mainloop()
    print("hello")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
