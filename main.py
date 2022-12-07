from tkinter import *
from tkinter import messagebox
from random import randint,shuffle,choice
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():

    letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    numbers = ['0','1','2','3','4','5','6','7','8','9']
    symbols = ['!','#','$','%','&','(',')','*','+']

    password_letters = [ choice(letters) for char in range(randint(8,10)) ]
    password_symbols = [ choice(symbols) for _ in range(randint(2,4)) ]
    password_numbers = [ choice(numbers) for _ in range(randint(2,4)) ]
    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)
    password = "".join(password_list)
    password_entry.insert(0,password)
    pyperclip.copy(password)
# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():

    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Ooops",message="Please don't leave any of fields empty")
    else:
        try:
            with open("data.json",mode="r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json",mode="w") as data_file:
                json.dump(new_data,data_file,indent=4)
        else:
            data.update(new_data)
            with open("data.json",mode="w") as data_file:
                json.dump(data,data_file,indent=4)
        finally:
            email_entry.delete(0,END)
            website_entry.delete(0,END)

# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()
    try:
        with open("data.json",mode="r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error",message="No Data File Found.")
    else:
        if website in data:
            password = data[website]["password"]
            email = data[website]["email"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error",message=f"No details for the {website} exists")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=20,pady=20)


logo_img = PhotoImage(file = "logo.png")

canvas = Canvas(width=200,height=200)
canvas.create_image(100,100,image=logo_img)
canvas.grid(row=0,column=1)

website_label = Label(text="Website")
website_label.grid(row=1,column=0)
email_label = Label(text="Email/Username")
email_label.grid(row=2,column=0)
password_label = Label(text="Password")
password_label.grid(row=3,column=0)

website_entry = Entry(width=21)
website_entry.grid(row=1,column=1)
email_entry = Entry(width=40)
email_entry.insert(0,"usainbolt@gmail.com")
email_entry.grid(row=2,column=1,columnspan=2)
password_entry = Entry(width=21)
password_entry.grid(row=3,column=1)

search_button = Button(text="Search",width=15,command=find_password)
search_button.grid(row=1,column=2)
generate_button = Button(text="Generate Password",command=generate_password)
generate_button.grid(row=3,column=2)
add_button = Button(text="Add",width=36,command=save)
add_button.grid(row=4,column=1,columnspan=2)

window.mainloop()