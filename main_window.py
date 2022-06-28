"""
This module implements the app's main window class.
"""

import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Callable

import customtkinter  # type: ignore[import]

# Modes: system (default), light, dark
customtkinter.set_appearance_mode("dark")

# Themes: blue (default), dark-blue, green
customtkinter.set_default_color_theme("sweetkind")


class MainWindow(customtkinter.CTk):
    """
    All the app's main functionality should be acessible through this window.
    """

    def __init__(
        self,
        *,
        functions: dict[str, Callable],
    ):
        super().__init__()

        self.functions: dict[str, Callable] = functions
        self.widgets: dict = {}

        self.selected_images: list[str] = []

        self._load_app()

    def _load_app(self):
        """
        This function will call subfunctions to load the app.
        """
        # self.withdraw()
        self.set_scaling(1, 1, 1)
        self._basic_configs()
        self._place_widgets()
        self._place_window_on_screen()
        # self.deiconify()

    def _basic_configs(self):
        """
        This function should contain all basic configurations such as:
            - Loading images/files/etc;
            - Creating variables (StringVar, IntVar, etc);
            - Configuring columns and rows;
        """
        self.title("Remove Background")
        self.resizable(width=False, height=False)

        self.iconphoto(
            False, self.functions["load_img"]("./images/cs50cat.png", (40, 40))
        )

        self.grid_rowconfigure(0, weight=2, minsize=10)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(6, weight=2, minsize=30)

        # self.grid_columnconfigure(0, uniform=10)
        self.grid_columnconfigure(0, weight=1, minsize=10)
        self.grid_columnconfigure(1, weight=100)
        # self.grid_columnconfigure(2, weight=100)
        self.grid_columnconfigure(5, weight=1, minsize=10)

    def _place_widgets(self):
        """
        This function should handle the creating and placing of widgets.
        """

        self.widgets["lbl_selected_images"] = customtkinter.CTkLabel(
            self,
            text="Images to process:",
            anchor="sw",
        )
        self.widgets["lbl_selected_images"].grid(
            row=1,
            column=1,
            pady=0,
            padx=0,
            ipady=0,
            sticky="w",
        )

        self.widgets["lbx_image_paths"] = tk.Listbox(
            self,
            width=40,
            bg="#4a4e69",
            highlightthickness=0,
            relief="flat",
            bd=3,
            # selectmode=tk.MULTIPLE,
        )
        self.widgets["lbx_image_paths"].insert(0, "Empty")
        self.widgets["lbx_image_paths"].grid(
            row=2,
            column=1,
            columnspan=2,
            rowspan=4,
            pady=(1, 1),
            padx=(20, 0),
            sticky="NEWS",
        )

        self.widgets["btn_add"] = customtkinter.CTkButton(
            self,
            corner_radius=13,
            text="  Add          ",
            image=self.functions["load_img"]("images/add_white.png", (60, 60)),
            compound="left",
            command=self.add_images_button_press,
        )
        self.widgets["btn_add"].grid(
            row=2,
            column=4,
            pady=(0, 5),
            padx=(8, 15),
            sticky="NEWS",
        )

        self.widgets["btn_remove"] = customtkinter.CTkButton(
            self,
            corner_radius=13,
            text="  Remove    ",
            image=self.functions["load_img"]("images/minus_white.png", (60, 60)),
            command=self.remove_image_from_list_button_press,
        )
        self.widgets["btn_remove"].grid(
            row=3,
            column=4,
            pady=5,
            padx=(8, 15),
            sticky="NEWS",
        )
        self.widgets["btn_clear"] = customtkinter.CTkButton(
            self,
            text="  Clear         ",
            corner_radius=13,
            image=self.functions["load_img"]("images/cross_white.png", (60, 60)),
            command=self.clear_listbox_button_press,
        )
        self.widgets["btn_clear"].grid(
            row=4,
            column=4,
            pady=5,
            padx=(8, 15),
            sticky="NEWS",
        )

        self.widgets["btn_apply"] = customtkinter.CTkButton(
            self,
            text="  Apply         ",
            corner_radius=13,
            image=self.functions["load_img"]("images/check_white.png", (60, 60)),
            command=self.apply_button_press,
        )
        self.widgets["btn_apply"].grid(
            row=5,
            column=4,
            # rowspan=1,
            pady=(5, 0),
            padx=(8, 15),
            sticky="NEWS",
        )

        with open("./help.txt", encoding="utf-8") as file:
            message = file.read()

        self.widgets["btn_help"] = customtkinter.CTkButton(
            master=self,
            image=self.functions["load_img"]("images/help_crop.png", 0.09),
            text="",
            width=28,
            border_width=0,
            corner_radius=1000,
            fg_color=None,
            hover_color="#212435",
            command=lambda: messagebox.showinfo(
                title="Help",
                message=message,
                icon="question",
            ),
        )
        self.widgets["btn_help"].grid(
            row=0,
            rowspan=2,
            column=4,
            columnspan=1,
            padx=(0, 15),
            pady=10,
            sticky="se",
        )

    def _place_window_on_screen(self):
        # self.update()
        # self.withdraw()
        # width = self.winfo_reqwidth()
        # height = self.winfo_reqheight()
        # offset = {
        #     "x": int(0.5 * self.winfo_screenwidth() - width // 2),
        #     "y": int(0.5 * self.winfo_screenheight() - height // 2 - 20),
        # }
        # print(width, height, offset)

        # self.geometry(f"{width}x{height}+{offset['x']}+{offset['y']}")
        self.geometry(f"{698}x{434}+{611}+{303}")

    def apply_button_press(
        self,
        # model_name: str = "u2net_human_seg.pth",
        alpha_matting: bool = False,
        file_id_to_dowload_model_from: str = "1-Yg0cxgrNhHP-016FPdp902BR-kSsA4P",
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
                message="No images were added. Add at least one before pressing this button.",
                parent=self,
            )
            return

        if not self.functions["model_exists"]():
            should_download = messagebox.askyesno(
                title="Model is not present in the expected folder.",
                message="Model for removing background not found, should it be downloaded?"
                + " You can't remove background without it.",
                parent=self,
            )
            if should_download:
                self.functions["download_model"](
                    # model_name=model_name,
                    file_id_to_dowload_model_from=file_id_to_dowload_model_from,
                    parent_window=self,
                )
            else:
                return

        # model_name: str = "u2net_human_seg",
        threads: list = []
        for pos, image_path in enumerate(self.selected_images):
            threads.append(
                threading.Thread(
                    target=self.functions["rm_bg"],
                    args=(
                        image_path,
                        # model_name,
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
            title="Done!",
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
            title="Select images to remove background.",
            filetypes=(
                ("Images", "*.jpg"),
                ("Images", "*.jpeg"),
                ("Images", "*.png"),
                ("All files", "*.*"),
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


def main() -> int:
    """
    This function exists for easily testing this module "directly". This will skip  the loading
    screen. Background removing won't work if this is executed.
    """
    # pylint: disable=import-error, import-outside-toplevel, cyclic-import
    from project import functions

    root = MainWindow(functions=functions)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
