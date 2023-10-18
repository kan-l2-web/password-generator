import customtkinter as ctk
import main as password
from string import ascii_lowercase, ascii_uppercase, digits, punctuation
from tkinter import END, StringVar, IntVar, messagebox
from widgets.table import CTkTable
from PIL import Image
from tkinter.constants import BOTH, NSEW, SW, W, NS
from db import Encrypter


class App(ctk.CTk):
    def __init__(self):
        super(App, self).__init__()

        self.title('PasGen')
        self.iconbitmap('./icon_64.ico')
        self.tk.call("source", "./Themes/azure.tcl")
        self.tk.call("set_theme", "dark")
        self.resizable(False, False)

        self.isLower = StringVar()
        self.isSymbol = StringVar()
        self.isUpper = StringVar()
        self.isNumber = StringVar()

        self.sliderLength = IntVar(value=20)
        self.font_face = "Inconsolata"

        self.setup_widgets()

    def setup_widgets(self):
        self.frame = ctk.CTkFrame(
            master=self,
            fg_color="transparent"
            )
        self.frame.pack(padx=10, pady=20)

        self.side_bar = ctk.CTkFrame(
            master=self.frame,
            fg_color="transparent",
            )
        self.side_bar.grid(column=0, row=0, padx=(5, 5), pady=(5, 5))

        self.logo_frame = ctk.CTkFrame(
            master=self.side_bar,
            width=100,
            height=100,
            fg_color="transparent"
            )
        self.logo_frame.grid(column=0, row=0, sticky=NSEW)

        self.logo = ctk.CTkImage(
            dark_image=Image.open("logo.png"), size=(42, 42))
        self.label1 = ctk.CTkLabel(
            text="",
            master=self.logo_frame,
            image=self.logo
            )
        self.label1.grid(
            column=0,
            row=0,
            pady=(5, 5),
            padx=(5, 5),
            sticky=W
            )

        self.label2 = ctk.CTkLabel(
            master=self.logo_frame,
            text='PasGen',
            font=(self.font_face, 24, "bold")
            )
        self.label2.grid(
            column=1,
            row=0,
            pady=(5, 5),
            padx=(5, 5),
            sticky=W
            )

        self.widgets_frame = ctk.CTkFrame(
            master=self.side_bar,
            border_width=1,
            fg_color="transparent"
            )
        self.widgets_frame.grid(column=0, row=1, sticky=NSEW, pady=20)

        pady = (5, 5)
        padx = (10, 0)

        self.upper_check = ctk.CTkCheckBox(
            master=self.widgets_frame,
            text="Include Uppercase letter",
            variable=self.isUpper,
            onvalue=ascii_uppercase,
            offvalue="",
            font=(self.font_face, 14, "bold")
            )
        self.upper_check.pack(anchor=SW, padx=padx, pady=pady)

        self.lower_check = ctk.CTkCheckBox(
            master=self.widgets_frame,
            text="Include Lowercase letter",
            variable=self.isLower,
            onvalue=ascii_lowercase,
            offvalue="",
            font=(self.font_face, 14, "bold")
            )
        self.lower_check.pack(anchor=SW, padx=padx, pady=pady)

        self.number_check = ctk.CTkCheckBox(
            master=self.widgets_frame,
            text="Include numbers",
            variable=self.isNumber,
            onvalue=digits,
            offvalue="",
            font=(self.font_face, 14, "bold")
            )
        self.number_check.pack(anchor=SW, padx=padx, pady=pady)

        self.symbol_check = ctk.CTkCheckBox(
            master=self.widgets_frame,
            text="Include symbols",
            variable=self.isSymbol,
            onvalue=punctuation,
            offvalue="",
            font=(self.font_face, 14, "bold")
            )
        self.symbol_check.pack(anchor=SW, padx=padx, pady=pady)

        self.settings_frame = ctk.CTkFrame(
            master=self.side_bar,
            bg_color="transparent",
            fg_color="transparent"
            )
        self.settings_frame.grid(column=0, row=2, sticky=NS, pady=(0, 10))

        self.slider_label = ctk.CTkLabel(
            anchor=W,
            master=self.settings_frame,
            text="Character length:",
            font=(self.font_face, 14, "bold")
            )
        self.slider_label.grid(column=0, row=0, sticky=NSEW)

        self.slider_length = ctk.CTkEntry(
            master=self.settings_frame,
            width=7,
            font=(self.font_face, 14, "bold"),
            textvariable=self.sliderLength
            )
        self.slider_length.grid(column=1, row=0, sticky=NSEW)

        self.slider = ctk.CTkSlider(
            master=self.settings_frame,
            from_=0,
            to=100,
            variable=self.sliderLength,
            command=self.slider_change_value
            )
        self.slider.grid(sticky=NSEW, columnspan=2, row=1, column=0)

        self.action_frame = ctk.CTkFrame(
            master=self.side_bar,
            bg_color="transparent",
            fg_color="transparent"
            )
        self.action_frame.grid(column=0, row=3, sticky=NSEW)

        padx = 5
        pady = 10

        self.entry = ctk.CTkEntry(
            master=self.action_frame,
            font=(self.font_face, 14, "bold")
            )
        self.entry.grid(
            column=0,
            row=0,
            columnspan=2,
            padx=(10, 10),
            pady=(5, 5),
            sticky=NSEW
            )

        self.gen_btn = ctk.CTkButton(
            master=self.action_frame,
            text="Generate",
            command=self.generate,
            font=(self.font_face, 14, "bold")
            )
        self.gen_btn.grid(column=0, row=1, padx=padx, pady=(0, 5), sticky=NSEW)

        self.db_btn = ctk.CTkButton(
            master=self.action_frame,
            text="Add Data",
            font=(self.font_face, 14, "bold"),
            command=self.add_data
            )
        self.db_btn.grid(column=1, row=1, padx=padx, pady=(0, 5), sticky=NSEW)

        self.table_frame = ctk.CTkFrame(
            master=self.frame,
            fg_color="transparent"
            )
        self.table_frame.grid(column=1, row=0)

        self.en = Encrypter("./Cryptus.db")
        data = self.en.get_data()
        self.tree = CTkTable(master=self.table_frame, values=data)
        self.tree.pack(fill=BOTH, expand=True, padx=(10, 10), pady=(10, 10))

    def get_char(self):
        chars = "".join(self.isLower.get() + self.isSymbol.get()
                        + self.isNumber.get() + self.isUpper.get())
        return chars

    def slider_change_value(self, value):
        self.slider_length.delete(0, "end")
        self.slider_length.insert(0, int(value))

    def spinbox_change_value(self):
        self.slider.set(str(self.sliderLength.get()))

    def add_data(self):
        self.en.add_password(password=str(self.entry.get()))
        self.entry.delete(0, END)

    def generate(self):
        if not self.get_char():
            messagebox.showerror(
                title="CheckBox Error",
                message='Select the items to generate a password'
                )
        else:
            self.entry.delete(0, 'end')
            self.entry.insert(
                0,
                password.create_new(
                    length=int(self.slider.get()),
                    chars=self.get_char())
                )


if __name__ == "__main__":
    app = App()
    app.mainloop()
