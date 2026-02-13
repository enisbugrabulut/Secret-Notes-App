import tkinter
from tkinter import PhotoImage, StringVar
import os
import sys

screen = tkinter.Tk()
screen.title("Secret Notes")
screen.geometry("400x750")


def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

base_dir = get_base_path()
file_path = os.path.join(base_dir, "my_secret.txt")
file_path_tk = StringVar()
txt_created = False

def save_encrypt_message():
    if txt_created:
        with open(file_path, "a") as f:
            f.write(f"\n{title_entry.get()}\n{message_text.get("0.0", "end-1c")}")
            title_entry.delete(0, "end")
            message_text.delete(1.0, tkinter.END)
    else:
        with open(file_path, "w") as f:
            f.write(f"{title_entry.get()}\n{message_text.get("0.0", "end-1c")}")
            title_entry.delete(0, "end")
            message_text.delete(1.0, tkinter.END)
    """
    add here the function of encrypt for adding encrypted message instead of normal message to txt file
    add here a variable to hold the key for using later to decrypt the message
    add here a mechanism to control if the title_entry, message_text and master_key_entry are not empty
    If empty, give popup error and do not
    """

def decrypt_message():
    """
    add here to ability of read the txt and decrypt the message
    when you copy the encrypted message, you will need the key. If you don't enter the key, program will give you popup error
    do the popup error box
    """

    pass

def show_filepath():
    if os.path.exists(file_path):
        file_path_tk.set(file_path)
        path_entry.config(textvariable=file_path_tk)
        global txt_created
        txt_created = True

image = PhotoImage(file="./assets/secret.png")

image_label = tkinter.Label(image=image)
image_label.pack(pady=(10,0))

path_label = tkinter.Label(text="Your secret .txt file's path", font=("Arial Bold", 15, "bold"))
path_label.pack(pady=(15,0))
path_entry = tkinter.Entry(width=50, font=("Arial Bold", 10))
path_entry.pack()

title_label = tkinter.Label(text="Title of the Secret Note", font=("Arial Bold", 15, "bold"))
title_label.pack(pady=(10,5))
title_entry = tkinter.Entry(width=40, font=("Arial Bold", 10, "bold"))
title_entry.pack()
title_entry.focus()

message_label = tkinter.Label(text="The Secret Note", font=("Arial Bold", 18, "bold"))
message_label.pack(pady=(10,5))
message_text = tkinter.Text(width=50, height=15, font=("Arial Bold", 10, "bold"))
message_text.pack()

key_label = tkinter.Label(text="Secret Key", font=("Arial Bold", 15, "bold"))
key_label.pack(pady=(10,5))
key_entry = tkinter.Entry(width=40, font=("Arial Bold", 10, "bold"))
key_entry.pack()

save_encrypt_button = tkinter.Button(text="Save & Encrypt", width=18, height=1, font=("Arial Bold", 8), command=save_encrypt_message)
save_encrypt_button.pack(pady=(20,5))

decrypt_button = tkinter.Button(text="Decrypt", width=12, height=1, font=("Arial Bold", 8), command=decrypt_message)
decrypt_button.pack(pady=(5,5))

if __name__ == "__main__":
    show_filepath()
    screen.mainloop()