import os
import tkinter as tk
from tkinter import Image, Tk, Label, Entry, Button, Toplevel, messagebox, simpledialog
from tkinter import filedialog
from PIL import Image  # Ensure Pillow is installed

class AdminOptions:
    def __init__(self, root, auth_system):
        self.root = Toplevel(root)
        self.auth_system = auth_system

        self.root.title("Admin Options")
        self.root.geometry("400x300")

        Label(self.root, text="Admin Options", font=("Helvetica", 16)).pack(pady=10)

        # Button for viewing all users
        Button(self.root, text="View All Users", command=self.view_all_users).pack(pady=5)
        
        # Button for searching a user
        Button(self.root, text="Search User", command=self.search_user).pack(pady=5)
        
        # Button for logging out
        Button(self.root, text="Logout", command=self.logout).pack(pady=10)

    def view_all_users(self):
        # Display information about all users in the system
        users = self.auth_system.users
        if users:
            user_info = "\n".join([user.display_info() for user in users])
            messagebox.showinfo("All Users", user_info)
        else:
            messagebox.showinfo("All Users", "No users found.")

    def search_user(self):
        # Search for a specific user by email
        email = simpledialog.askstring("Search User", "Enter the email of the user:")
        if email:
            user = next((u for u in self.auth_system.users if u.email == email), None)
            if user:
                messagebox.showinfo("User Found", user.display_info())
            else:
                messagebox.showerror("Error", "User not found.")

    def logout(self):
        # Close the admin options window and show the main login window
        self.root.destroy()
        self.root.master.deiconify()


class FileHandler:
    def __init__(self, file_name="users.txt"):
        # Use os.path to ensure compatibility across platforms
        self.file_name = os.path.abspath(file_name)

    def read_users_from_file(self):
        users = []
        try:
            with open(self.file_name, "r") as file:
                lines = file.readlines()
                for line in lines:
                    user_info = line.strip().split("-")
                    
                    if len(user_info) < 3:
                        continue
                    
                    user_type = user_info[0]
                    email = user_info[1]
                    name = user_info[2]
                    password = user_info[3] if len(user_info) > 3 else None
                    if user_type == "Patient" and len(user_info) >= 5:
                        age = user_info[4]
                        medical_history = user_info[5]
                        users.append(Patient(email, name, password, age, medical_history))
                    elif user_type == "Admin" and len(user_info) == 4:
                        users.append(Admin(email, name, password))
                    elif user_type == "Doctor" and len(user_info) == 4:
                        users.append(Doctor(email, name, password))
        except FileNotFoundError:
            pass
        return users

    def save_users_to_file(self, users):
        with open(self.file_name, "w") as file:
            for user in users:
                file.write(f"{type(user).__name__}-" + "-".join(user.get_user_info()) + "\n")


class PatientOptions:
    def __init__(self, root, auth_system, patient):
        self.root = Toplevel(root)
        self.auth_system = auth_system
        self.patient = patient

        self.root.title("Patient Options")
        self.root.geometry("400x300")

        Label(self.root, text="Patient Options", font=("Helvetica", 16)).pack(pady=10)

        Button(self.root, text="Upload MRI Scan", command=self.upload_scan).pack(pady=5)
        Button(self.root, text="View My MRI Scan", command=self.view_scan).pack(pady=5)
        Button(self.root, text="Logout", command=self.logout).pack(pady=10)

    def upload_scan(self):
        file_path = filedialog.askopenfilename(
            title="Select MRI scan",
            filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")]
        )
        if file_path:
            self.patient.upload_scan(file_path)
            self.auth_system.save_users()
            messagebox.showinfo("Upload Successful", "Your MRI scan has been uploaded.")

    def view_scan(self):
        scan_path = self.patient.get_scan()
        if scan_path and os.path.exists(scan_path):
            try:
                img = Image.open(scan_path)
                img.show()  # Open the image using the default viewer
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open the image: {e}")
        else:
            messagebox.showerror("Error", "You have not uploaded an MRI scan.")

    def logout(self):
        self.root.destroy()
        self.root.master.deiconify()


class User:
    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password = password

    def display_info(self):
        return f"Email: {self.email}, Name: {self.name}"

    def get_user_info(self):
        return [self.email, self.name, self.password]


class Patient(User):
    def __init__(self, email, name, password, age, medical_history, scan_path=None):
        super().__init__(email, name, password)
        self.age = age
        self.medical_history = medical_history
        self.scan_path = scan_path

    def get_user_info(self):
        return [self.email, self.name, self.password, str(self.age), self.medical_history]

    def upload_scan(self, file_path):
        self.scan_path = file_path

    def get_scan(self):
        return self.scan_path


class Doctor(User):
    def __init__(self, email, name, password):
        super().__init__(email, name, password)

    def get_user_info(self):
        return [self.email, self.name, self.password]


class Admin(User):
    def __init__(self, email, name, password):
        super().__init__(email, name, password)

    def get_user_info(self):
        return [self.email, self.name, self.password]


class AuthenticationSystem:
    def __init__(self, file_handler):
        self.file_handler = file_handler
        self.users = self.load_users()

    def load_users(self):
        return self.file_handler.read_users_from_file()

    def save_users(self):
        self.file_handler.save_users_to_file(self.users)

    def register_user(self, user):
        self.users.append(user)
        self.save_users()

    def login(self, email, password):
        for user in self.users:
            if user.email == email and user.password == password:
                return user
        return None

    def create_patient_account(self, email, name, password):
        age = simpledialog.askstring("Input", "Enter age:")
        medical_history = simpledialog.askstring("Input", "Enter medical history:")
        user = Patient(email, name, password, age, medical_history)
        self.register_user(user)


class LoginApp:
    def __init__(self, root, auth_system):
        self.root = root
        self.auth_system = auth_system

        self.root.title("Login")
        self.root.geometry("400x300")

        Label(self.root, text="Email:").pack(pady=10)
        self.email_entry = Entry(self.root)
        self.email_entry.pack(pady=5)

        Label(self.root, text="Password:").pack(pady=10)
        self.password_entry = Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        Button(self.root, text="Login", command=self.login_user).pack(pady=20)

    def login_user(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        user = self.auth_system.login(email, password)

        if user:
            if isinstance(user, Admin):
                self.root.withdraw()
                AdminOptions(self.root, self.auth_system)
            elif isinstance(user, Doctor):
                messagebox.showinfo("Login", f"Welcome, Doctor {user.name}!")
            elif isinstance(user, Patient):
                self.root.withdraw()
                PatientOptions(self.root, self.auth_system, user)
        else:
            messagebox.showerror("Login Failed", "Invalid email or password.")


if __name__ == "__main__":
    file_handler = FileHandler()
    auth_system = AuthenticationSystem(file_handler)

    root = tk.Tk()
    app = LoginApp(root, auth_system)
    root.mainloop()
