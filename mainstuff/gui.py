import tkinter as tk
from tkinter import ttk as ttk


class entry_box_and_button():
    def __init__(self, frame, button_text, width, button_height, box_bg="White", box_fg="Black", button_bg="White", button_fg="Black", box_text="") -> None:
        self.box = tk.Entry(master=frame, fg=box_fg,
                            bg=box_bg, width=width, text=box_text)
        self.button = tk.Button(
            master=frame,
            text=button_text,
            width=width,
            height=button_height,
            bg=button_bg,
            fg=button_fg, command=self.button_click)
        self.box.pack()
        self.button.pack()

    def get_box_value(self):
        return self.box.get()

    def clear_box(self):
        self.box.delete(0, tk.END)

    def button_click(self):
        print(self.get_box_value())
        return self.get_box_value()


def entry_box(width, height, bg="White", fg="Black"):
    entry = tk.Entry(fg=fg, bg=bg, width=width)
    return entry


def button(text, width, height, bg="White", fg="Black"):
    button = tk.Button(
        text=text,
        width=width,
        height=height,
        bg=bg,
        fg=fg,)
    return button


def handle_keypress(event):
    """Print the character associated to the key pressed"""
    # print(event.char)
    pass


def gui():
    root = tk.Tk()
    home = tk.Frame(root)
    box_button = entry_box_and_button(home, "Submit contents", 30, 5)
    home.pack()
    greeting = tk.Label(text="Hello, Tkinter")
    greeting.pack()

    # Bind keypress event to handle_keypress()
    root.bind("<Key>", handle_keypress)

    root.mainloop()
    return 0


if __name__ == "__main__":
    gui()
