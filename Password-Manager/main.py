from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json
import secrets
import string
import random



# ---------------------------- PASSWORD FINDER ------------------------------- #
def find_password():
    try:
        with open("data.json") as file:
            passwords = json.load(file)
    except FileNotFoundError:
        messagebox.showwarning(title="Oops", message="No Data File Found")
    else:
        if web_entry.get() in passwords:
            messagebox.showinfo(
                title=f"{web_entry.get()}",
                message=f"Here's your details: "
                        f""
                        f"\nemail: {passwords[web_entry.get()]['email']} "
                        f"\npassword: {passwords[web_entry.get()]['password']}"
            )
        else:
            messagebox.showwarning(title="Error", message=f"No details for {web_entry.get()} exists yet!")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generator():
    #Changing the length of the PSW (x value) Recomended: [4-12]
    x = 5
    minUpper = random.randint(3, x)
    minLower = random.randint(2, x)
    minDigits = random.randint(1, x)
    minSpec = random.randint(1, x)
    password = ""
     

    for i in range(minUpper):
        password += "".join(random.choice(secrets.choice(string.ascii_uppercase)))

    for i in range(minLower):
        password += "".join(random.choice(secrets.choice(string.ascii_lowercase)))

    for i in range(minDigits):
        password += "".join(random.choice(secrets.choice(string.digits)))

    for i in range(minSpec):
        password += "".join(random.choice(secrets.choice(string.punctuation)))

    password = list(password)
    random.shuffle(password)
    
    my_password = "".join(password)

    password_entry.insert(0, my_password)
    pyperclip.copy(my_password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    new_data = {
        web_entry.get(): {
            "email": email_entry.get(),
            "password": password_entry.get(),
        }
    }
    if len(web_entry.get()) == 0 or len(password_entry.get()) == 0:
        messagebox.showwarning(title="Oops", message="Please, make sure you don't leave any fields empty!")
    else:
        try:
            with open("data.json", "r") as file_path:
                #Reading old data
                data = json.load(file_path)
        except FileNotFoundError:
            with open("data.json", "w") as file_path:
                # Saving updated data
                json.dump(new_data, file_path, indent=4)
        else:
            #Updating old data with new data
            data.update(new_data)
            with open("data.json", "w") as file_path:
                #Saving updated data
                json.dump(data, file_path, indent=4)

        is_okay = messagebox.askokcancel(
            title=f"{web_entry.get()}",
            message=f"These are the details entered! \nEmail: {email_entry.get()} "
                    f"\nPassword: {password_entry.get()} \n\nIs it okay to save?"
        )
        if is_okay:
            web_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("☯ Simple Password Manager ☯")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=250)
logo_img = PhotoImage(file="x.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

website = Label(text="Account:")
website.grid(column=0, row=1)

web_entry = Entry(width=32)
web_entry.grid(column=1, row=1)
web_entry.focus()

search = Button(text="Search", width=15, command=find_password)
search.grid(column=2, row=1)

email = Label(text="Email/Username:")
email.grid(column=0, row=2)

email_entry = Entry(width=51)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(END, "email@gmail.com")

password = Label(text="Password:")
password.grid(column=0, row=3)

password_entry = Entry(width=32)
password_entry.grid(column=1, row=3)

pass_button = Button(text="Generate Password", command=password_generator)
pass_button.grid(column=2, row=3)

add_button = Button(text="Add", width=44, command=save)
add_button.grid(column=1, row=4, columnspan=2)



window.mainloop()