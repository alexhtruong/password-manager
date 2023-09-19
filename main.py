from tkinter import *
from tkinter import messagebox
import random
import pyperclip 
import json

# ---------------------------- PASSWORD SEARCH ------------------------------- #
def find_password():
    website = website_input.get()
    try:
        with open("data.json", 'r') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="No Data File Found", message="No Data File Found")
    else:
        if website in data:
            email = data[website]['email/username']
            encrypted_password = data[website]['password']
            messagebox.showinfo(title="Email/Password", message=
                                f"Email: {email}\n"
                                f"Password: {encrypted_password}"
                                )
        else:
            messagebox.showinfo(title="No info found", message=f"No details for the {website} exists.")
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)
    
    password_input.delete(0, "end")  #clear pre-existing text

    password_letters = [random.choice(letters) for char in range(nr_letters)]
    password_symbols = [random.choice(symbols) for char in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for char in range(nr_numbers)]
    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    password = "".join(password_list)
    password_input.insert(0, password)
    pyperclip.copy(password)
# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_entry():
    # Getting input data
    website = website_input.get()
    username = username_input.get()
    password = password_input.get()
    new_data = {website: {
        "email/username": username,
        "password": password,
        }
    }

    # empty fields
    if website.strip() == "" or username.strip() == "" or password.strip() == "":
        messagebox.showinfo(title="Missing Input", message="Please don't leave any fields empty!")
        return

    try:
        with open("data.json", "r") as d:
            json.load(d)
    except FileNotFoundError:
        with open("data.json", "w") as d:
            json.dump(new_data, encrypted, indent=4)

    # Check for duplicates
    with open("data.json", "r") as data_file:
        data = json.load(data_file)
        if website in data and username == data[website]["email/username"]:
            is_edit = messagebox.askyesno(title="Duplicate Entry",
                                          message="This combination of website and username already exists. Do you "
                                                  "want to edit it?")
            if is_edit:
                try:
                    with open("data.json", "r") as d:  # loading data
                        json.load(d)
                except FileNotFoundError:  # if data file not found create new data file
                    with open("data.json", "w") as d:
                        json.dump(new_data, d, indent=4)
                else:
                    # update the existing entry
                    data.update(new_data)
                    with open("data.json", 'w') as d:
                        json.dump(data, d, indent=4)
            else:
                website_input.delete(0, "end")
                username_input.delete(0, "end")
                password_input.delete(0, "end")
                return
        else:
            with open("data.json", "w") as d:
                data.update(new_data)
                # saving updated data
                json.dump(data, d, indent=4)

    website_input.delete(0, "end")
    username_input.delete(0, "end")
    password_input.delete(0, "end")
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# MyPass Image
canvas = Canvas(width=200, height=200, highlightthickness=0)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

# Website label and input form
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)
website_input = Entry(width=35)
website_input.insert(0, "Facebook")
website_input.grid(column=1, row=1, columnspan=2)

# Email/Password search
search_button = Button(text="Search", command=find_password)
search_button.grid(column=3, row=1, columnspan=2)

# Email/Username
username_label = Label(text="Email/Username:")
username_label.grid(column=0, row=2)
username_input = Entry(width=35)
username_input.insert(0, "username123@gmail.com")
username_input.grid(column=1, row=2, columnspan=2)

# Password
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)
password_input = Entry(width=23)
password_input.grid(column=1, row=3)
password_button = Button(text="Generate Password", command=generate_password) 
password_button.grid(column=2, row=3, columnspan=2)

# Add entries
add_button = Button(text="Add", width=36, command=add_entry)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()
