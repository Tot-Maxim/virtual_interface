from tkinter import *
import subprocess

def run_shell_script():
    try:
        password = password_entry.get()
        command = f"echo {password} | sudo -S ./run.sh"
        subprocess.Popen(command, shell=True)
        label.config(text="Start sh file successful", fg='white')
    except Exception as e:
        label.config(text=f"Error: {e}", fg='red')

window = Tk()
window.geometry("820x450")
window.title('Test GUI program')
window.config(background='black')

icon = PhotoImage(file='logo.png')
window.iconphoto(True, icon)

button = Button(window, text="Press to run run.sh", command=run_shell_script, bg='black', fg='white')
button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

password_label = Label(window, text="Enter sudo password:", fg='white', bg='black')
password_label.grid(row=1, column=0, padx=10, pady=(30, 10), sticky="e")

password_entry = Entry(window, show='*')
password_entry.grid(row=1, column=1, padx=10, pady=(30, 10), sticky="w")

label = Label(window, text="", fg='white', bg='black')
label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

window.mainloop()