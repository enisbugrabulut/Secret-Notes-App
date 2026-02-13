import tkinter
from tkinter import PhotoImage, StringVar
import tkinter.messagebox as messagebox
import os
import sys
from cryptography.fernet import Fernet, InvalidToken
import hashlib
import base64

screen = tkinter.Tk()
screen.title("Secret Notes")
screen.resizable(False, False)

def center_screen(window):
    width = 400
    height = 750
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

base_dir = get_base_path()
file_path = os.path.join(base_dir, "my_secret.txt")
file_path_tk = StringVar()
txt_created = False

def save_message():
    if title_entry.get() != "" and message_text.get("0.0", "end-1c") != "" and key_entry.get() != "":
        if txt_created:
            with open(file_path, "a") as f:
                f.write(f"\n{title_entry.get()}"
                        f"\n{encrypt_message().decode()}")
                title_entry.delete(0, "end")
                message_text.delete(1.0, tkinter.END)
                key_entry.delete(0, "end")

        else:
            with open(file_path, "w") as f:
                f.write(f"{title_entry.get()}\n{encrypt_message()}")
                title_entry.delete(0, "end")
                message_text.delete(1.0, tkinter.END)

    else:
        print("POP UP ERROR. YOU NEED TO FILL ALL AREAS")
        messagebox.showerror("Input Error", "You need to fill all information !")

def create_key(key_text):
    hash_obj = hashlib.sha256(key_text.encode())
    return base64.urlsafe_b64encode(hash_obj.digest())

def encrypt_message():
    text = message_text.get("0.0", "end-1c")
    key_text = key_entry.get()
    key = create_key(key_text)
    f = Fernet(key)
    encrypted_message = f.encrypt(text.encode("utf-8"))
    return encrypted_message

def decrypt_message():
    if message_text.get("0.0", "end-1c") != "" and key_entry.get() != "":
        encrypted_text = message_text.get("0.0", "end-1c")
        if search_text(file_path, encrypted_text):
            key_text = key_entry.get()
            key = create_key(key_text)
            f = Fernet(key)
            try:
                decrypted_message = f.decrypt(encrypted_text.encode()).decode()
                message_text.delete("1.0", "end")
                message_text.insert("end", decrypted_message)
            except InvalidToken:
                fake_text = base64.b64encode(encrypted_text[::-1].encode()).decode()[:len(encrypted_text)]
                message_text.delete("1.0", "end")
                message_text.insert("end", fake_text)
        else:
            messagebox.showerror("Input Error", "The encoded content is not exist !")
    else:
        messagebox.showerror("Input Error", "You need to fill all information !")

def search_text(file_of_path, checking_text):
    with open(file_of_path, 'r') as f:
        all_text = f.read()
        if checking_text in all_text:
            return True
        else:
            return False

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

save_encrypt_button = tkinter.Button(text="Save & Encrypt", width=18, height=1, font=("Arial Bold", 8), command=save_message)
save_encrypt_button.pack(pady=(20,5))

decrypt_button = tkinter.Button(text="Decrypt", width=12, height=1, font=("Arial Bold", 8), command=decrypt_message)
decrypt_button.pack(pady=(5,5))

show_filepath()
center_screen(screen)

screen.mainloop()