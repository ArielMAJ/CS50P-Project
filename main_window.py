"""
This module implements the app's main window class.
"""

from ctypes import windll
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Callable

# import customtkinter  # type: ignore[import]


class MainWindow(tk.Tk):
    """
    All the app's main functionality should be acessible through this window.
    """

    def __init__(
        self,
        *,
        functions: dict[str, Callable],
    ):
        super().__init__()
        self.withdraw()

        self.functions: dict[str, Callable] = functions
        self.widgets: dict = {}
        # self.vars: dict = {}
        self.settings: dict = {
            "padx": 2,
            "pady": 1,
            "title": "Remove Background",
            # "font": ("Arial", 12),
        }

        self.colors: dict[str, str] = {
            "yellow": "#FCE388",
            "blue": "#C2CEFF",
            "red": "#B52C30",
            "green": "#256A49",
            "gray": "#525a49",
            "app_bg_color": "#22223b",
            "app_bg_light_color": "#4a4e69",
            "app_fg_color": "#f2e9e4",
        }
        self.frames: dict = {}
        self.selected_images: list[str] = []
        self._click_event = None

        # self.after(50, self._load_window)
        self._load_window()

    def _load_window(self):
        """
        This function will call subfunctions to load the app.
        """
        self._basic_configs()
        self._place_menu_bar()
        self._place_widgets()
        self._place_window_on_screen()

    def _basic_configs(self):
        """
        This function should contain all basic configurations such as:
        - Loading images/files/etc;
        - Creating variables (StringVar, IntVar, etc);
        """
        # self._check_and_load_settings()

        self.title(self.settings["title"])
        # self.minsize(width=800, height=600)
        self.resizable(width=False, height=False)

        self.config(bg=self.colors["app_bg_color"])

        # self.vars["image_paths"] = tk.StringVar()
        # self.vars["image_paths"].set("None")
        self.frames["menu"] = tk.Frame(self, bg="black", relief="raised", bd=0)
        self.frames["menu"].pack(side=tk.TOP, expand=1, fill=tk.BOTH)

        self.frames["app"] = tk.Frame(
            self, height=100, bg=self.colors["app_bg_color"], relief="raised", bd=0
        )
        self.frames["app"].pack(
            side=tk.TOP, padx=20, pady=(20, 30), expand=1, fill=tk.BOTH
        )

        self.iconphoto(
            False, self.functions["load_img"]("./images/cs50cat.png", (40, 40))
        )

        # self.grid_rowconfigure(0, weight=1)
        # self.grid_columnconfigure(1, weight=1)
        self._overrideredirect(True)
        # self.lift()

    def _place_menu_bar(self):
        """
        This function should handle the menu bar creation.
        """

        def turn_label_into_button(label, command=None):
            label.bind("<Button-1>", lambda e: label.configure(relief="sunken"))
            label.bind(
                "<ButtonRelease-1>",
                lambda e: label.configure(relief="raised"),
            )

            if command is not None:
                label.bind(
                    "<ButtonRelease-1>", lambda e: self.after(100, command), add="+"
                )

        self.widgets["menu_exit"] = tk.Label(
            self.frames["menu"],
            fg=self.colors["app_fg_color"],
            # fg=self.colors["app_bg_light_color"],
            bg="gray",
            relief="raised",
            text="✖",  # Change folder
            width=3,
            height=1,
        )
        self.widgets["menu_exit"].pack(side=tk.RIGHT)
        turn_label_into_button(self.widgets["menu_exit"], self.destroy)

        self.widgets["menu_help"] = tk.Label(
            self.frames["menu"],
            fg=self.colors["app_fg_color"],
            bg="gray",
            relief="raised",
            text="Help",  # Change folder
            width=5,
            height=1,
        )
        self.widgets["menu_help"].pack(side=tk.LEFT)

        with open("./README.md", encoding="utf-8") as file:
            message = file.read()
        turn_label_into_button(
            self.widgets["menu_help"],
            lambda: messagebox.showinfo(
                title="Help",
                message=message,
                icon="question",
            ),
        )

        self.widgets["menu_title"] = tk.Label(
            self.frames["menu"],
            fg=self.colors["app_fg_color"],
            bg="black",
            # relief="raised",
            text=self.settings["title"],  # Change folder
            # width=5,
            justify="left",
            # height=1,
        )
        self.widgets["menu_title"].pack(side=tk.LEFT, expand=1, fill=tk.X)

        self.widgets["menu_title"].bind(
            "<B1-Motion>",
            lambda event: self.geometry(
                f"+{event.x_root - self._click_event.x -58}+{event.y_root - self._click_event.y}"
            ),
        )

        def click_event_fun(event):
            self._click_event = event

        self.widgets["menu_title"].bind("<Button-1>", click_event_fun)

    def _place_widgets(self):
        """
        This function should handle the non-menubar widgets.
        """

        self.widgets["lbl_selected_images"] = tk.Label(
            self.frames["app"],
            text="Images to process:",
            # Set "bg" to "self.colors["app_bg_color"]" once all widgets are placed.
            # bg="#9a8c98",
            bg=self.colors["app_bg_color"],
            fg=self.colors["app_fg_color"],
            # width=30,
            anchor="w",
            # justify="left",
        )
        self.widgets["lbl_selected_images"].grid(
            row=0,
            column=0,
            columnspan=2,
            padx=self.settings["padx"],
            pady=0,
            sticky="NEWS",
        )

        self.widgets["lbx_image_paths"] = tk.Listbox(
            self.frames["app"],
            # textvariable=self.vars["image_paths"],
            # Set "bg" to "self.colors["app_bg_color"]" once all widgets are placed.
            # bg="blue",  # self.colors["app_bg_color"],
            width=30,
            fg=self.colors["app_fg_color"],
            bg=self.colors["app_bg_light_color"],
            # selectmode=tk.MULTIPLE,
            highlightthickness=0,
            relief=tk.FLAT,
            height=5,
            bd=3,
            # anchor="nw",
            justify="left",
        )
        self.widgets["lbx_image_paths"].insert(0, "Empty")
        self.widgets["lbx_image_paths"].grid(
            row=1,
            column=0,
            rowspan=5,
            padx=self.settings["padx"],
            pady=(0, self.settings["pady"]),
            sticky="NEWS",
        )

        self.widgets["btn_add"] = tk.Button(
            self.frames["app"],
            fg=self.colors["app_fg_color"],
            bg=self.colors["app_bg_light_color"],
            text="Add",  # Change folder
            width=8,
            command=self.add_images_button_press,
        )
        self.widgets["btn_add"].grid(
            row=1,
            column=1,
            # rowspan=2,
            padx=self.settings["padx"],
            pady=(self.settings["pady"], 0),
            sticky="NEWS",
        )

        self.widgets["btn_remove"] = tk.Button(
            self.frames["app"],
            fg=self.colors["app_fg_color"],
            bg=self.colors["app_bg_light_color"],
            # Remove background (all subfolders)
            text="Remove",
            width=8,
            # height=1,
            command=self.remove_image_from_list_button_press,
        )
        self.widgets["btn_remove"].grid(
            row=3,
            column=1,
            # rowspan=1,
            padx=self.settings["padx"],
            pady=0,  # self.settings["pady"],
            sticky="NEWS",
        )
        self.widgets["btn_clear"] = tk.Button(
            self.frames["app"],
            # Remove background (all subfolders)
            text="Clear",
            width=8,
            fg=self.colors["app_fg_color"],
            bg=self.colors["app_bg_light_color"],
            # height=1,
            command=self.clear_listbox_button_press,
        )
        self.widgets["btn_clear"].grid(
            row=4,
            column=1,
            # rowspan=1,
            padx=self.settings["padx"],
            pady=0,  # self.settings["pady"],
            sticky="NEWS",
        )

        self.widgets["btn_rembg"] = tk.Button(
            self.frames["app"],
            # Remove background (all subfolders)
            text="Apply",
            width=8,
            fg=self.colors["app_fg_color"],
            bg=self.colors["app_bg_light_color"],
            # height=1,
            command=self.rembg_button_press,
        )
        self.widgets["btn_rembg"].grid(
            row=5,
            column=1,
            # rowspan=1,
            padx=self.settings["padx"],
            pady=0,  # self.settings["pady"],
            sticky="NEWS",
        )

    def _place_window_on_screen(self):
        self.update()
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()
        offset = {
            "x": int(0.5 * self.winfo_screenwidth() - width // 2),
            "y": int(0.5 * self.winfo_screenheight() - height // 2 - 20),
        }
        # print(self.winfo_screenwidth(), self.winfo_width())
        # print(self.winfo_screenheight(), self.winfo_height())
        # print(offset, self.geometry())
        self.geometry(f"{width}x{height}+{offset['x']}+{offset['y']}")

    def rembg_button_press(
        self,
        model_path: str = "./models/u2net_human_seg.pth",
        alpha_matting: bool = False,
    ) -> None:
        """
        Implementation of the background removing button.

        - This should open a file navigator dialog to get an amount of image paths.
        - These images should all be JPGs.
        - If no image is selected the function should return. If any amount of images
        are selected, they should have their background removed.
        """
        if not self.selected_images:
            messagebox.showinfo(
                title="Wait... wut?",
                message="No images were selected. Select at least one before pressing this button.",
                parent=self,
            )
            return
        threads: list = []
        for pos, image_path in enumerate(self.selected_images):
            threads.append(
                threading.Thread(
                    target=rm_bg,
                    args=(
                        image_path,
                        model_path,
                        alpha_matting,
                    ),
                )
            )
            threads[pos].start()

        messagebox.showinfo(
            title="Wait...",
            message=(
                "This can take a while, specially if you select many. "
                + "Please press OK and wait all images to be processed."
            ),
            parent=self,
        )
        for thread in threads:
            thread.join()

        messagebox.showinfo(
            # Finished
            title="Done!",
            # Backgrounds removed successfully!
            message="All background were successfully removed!",
            parent=self,
            # This specific icon removes the bell noise from the messagebox.
            # icon="question",
        )

    def add_images_button_press(self) -> None:
        """
        This will open a folder navigator dialog to get a folder path.
        This will update the settings.json file if a folder is selected and is different from the
        current one. It will also update the label showing the current selected folder.
        """
        selected_images = filedialog.askopenfilenames(
            # initialdir=r"/",
            # Select JPG images to remove background
            title="Select images to remove background.",
            filetypes=(
                ("Images", "*.jpg"),  # Images
                ("Images", "*.jpeg"),  # Images
                ("Images", "*.png"),  # Images
                ("All files", "*.*"),  # All files.
            ),
        )
        if not selected_images:
            return

        lbx_items = self.widgets["lbx_image_paths"].get(0, tk.END)
        if lbx_items[0] == "Empty":
            self.widgets["lbx_image_paths"].delete(0)

        img_names_to_insert: list[str] = []
        ignored_images: list[str] = []

        for img_path in selected_images:
            img_name = img_path.split("/")[-1]
            if img_name in lbx_items:
                ignored_images.append(img_name)
            else:
                img_names_to_insert.append(img_name)

        # for image_path in selected_images:

        self.selected_images.extend(selected_images)
        self.widgets["lbx_image_paths"].insert(
            tk.END,
            *img_names_to_insert,
        )

        if ignored_images:
            messagebox.showinfo(
                title="Images already selected.",
                message="Some of the selected images were ignored, as they were already selected:"
                + f"\n{ignored_images}",
            )

    def _list_is_empty(self) -> bool:
        if not self.selected_images:
            messagebox.showinfo(
                title="List already empty",
                message="The image list is already empty.",
            )
            return True
        return False

    def remove_image_from_list_button_press(self):
        """
        Gets the listbox's cursor selection and removes the selected path from it.
        """
        if self._list_is_empty():
            return

        selected = self.widgets["lbx_image_paths"].curselection()
        if not selected:
            messagebox.showinfo(
                title="No image selected",
                message="Please select an image to remove from the list.",
            )
            return

        selected_text = self.widgets["lbx_image_paths"].get(selected)
        for img_path in self.selected_images:
            if img_path.split("/")[-1] == selected_text:
                self.selected_images.remove(img_path)
                break
        self.widgets["lbx_image_paths"].delete(selected)
        if not self.widgets["lbx_image_paths"].get(0, tk.END):
            self.widgets["lbx_image_paths"].insert(0, "Empty")

    def clear_listbox_button_press(self):
        """
        Deletes everything in the listbox.
        """
        if self._list_is_empty():
            return
        self.widgets["lbx_image_paths"].delete(0, tk.END)
        self.widgets["lbx_image_paths"].insert(0, "Empty")
        self.selected_images.clear()

    def _overrideredirect(self, boolean=None):
        """
        Stackoverflow solution to make it so overrideredirect doesn't stop the app from showing
        when the user alt+tab or wants to click on it from the taskbar.
        https://stackoverflow.com/questions/63217105/tkinter-overridedirect-minimizing-and-windows-task-bar-issues
        """
        self.overrideredirect(boolean)
        gwl_exstyle = -20
        ws_ex_appwindow = 0x00040000
        ws_ex_toolwindow = 0x00000080
        if boolean:
            hwnd = windll.user32.GetParent(self.winfo_id())
            style = windll.user32.GetWindowLongW(hwnd, gwl_exstyle)
            style = style & ~ws_ex_toolwindow
            style = style | ws_ex_appwindow
            windll.user32.SetWindowLongW(hwnd, gwl_exstyle, style)


def main() -> int:
    """
    This function exists for easily testing this module "directly". This will skip  the loading
    screen.
    """
    from project import load_img, rm_bg

    functions: dict[str, Callable] = {
        "load_img": load_img,
        "rm_bg": rm_bg,
    }
    root = MainWindow(functions=functions)
    root.deiconify()
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
