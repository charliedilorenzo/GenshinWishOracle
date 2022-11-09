import tkinter as tk
from tkinter import ttk as ttk

class entry_box_and_button():
    def __init__(self, button_text, width, button_height, box_bg = "White", box_fg = "Black", button_bg = "White", button_fg = "Black", box_text = ""):
        self.frame = tk.Frame()
        self.box =  tk.Entry(master=self.frame,fg=box_fg, bg=box_bg, width=width, text=box_text)
        self.button =  tk.Button(
            master=self.frame,
            text=button_text,
            width=width,
            height=button_height,
            bg=button_bg,
            fg=button_fg,)
        self.box.pack()
        self.button.pack()

    def get_box_value(self):
        return self.box.get()

    def button_click(self):
        return self.get_box_value()

    def clear_box(self):
        self.box.delete(0,tk.END)

def entry_box(width, height, bg="White", fg="Black"):
    entry = tk.Entry(fg=fg, bg=bg, width=width)
    return entry

def button(text, width, height, bg = "White", fg = "Black"):
    button =  tk.Button(
    text=text,
    width=width,
    height=height,
    bg=bg,
    fg=fg,)
    return button

def handle_keypress(event):
    """Print the character associated to the key pressed"""
    print(event.char)


def gui():
    window = tk.Tk()
    box_button = entry_box_and_button("Submit contents", 30, 5)
    box_button.frame.pack()
    greeting = tk.Label(text="Hello, Tkinter")
    greeting.pack()

    # Bind keypress event to handle_keypress()
    window.bind("<Key>", handle_keypress)

    window.mainloop()
    return 0

if __name__ == "__main__":
    gui()