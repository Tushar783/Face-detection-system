import tkinter as tk
from tkinter import messagebox, PhotoImage, simpledialog
from firebase import firebase
from PIL import Image, ImageTk

firebase_url = 'https://faceattendancrecognitionsystem-default-rtdb.firebaseio.com/'
firebase = firebase.FirebaseApplication(firebase_url, None)


def get_next_id():
    # Fetch the current counter value from Firebase
    current_count = firebase.get('/counter', None)
    if current_count is None:
        current_count = 0
    # Increment the counter by 1
    next_id = current_count + 1
    # Update the counter value in Firebase
    firebase.put('/', 'counter', next_id)
    return str(next_id).zfill(5)


def preview_data():
    name = name_entry.get().strip().upper()
    roll_number = roll_number_entry.get().strip()
    branch = branch_entry.get().strip().upper()
    starting_year = starting_year_entry.get().strip()
    attendance = attendance_entry.get().strip()
    last_attendance_marked = last_attendance_entry.get().strip()

    if not roll_number.isdigit():
        messagebox.showerror("Error", "University Roll Number must be a numerical value.")
        return

    if not starting_year.isdigit() or not (2015 <= int(starting_year) <= 2030):
        messagebox.showerror("Error", "Starting year must be a number between 2015 and 2030.")
        return

    preview_text = f"Name: {name}\nUniversity Roll Number: {roll_number}\nBranch: {branch}\nStarting Year: {starting_year}\nAttendance: {attendance}\nLast Attendance Marked: {last_attendance_marked}"

    # Display preview in a pop-up window
    edit = messagebox.askyesno("Preview", preview_text + "\n\nDo you want to edit?")
    if edit:
        edit_data()
    else:
        submit_data()


def edit_data():
    global name_entry, roll_number_entry, branch_entry, starting_year_entry, attendance_entry, last_attendance_entry

    name_entry.delete(0, tk.END)
    name_entry.insert(0, simpledialog.askstring("Edit", "Name:"))

    roll_number_entry.delete(0, tk.END)
    roll_number_entry.insert(0, simpledialog.askstring("Edit", "University Roll Number:"))

    branch_entry.delete(0, tk.END)
    branch_entry.insert(0, simpledialog.askstring("Edit", "Branch:"))

    starting_year_entry.delete(0, tk.END)
    starting_year_entry.insert(0, simpledialog.askstring("Edit", "Starting Year:"))

    attendance_entry.delete(0, tk.END)
    attendance_entry.insert(0, simpledialog.askstring("Edit", "Attendance:"))

    last_attendance_entry.delete(0, tk.END)
    last_attendance_entry.insert(0, simpledialog.askstring("Edit", "Last Attendance Marked:"))


def submit_data():
    name = name_entry.get().strip().upper()
    roll_number = roll_number_entry.get().strip()
    branch = branch_entry.get().strip().upper()
    starting_year = starting_year_entry.get().strip()
    attendance = attendance_entry.get().strip()
    last_attendance_marked = last_attendance_entry.get().strip()

    data = {
        'ID': get_next_id(),
        'Name': name,
        'University_Roll_Number': roll_number,
        'Branch': branch,
        'Starting_Year': starting_year,
        'Attendance': attendance,
        'Last_Attendance_Marked': last_attendance_marked
    }

    result = firebase.post('/students', data)
    print("Data submitted successfully:", result)


# Create main window
root = tk.Tk()
root.title("Firebase Data Entry")
root.geometry("1300x960")

# Load the background image
bg_image = Image.open("Resources/background.png")
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create entry fields with lambda functions for validation
tk.Label(root, text="Name:", bg='white').grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1, padx=5, pady=5)
name_entry.config(validate="key", validatecommand=(root.register(lambda text: text.strip().upper()), "%P"))

tk.Label(root, text="University Roll Number:", bg='white').grid(row=1, column=0, padx=5, pady=5)
roll_number_entry = tk.Entry(root)
roll_number_entry.grid(row=1, column=1, padx=5, pady=5)
roll_number_entry.config(validate="key", validatecommand=(root.register(lambda text: text.isdigit()), "%P"))

tk.Label(root, text="Branch:", bg='white').grid(row=2, column=0, padx=5, pady=5)
branch_entry = tk.Entry(root)
branch_entry.grid(row=2, column=1, padx=5, pady=5)
branch_entry.config(validate="key", validatecommand=(root.register(lambda text: text.strip().upper()), "%P"))

tk.Label(root, text="Starting Year:", bg='white').grid(row=3, column=0, padx=5, pady=5)
starting_year_entry = tk.Entry(root)
starting_year_entry.grid(row=3, column=1, padx=5, pady=5)
starting_year_entry.config(validate="key", validatecommand=(
root.register(lambda text: text.isdigit() and 2015 <= int(text) <= 2030), "%P"))

tk.Label(root, text="Attendance:", bg='white').grid(row=4, column=0, padx=5, pady=5)
attendance_entry = tk.Entry(root)
attendance_entry.grid(row=4, column=1, padx=5, pady=5)

tk.Label(root, text="Last Attendance Marked:", bg='white').grid(row=5, column=0, padx=5, pady=5)
last_attendance_entry = tk.Entry(root)
last_attendance_entry.grid(row=5, column=1, padx=5, pady=5)

# Create preview and submit buttons
preview_button = tk.Button(root, text="Preview", command=preview_data)
preview_button.grid(row=6, column=0, padx=5, pady=5)

submit_button = tk.Button(root, text="Submit", command=submit_data)
submit_button.grid(row=6, column=1, padx=5, pady=5)

root.mainloop()
