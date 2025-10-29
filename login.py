"""
Login System for Face Recognition Attendance System
"""
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

from main import Student

class LoginWindow:
    def __init__(self, root, on_success=None):
        self.root = root
        self.root.title("Login - Face Recognition Attendance System")
        self.root.geometry("1366x768+0+0")
        self.root.config(bg="white")
        # Optional callback to run after successful login
        self.on_success = on_success
        
        try:
            self.root.state('zoomed')
        except:
            pass
        
        # Background Image
        try:
            if os.path.exists("images/login.jpg"):
                # Load the background image
                img_bg = Image.open("images/login.jpg")
                img_bg = img_bg.resize((1366, 768), Image.Resampling.LANCZOS)
                self.photoimg_bg = ImageTk.PhotoImage(img_bg)
                
                # Create background label
                bg_lbl = Label(self.root, image=self.photoimg_bg)
                bg_lbl.place(x=0, y=0, width=1366, height=768)
            else:
                # Fallback to white background
                bg_lbl = Label(self.root, bg="white")
                bg_lbl.place(x=0, y=0, width=1366, height=768)
        except Exception as e:
            print(f"Background image error: {e}")
            # Fallback to white background
            bg_lbl = Label(self.root, bg="white")
            bg_lbl.place(x=0, y=0, width=1366, height=768)
        
        # Title - placed directly on background image
        title = Label(self.root, text="FACE RECOGNITION ATTENDANCE SYSTEM", 
                     font=("Arial", 35, "bold"), fg="red")
        title.place(x=0, y=30, width=1366, height=50)
        
        subtitle = Label(self.root, text="Login Security System", 
                        font=("Arial", 25, "bold"), fg="darkgreen")
        subtitle.place(x=0, y=90, width=1366, height=40)
        
        # Login Frame (white box for login form)
        login_frame = Frame(self.root, bg="white", bd=2, relief=RIDGE)
        login_frame.place(x=433, y=180, width=500, height=400)
        
        # Login Icon/Image - Logo
        try:
            # Try to load the logo image from images folder
            if os.path.exists("images/logo image.png"):
                img_login = Image.open("images/logo image.png")
                img_login = img_login.resize((120, 120), Image.Resampling.LANCZOS)
            else:
                # Fallback to a placeholder if logo not found
                img_login = Image.new('RGB', (120, 120), color='#0066cc')
            
            self.photoimage_login = ImageTk.PhotoImage(img_login)
            lblimg_login = Label(login_frame, image=self.photoimage_login, bg="white", bd=0)
            lblimg_login.place(x=190, y=20, width=120, height=120)
        except Exception as e:
            print(f"Error loading logo: {e}")
            pass
        
        # Get Started Label
        get_str = Label(login_frame, text="Get Started", font=("Arial", 20, "bold"), 
                       fg="darkblue", bg="white")
        get_str.place(x=170, y=130)
        
        # Username
        username_lbl = Label(login_frame, text="Username:", font=("Arial", 15, "bold"), 
                            fg="black", bg="white")
        username_lbl.place(x=70, y=180)
        
        self.txtuser = ttk.Entry(login_frame, font=("Arial", 15))
        self.txtuser.place(x=70, y=215, width=350, height=35)
        
        # Password
        password_lbl = Label(login_frame, text="Password:", font=("Arial", 15, "bold"), 
                            fg="black", bg="white")
        password_lbl.place(x=70, y=260)
        
        self.txtpass = ttk.Entry(login_frame, show="*", font=("Arial", 15))
        self.txtpass.place(x=70, y=295, width=350, height=35)
        
        # Buttons Frame
        btn_frame = Frame(login_frame, bg="white", bd=0)
        btn_frame.place(x=70, y=345, width=350, height=40)
        
        # Login Button
        loginbtn = Button(btn_frame, text="Login", command=self.login, 
                         font=("Arial", 14, "bold"), bd=0, relief=FLAT,
                         fg="white", bg="darkblue", activebackground="blue",
                         cursor="hand2")
        loginbtn.place(x=0, y=0, width=170, height=40)
        
        # Reset Button
        resetbtn = Button(btn_frame, text="Reset", command=self.reset_fields,
                         font=("Arial", 14, "bold"), bd=0, relief=FLAT,
                         fg="white", bg="red", activebackground="darkred",
                         cursor="hand2")
        resetbtn.place(x=180, y=0, width=170, height=40)
        
        # Footer - placed directly on root (over background)
        footer = Label(self.root, text="Developed by Your Name | © 2025 All Rights Reserved", 
                      font=("Arial", 12), fg="gray")
        footer.place(x=0, y=720, width=1366, height=30)
    
    def reset_fields(self):
        """Reset username and password fields"""
        self.txtuser.delete(0, END)
        self.txtpass.delete(0, END)
    
    def login(self):
        """Fixed login method with better validation and debugging"""
        # Get credentials and remove whitespace
        username = self.txtuser.get().strip()
        password = self.txtpass.get().strip()

        # Debug print (shows in console)
        print(f"Login attempt: username='{username}', password='{password}'")

        # Valid Credentials Table
        valid_users = {
            # Format: "username": {"password": "xxx", "role": "xxx", "name": "xxx", "access_level": "xxx"}
            "admin": {
                "password": "admin123",
                "role": "Administrator",
                "name": "Admin",
                "access_level": "Full Access"
            },
            "user": {
                "password": "user123",
                "role": "User",
                "name": "User",
                "access_level": "User Access"
            },
            "test": {
                "password": "test123",
                "role": "Test",
                "name": "Test",
                "access_level": "Test Access"
            }
        }
                    
        if username == "" or password == "":
            messagebox.showerror("Error", "All fields are required!", parent=self.root)
        elif username in valid_users and valid_users[username]["password"] == password:
            user_info = valid_users[username]
            welcome_msg = f"Welcome {user_info['name']}!\n\nRole: {user_info['role']}\nAccess: {user_info['access_level']}"
            messagebox.showinfo("Login Successful", welcome_msg, parent=self.root)
            self.root.destroy()
            
            # If a post-login callback is provided, use it; otherwise open main.py default
            try:
                if callable(self.on_success):
                    self.on_success()
                else:
                    import main
                    root = Tk()
                    obj = main.Face_Recognition_System(root)
                    root.mainloop()
            except Exception as e:
                # Root is destroyed; print for safety if messagebox can't attach to a parent
                try:
                    messagebox.showerror("Error", f"Failed to open main application: {str(e)}")
                except:
                    print(f"Failed to open main application: {e}")
        else:
            # Debug info
            print(f"Available users: {list(valid_users.keys())}")
            messagebox.showerror("Invalid",
                "Invalid Username or Password!\n\n"
                "Available users: admin, user, test\n"
                "Check for extra spaces or case sensitivity.",
                parent=self.root)


if __name__ == "__main__":
    root = Tk()
    app = LoginWindow(root)
    root.mainloop()
