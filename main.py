from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
from tkinter import messagebox
import pickle
import cv2
import os
import numpy as np
from datetime import datetime
import csv
import time
import sys
import threading

# Fix OpenCV threading issue with Tkinter
os.environ["OPENCV_VIDEOIO_PRIORITY_MSMF"] = "0"
cv2.setNumThreads(1)

# Import attendance report system and optimized camera
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from attendance_report import AttendanceReport
except:
    AttendanceReport = None

try:
    from optimized_camera import fix_camera_quality, OptimizedCameraCapture
    OPTIMIZED_CAMERA_AVAILABLE = True
except:
    OPTIMIZED_CAMERA_AVAILABLE = False
    print("Warning: Optimized camera module not available, using standard camera")

# ==================== Robust Camera Capture Helper ====================
def open_camera_with_backend():
    """
    Open camera with multiple backend attempts - optimized for Windows
    Captures COLOR images properly without hanging issues
    Fixed threading issues with Tkinter
    Returns: (cap, backend_name) or (None, None) if failed
    """
    print("🔍 Searching for available cameras...")
    
    # Try different backends and camera indices
    # Using DirectShow first for best Windows compatibility
    backends = [
        (cv2.CAP_DSHOW, "DirectShow (Windows)"),
        (cv2.CAP_ANY, "Default Backend")
    ]
    
    camera_indices = [0, 1]
    
    for backend, backend_name in backends:
        for camera_idx in camera_indices:
            try:
                print(f"  Trying Camera {camera_idx} with {backend_name}...")
                
                # Open camera with backend
                if isinstance(backend, int) and backend == 0:
                    cap = cv2.VideoCapture(camera_idx)
                else:
                    cap = cv2.VideoCapture(camera_idx, backend)
                
                # Give camera time to initialize
                time.sleep(0.5)
                
                if cap.isOpened():
                    # Set reasonable properties for color capture
                    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                    cap.set(cv2.CAP_PROP_FPS, 30)
                    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Minimize buffer to reduce lag
                    
                    # Discard first few frames to let camera warm up
                    for _ in range(5):
                        cap.read()
                    
                    # Test if we can read a valid COLOR frame
                    ret, frame = cap.read()
                    
                    if ret and frame is not None and frame.size > 0:
                        # Verify it's a color image (3 channels)
                        if len(frame.shape) == 3 and frame.shape[2] == 3:
                            print(f"✓ Camera {camera_idx} opened successfully with {backend_name}")
                            print(f"  Resolution: {frame.shape[1]}x{frame.shape[0]}")
                            print(f"  Color Mode: BGR (3 channels) ✓")
                            return cap, backend_name
                    
                    cap.release()
                    
            except Exception as e:
                print(f"  ✗ Failed: {str(e)}")
                try:
                    if 'cap' in locals() and cap is not None:
                        cap.release()
                except:
                    pass
                continue
    
    print("✗ No working camera found!")
    return None, None

def safe_frame_read(cap):
    """
    Safely read a frame from camera with validation
    Returns: (success, frame) - frame is None if read failed
    """
    try:
        ret, frame = cap.read()
        
        if ret and frame is not None and frame.size > 0:
            return True, frame
        else:
            return False, None
    except Exception as e:
        print(f"Frame read error: {str(e)}")
        return False, None

class Face_Recognition_System:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1366x768+0+0")
        self.root.title("Face Recognition System")
        try:
            self.root.state('zoomed')  # Maximize window
        except:
            pass
        
        # Title
        title_lbl = Label(self.root, text="FACE RECOGNITION ATTENDANCE SYSTEM", 
                         font=("Arial", 40, "bold"), bg="white", fg="red")
        title_lbl.place(x=0, y=0, width=1366, height=70)
        
        # Top Image Section - 3 images side by side with proper initialization
        try:
            img_top = Image.new('RGB', (455, 140), color='lightblue')
            self.photoimg_top = ImageTk.PhotoImage(img_top)
            f_lbl = Label(self.root, image=self.photoimg_top, bg='lightblue')
            f_lbl.place(x=0, y=70, width=455, height=140)
        except:
            f_lbl = Label(self.root, bg='lightblue')
            f_lbl.place(x=0, y=70, width=455, height=140)
        
        # Second Image
        try:
            img_top1 = Image.new('RGB', (455, 140), color='lightgreen')
            self.photoimg_top1 = ImageTk.PhotoImage(img_top1)
            f_lbl1 = Label(self.root, image=self.photoimg_top1, bg='lightgreen')
            f_lbl1.place(x=455, y=70, width=456, height=140)
        except:
            f_lbl1 = Label(self.root, bg='lightgreen')
            f_lbl1.place(x=455, y=70, width=456, height=140)
        
        # Third Image
        try:
            img_top2 = Image.new('RGB', (455, 140), color='lightyellow')
            self.photoimg_top2 = ImageTk.PhotoImage(img_top2)
            f_lbl2 = Label(self.root, image=self.photoimg_top2, bg='lightyellow')
            f_lbl2.place(x=911, y=70, width=455, height=140)
        except:
            f_lbl2 = Label(self.root, bg='lightyellow')
            f_lbl2.place(x=911, y=70, width=455, height=140)
        
        # Background
        bg_lbl = Label(self.root, bg='white')
        bg_lbl.place(x=0, y=210, width=1366, height=558)
        
        # Title inside background
        title_lbl1 = Label(bg_lbl, text="FACE RECOGNITION SYSTEM", 
                          font=("Arial", 32, "bold"), bg="white", fg="darkgreen")
        title_lbl1.place(x=0, y=0, width=1366, height=50)
        
        # Button dimensions and spacing - Smaller buttons for compact layout
        btn_width = 200
        btn_height = 130
        btn_label_height = 40
        
        # Calculate spacing for 4 columns (more even distribution)
        total_width = 1366
        spacing = (total_width - (4 * btn_width)) // 5
        
        # Row 1 - Y position (starts right after title)
        row1_y = 65
        row1_label_y = row1_y + btn_height
        
        # Row 2 - Y position (optimized spacing to fit all buttons perfectly)
        row2_y = row1_label_y + btn_label_height + 12
        row2_label_y = row2_y + btn_height
        
        # Column X positions
        col1_x = spacing
        col2_x = col1_x + btn_width + spacing
        col3_x = col2_x + btn_width + spacing
        col4_x = col3_x + btn_width + spacing
        
        # Helper function to create uniform button images
        def create_button_image(color, width, height):
            """Create a uniform colored button image with exact dimensions"""
            img = Image.new('RGB', (width, height), color=color)
            return ImageTk.PhotoImage(img)
        
        # ROW 1 BUTTONS - All using exact same dimensions
        
        # Student Details Button (Blue)
        self.photoimg1 = create_button_image('#0000FF', btn_width, btn_height)
        
        b1 = Button(bg_lbl, image=self.photoimg1, command=self.student_details, cursor="hand2", bd=0, relief=FLAT)
        b1.place(x=col1_x, y=row1_y, width=btn_width, height=btn_height)
        
        b1_1 = Button(bg_lbl, text="Student Details", command=self.student_details, cursor="hand2",
                     font=("Arial", 16, "bold"), bg="darkblue", fg="white", bd=0, relief=FLAT, activebackground="blue")
        b1_1.place(x=col1_x, y=row1_label_y, width=btn_width, height=btn_label_height)
        
        # Face Detector Button (Red)
        self.photoimg2 = create_button_image('#FF0000', btn_width, btn_height)
        
        b2 = Button(bg_lbl, image=self.photoimg2, command=self.face_recognition, cursor="hand2", bd=0, relief=FLAT)
        b2.place(x=col2_x, y=row1_y, width=btn_width, height=btn_height)
        
        b2_1 = Button(bg_lbl, text="Face Detector", command=self.face_recognition, cursor="hand2",
                     font=("Arial", 16, "bold"), bg="darkblue", fg="white", bd=0, relief=FLAT, activebackground="blue")
        b2_1.place(x=col2_x, y=row1_label_y, width=btn_width, height=btn_label_height)
        
        # Attendance Button (Green)
        self.photoimg3 = create_button_image('#008000', btn_width, btn_height)
        
        b3 = Button(bg_lbl, image=self.photoimg3, command=self.attendance, cursor="hand2", bd=0, relief=FLAT)
        b3.place(x=col3_x, y=row1_y, width=btn_width, height=btn_height)
        
        b3_1 = Button(bg_lbl, text="Attendance", command=self.attendance, cursor="hand2",
                     font=("Arial", 16, "bold"), bg="darkblue", fg="white", bd=0, relief=FLAT, activebackground="blue")
        b3_1.place(x=col3_x, y=row1_label_y, width=btn_width, height=btn_label_height)
        
        # Train Data Button (Purple)
        self.photoimg4 = create_button_image('#800080', btn_width, btn_height)
        
        b4 = Button(bg_lbl, image=self.photoimg4, command=self.train_data, cursor="hand2", bd=0, relief=FLAT)
        b4.place(x=col4_x, y=row1_y, width=btn_width, height=btn_height)
        
        b4_1 = Button(bg_lbl, text="Train Data", command=self.train_data, cursor="hand2",
                     font=("Arial", 16, "bold"), bg="darkblue", fg="white", bd=0, relief=FLAT, activebackground="blue")
        b4_1.place(x=col4_x, y=row1_label_y, width=btn_width, height=btn_label_height)
        
        # ROW 2 BUTTONS - All using exact same dimensions
        
        # Photos Button (Orange)
        self.photoimg5 = create_button_image('#FFA500', btn_width, btn_height)
        
        b5 = Button(bg_lbl, image=self.photoimg5, command=self.open_img, cursor="hand2", bd=0, relief=FLAT)
        b5.place(x=col1_x, y=row2_y, width=btn_width, height=btn_height)
        
        b5_1 = Button(bg_lbl, text="Photos", command=self.open_img, cursor="hand2",
                     font=("Arial", 16, "bold"), bg="darkblue", fg="white", bd=0, relief=FLAT, activebackground="blue")
        b5_1.place(x=col1_x, y=row2_label_y, width=btn_width, height=btn_label_height)
        
        # Developer Button (Cyan)
        self.photoimg6 = create_button_image('#00FFFF', btn_width, btn_height)
        
        b6 = Button(bg_lbl, image=self.photoimg6, command=self.developer, cursor="hand2", bd=0, relief=FLAT)
        b6.place(x=col2_x, y=row2_y, width=btn_width, height=btn_height)
        
        b6_1 = Button(bg_lbl, text="Developer", command=self.developer, cursor="hand2",
                     font=("Arial", 16, "bold"), bg="darkblue", fg="white", bd=0, relief=FLAT, activebackground="blue")
        b6_1.place(x=col2_x, y=row2_label_y, width=btn_width, height=btn_label_height)
        
        # Help Button (Yellow)
        self.photoimg7 = create_button_image('#FFFF00', btn_width, btn_height)
        
        b7 = Button(bg_lbl, image=self.photoimg7, command=self.help, cursor="hand2", bd=0, relief=FLAT)
        b7.place(x=col3_x, y=row2_y, width=btn_width, height=btn_height)
        
        b7_1 = Button(bg_lbl, text="Help", command=self.help, cursor="hand2",
                     font=("Arial", 16, "bold"), bg="darkblue", fg="white", bd=0, relief=FLAT, activebackground="blue")
        b7_1.place(x=col3_x, y=row2_label_y, width=btn_width, height=btn_label_height)
        
        # Exit Button (Pink)
        self.photoimg8 = create_button_image('#FFC0CB', btn_width, btn_height)
        
        b8 = Button(bg_lbl, image=self.photoimg8, command=self.exit_app, cursor="hand2", bd=0, relief=FLAT)
        b8.place(x=col4_x, y=row2_y, width=btn_width, height=btn_height)
        
        b8_1 = Button(bg_lbl, text="Exit", command=self.exit_app, cursor="hand2",
                     font=("Arial", 16, "bold"), bg="darkblue", fg="white", bd=0, relief=FLAT, activebackground="blue")
        b8_1.place(x=col4_x, y=row2_label_y, width=btn_width, height=btn_label_height)
    
    def open_img(self):
        os.startfile("data")
    
    def exit_app(self):
        self.exit_app = messagebox.askyesno("Face Recognition", "Are you sure you want to exit?", parent=self.root)
        if self.exit_app > 0:
            self.root.destroy()
        else:
            return
    
    # ==================== Function Buttons ====================
    def student_details(self):
        self.new_window = Toplevel(self.root)
        self.app = Student(self.new_window)
    
    def train_data(self):
        self.new_window = Toplevel(self.root)
        self.app = Train(self.new_window)
    
    def face_recognition(self):
        self.new_window = Toplevel(self.root)
        self.app = FaceRecognition(self.new_window)
    
    def attendance(self):
        self.new_window = Toplevel(self.root)
        if AttendanceReport:
            self.app = AttendanceReport(self.new_window)
        else:
            self.app = Attendance(self.new_window)
    
    def developer(self):
        self.new_window = Toplevel(self.root)
        self.app = Developer(self.new_window)
    
    def help(self):
        self.new_window = Toplevel(self.root)
        self.app = Help(self.new_window)


# ==================== Student Details Window ====================
class Student:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Student Management System")
        
        # Variables
        self.var_dep = StringVar()
        self.var_course = StringVar()
        self.var_year = StringVar()
        self.var_semester = StringVar()
        self.var_std_id = StringVar()
        self.var_std_name = StringVar()
        self.var_div = StringVar()
        self.var_roll = StringVar()
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_email = StringVar()
        self.var_phone = StringVar()
        self.var_address = StringVar()
        self.var_teacher = StringVar()
        
        # Title
        title_lbl = Label(self.root, text="STUDENT MANAGEMENT SYSTEM", 
                         font=("times new roman", 35, "bold"), bg="white", fg="darkgreen")
        title_lbl.place(x=0, y=0, width=1530, height=45)
        
        # Main frame - moved up to y=55 (no banner)
        main_frame = Frame(self.root, bd=2, bg="white")
        main_frame.place(x=10, y=55, width=1510, height=730)
        
        # Left Frame
        Left_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE, 
                               text="Student Details", font=("times new roman", 12, "bold"))
        Left_frame.place(x=10, y=10, width=730, height=710)
        
        # Current Course
        current_course_frame = LabelFrame(Left_frame, bd=2, bg="white", relief=RIDGE, 
                                         text="Current Course Information", font=("times new roman", 12, "bold"))
        current_course_frame.place(x=5, y=5, width=715, height=150)
        
        # Department
        dep_label = Label(current_course_frame, text="Department", font=("times new roman", 12, "bold"), bg="white")
        dep_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        
        dep_combo = ttk.Combobox(current_course_frame, textvariable=self.var_dep, font=("times new roman", 12, "bold"), 
                                state="readonly", width=17)
        dep_combo["values"] = ("Select Department", "Computer Science", "IT", "Civil", "Mechanical")
        dep_combo.current(0)
        dep_combo.grid(row=0, column=1, padx=2, pady=10, sticky=W)
        
        # Course
        course_label = Label(current_course_frame, text="Course", font=("times new roman", 12, "bold"), bg="white")
        course_label.grid(row=0, column=2, padx=10, pady=10, sticky=W)
        
        course_combo = ttk.Combobox(current_course_frame, textvariable=self.var_course, font=("times new roman", 12, "bold"), 
                                   state="readonly", width=17)
        course_combo["values"] = ("Select Course", "Data Structure", "Aritificial Intelligence", "Machine Learning", "Computer Network")
        course_combo.current(0)
        course_combo.grid(row=0, column=3, padx=2, pady=10, sticky=W)
        
        # Year
        year_label = Label(current_course_frame, text="Year", font=("times new roman", 12, "bold"), bg="white")
        year_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)
        
        year_combo = ttk.Combobox(current_course_frame, textvariable=self.var_year, font=("times new roman", 12, "bold"), 
                                 state="readonly", width=17)
        year_combo["values"] = ("Select Year", "2020-21", "2021-22", "2022-23", "2023-24", "2024-25", "2025-26", "2026-27", "2027-28")
        year_combo.current(0)
        year_combo.grid(row=1, column=1, padx=2, pady=10, sticky=W)
        
        # Semester
        semester_label = Label(current_course_frame, text="Semester", font=("times new roman", 12, "bold"), bg="white")
        semester_label.grid(row=1, column=8, padx=10, pady=10, sticky=W)
        
        semester_combo = ttk.Combobox(current_course_frame, textvariable=self.var_semester, font=("times new roman", 12, "bold"), 
                                     state="readonly", width=17)
        semester_combo["values"] = ("Select Semester", "Semester-1", "Semester-2", "Semester-3", "Semester-4", 
                                   "Semester-5", "Semester-6", "Semester-7", "Semester-8")
        semester_combo.current(0)
        semester_combo.grid(row=1, column=3, padx=2, pady=10, sticky=W)
        
        # Class Student Information
        class_student_frame = LabelFrame(Left_frame, bd=2, bg="white", relief=RIDGE, 
                                        text="Class Student Information", font=("times new roman", 12, "bold"))
        class_student_frame.place(x=5, y=160, width=715, height=540)
        
        # Student ID
        studentId_label = Label(class_student_frame, text="Student ID:", font=("times new roman", 12, "bold"), bg="white")
        studentId_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)
        
        studentId_entry = ttk.Entry(class_student_frame, textvariable=self.var_std_id, width=20, font=("times new roman", 12, "bold"))
        studentId_entry.grid(row=0, column=1, padx=10, pady=5, sticky=W)
        
        # Student Name
        studentName_label = Label(class_student_frame, text="Student Name:", font=("times new roman", 12, "bold"), bg="white")
        studentName_label.grid(row=0, column=2, padx=10, pady=5, sticky=W)
        
        studentName_entry = ttk.Entry(class_student_frame, textvariable=self.var_std_name, width=20, font=("times new roman", 12, "bold"))
        studentName_entry.grid(row=0, column=3, padx=10, pady=5, sticky=W)
        
        # Class Division
        class_div_label = Label(class_student_frame, text="Class Division:", font=("times new roman", 12, "bold"), bg="white")
        class_div_label.grid(row=1, column=0, padx=10, pady=5, sticky=W)
        
        class_div_combo = ttk.Combobox(class_student_frame, textvariable=self.var_div, font=("times new roman", 12, "bold"), 
                                      state="readonly", width=18)
        class_div_combo["values"] = ("A", "B", "C")
        class_div_combo.current(0)
        class_div_combo.grid(row=1, column=1, padx=10, pady=5, sticky=W)
        
        # Roll No
        roll_no_label = Label(class_student_frame, text="Roll No:", font=("times new roman", 12, "bold"), bg="white")
        roll_no_label.grid(row=1, column=2, padx=10, pady=5, sticky=W)
        
        roll_no_entry = ttk.Entry(class_student_frame, textvariable=self.var_roll, width=20, font=("times new roman", 12, "bold"))
        roll_no_entry.grid(row=1, column=3, padx=10, pady=5, sticky=W)
        
        # Gender
        gender_label = Label(class_student_frame, text="Gender:", font=("times new roman", 12, "bold"), bg="white")
        gender_label.grid(row=2, column=0, padx=10, pady=5, sticky=W)
        
        gender_combo = ttk.Combobox(class_student_frame, textvariable=self.var_gender, font=("times new roman", 12, "bold"), 
                                   state="readonly", width=18)
        gender_combo["values"] = ("Male", "Female", "Other")
        gender_combo.current(0)
        gender_combo.grid(row=2, column=1, padx=10, pady=5, sticky=W)
        
        # DOB
        dob_label = Label(class_student_frame, text="DOB:", font=("times new roman", 12, "bold"), bg="white")
        dob_label.grid(row=2, column=2, padx=10, pady=5, sticky=W)
        
        dob_entry = ttk.Entry(class_student_frame, textvariable=self.var_dob, width=20, font=("times new roman", 12, "bold"))
        dob_entry.grid(row=2, column=3, padx=10, pady=5, sticky=W)
        
        # Email
        email_label = Label(class_student_frame, text="Email:", font=("times new roman", 12, "bold"), bg="white")
        email_label.grid(row=3, column=0, padx=10, pady=5, sticky=W)
        
        email_entry = ttk.Entry(class_student_frame, textvariable=self.var_email, width=20, font=("times new roman", 12, "bold"))
        email_entry.grid(row=3, column=1, padx=10, pady=5, sticky=W)
        
        # Phone
        phone_label = Label(class_student_frame, text="Phone No:", font=("times new roman", 12, "bold"), bg="white")
        phone_label.grid(row=3, column=2, padx=10, pady=5, sticky=W)
        
        phone_entry = ttk.Entry(class_student_frame, textvariable=self.var_phone, width=20, font=("times new roman", 12, "bold"))
        phone_entry.grid(row=3, column=3, padx=10, pady=5, sticky=W)
        
        # Address
        address_label = Label(class_student_frame, text="Address:", font=("times new roman", 12, "bold"), bg="white")
        address_label.grid(row=4, column=0, padx=10, pady=5, sticky=W)
        
        address_entry = ttk.Entry(class_student_frame, textvariable=self.var_address, width=20, font=("times new roman", 12, "bold"))
        address_entry.grid(row=4, column=1, padx=10, pady=5, sticky=W)
        
        # Teacher Name
        teacher_label = Label(class_student_frame, text="Teacher Name:", font=("times new roman", 12, "bold"), bg="white")
        teacher_label.grid(row=4, column=2, padx=10, pady=5, sticky=W)
        
        teacher_entry = ttk.Entry(class_student_frame, textvariable=self.var_teacher, width=20, font=("times new roman", 12, "bold"))
        teacher_entry.grid(row=4, column=3, padx=10, pady=5, sticky=W)
        
        # Radio Buttons
        self.var_radio1 = StringVar()
        radiobtn1 = ttk.Radiobutton(class_student_frame, variable=self.var_radio1, text="Take Photo Sample", value="Yes")
        radiobtn1.grid(row=5, column=0, pady=5, padx=10, sticky=W)
        
        radiobtn2 = ttk.Radiobutton(class_student_frame, variable=self.var_radio1, text="No Photo Sample", value="No")
        radiobtn2.grid(row=5, column=1, pady=5, padx=10, sticky=W)
        
        # Take Photo Button Frame (using grid for better layout)
        btn_frame1 = Frame(class_student_frame, bd=2, relief=RIDGE, bg="white")
        btn_frame1.grid(row=6, column=0, columnspan=4, padx=10, pady=10, sticky=W+E)
        
        take_photo_btn = Button(btn_frame1, command=self.generate_dataset, text="Take Photo Sample", 
                               font=("times new roman", 12, "bold"), bg="green", fg="white", cursor="hand2", width=20)
        take_photo_btn.grid(row=0, column=0, padx=5, pady=5)
        
        update_photo_btn = Button(btn_frame1, text="Update Photo Sample", 
                                 font=("times new roman", 12, "bold"), bg="orange", fg="white", cursor="hand2", width=20)
        update_photo_btn.grid(row=0, column=1, padx=5, pady=5)
        
        # Main Buttons Frame (Save, Update, Delete, Reset) using grid
        btn_frame = Frame(class_student_frame, bd=2, relief=RIDGE, bg="white")
        btn_frame.grid(row=7, column=0, columnspan=4, padx=10, pady=5, sticky=W+E)
        
        save_btn = Button(btn_frame, text="Save", command=self.add_data, 
                         font=("times new roman", 12, "bold"), bg="blue", fg="white", cursor="hand2", width=15)
        save_btn.grid(row=0, column=0, padx=5, pady=5)
        
        update_btn = Button(btn_frame, text="Update", command=self.update_data, 
                           font=("times new roman", 12, "bold"), bg="blue", fg="white", cursor="hand2", width=15)
        update_btn.grid(row=0, column=1, padx=5, pady=5)
        
        delete_btn = Button(btn_frame, text="Delete", command=self.delete_data, 
                           font=("times new roman", 12, "bold"), bg="red", fg="white", cursor="hand2", width=15)
        delete_btn.grid(row=0, column=2, padx=5, pady=5)
        
        reset_btn = Button(btn_frame, text="Reset", command=self.reset_data, 
                          font=("times new roman", 12, "bold"), bg="darkgray", fg="white", cursor="hand2", width=15)
        reset_btn.grid(row=0, column=3, padx=5, pady=5)
        
        # Right Frame
        Right_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE, 
                                text="Student Details", font=("times new roman", 12, "bold"))
        Right_frame.place(x=750, y=10, width=750, height=710)
        
        # Search System
        search_frame = LabelFrame(Right_frame, bd=2, bg="white", relief=RIDGE, 
                                 text="Search System", font=("times new roman", 12, "bold"))
        search_frame.place(x=5, y=5, width=735, height=80)
        
        search_label = Label(search_frame, text="Search By:", font=("times new roman", 12, "bold"), bg="red", fg="white")
        search_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)
        
        search_combo = ttk.Combobox(search_frame, font=("times new roman", 12, "bold"), state="readonly", width=15)
        search_combo["values"] = ("Select", "Roll No", "Phone No")
        search_combo.current(0)
        search_combo.grid(row=0, column=1, padx=2, pady=10, sticky=W)
        
        search_entry = ttk.Entry(search_frame, width=15, font=("times new roman", 12, "bold"))
        search_entry.grid(row=0, column=2, padx=10, pady=5, sticky=W)
        
        search_btn = Button(search_frame, text="Search", width=12, font=("times new roman", 12, "bold"), bg="blue", fg="white")
        search_btn.grid(row=0, column=3, padx=4)
        
        showAll_btn = Button(search_frame, text="Show All", width=12, font=("times new roman", 12, "bold"), bg="blue", fg="white")
        showAll_btn.grid(row=0, column=4, padx=4)
        
        # Table Frame
        table_frame = Frame(Right_frame, bd=2, bg="white", relief=RIDGE)
        table_frame.place(x=5, y=90, width=735, height=610)
        
        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)
        
        self.student_table = ttk.Treeview(table_frame, columns=("dep", "course", "year", "sem", "id", "name", 
                                                                "div", "roll", "gender", "dob", "email", "phone", 
                                                                "address", "teacher", "photo"), 
                                         xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)
        
        self.student_table.heading("dep", text="Department")
        self.student_table.heading("course", text="Course")
        self.student_table.heading("year", text="Year")
        self.student_table.heading("sem", text="Semester")
        self.student_table.heading("id", text="Student ID")
        self.student_table.heading("name", text="Name")
        self.student_table.heading("div", text="Section")
        self.student_table.heading("roll", text="Roll No")
        self.student_table.heading("gender", text="Gender")
        self.student_table.heading("dob", text="DOB")
        self.student_table.heading("email", text="Email")
        self.student_table.heading("phone", text="Phone")
        self.student_table.heading("address", text="Address")
        self.student_table.heading("teacher", text="Teacher")
        self.student_table.heading("photo", text="PhotoSampleStatus")
        
        self.student_table["show"] = "headings"
        
        self.student_table.column("dep", width=100)
        self.student_table.column("course", width=100)
        self.student_table.column("year", width=100)
        self.student_table.column("sem", width=100)
        self.student_table.column("id", width=100)
        self.student_table.column("name", width=100)
        self.student_table.column("div", width=100)
        self.student_table.column("roll", width=100)
        self.student_table.column("gender", width=100)
        self.student_table.column("dob", width=100)
        self.student_table.column("email", width=100)
        self.student_table.column("phone", width=100)
        self.student_table.column("address", width=100)
        self.student_table.column("teacher", width=100)
        self.student_table.column("photo", width=150)
        
        self.student_table.pack(fill=BOTH, expand=1)
        self.student_table.bind("<ButtonRelease>", self.get_cursor)
        self.fetch_data()
    
    # ==================== Function Declaration ====================
    def add_data(self):
        if self.var_dep.get() == "Select Department" or self.var_std_name.get() == "" or self.var_std_id.get() == "":
            messagebox.showerror("Error", "All Fields are required", parent=self.root)
        else:
            try:
                # Create data directory if it doesn't exist
                if not os.path.exists("data"):
                    os.makedirs("data")
                
                # Save to CSV file
                with open("data/student.csv", "a", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow([
                        self.var_dep.get(),
                        self.var_course.get(),
                        self.var_year.get(),
                        self.var_semester.get(),
                        self.var_std_id.get(),
                        self.var_std_name.get(),
                        self.var_div.get(),
                        self.var_roll.get(),
                        self.var_gender.get(),
                        self.var_dob.get(),
                        self.var_email.get(),
                        self.var_phone.get(),
                        self.var_address.get(),
                        self.var_teacher.get(),
                        self.var_radio1.get()
                    ])
                    
                messagebox.showinfo("Success", "Student details has been added successfully", parent=self.root)
                self.fetch_data()
            except Exception as es:
                messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)
    
    def fetch_data(self):
        if not os.path.exists("data/student.csv"):
            return
        
        with open("data/student.csv", "r") as file:
            reader = csv.reader(file)
            data = list(reader)
        
        if len(data) != 0:
            self.student_table.delete(*self.student_table.get_children())
            for i in data:
                self.student_table.insert("", END, values=i)
    
    def get_cursor(self, event=""):
        cursor_focus = self.student_table.focus()
        content = self.student_table.item(cursor_focus)
        data = content["values"]
        
        if data:
            self.var_dep.set(data[0])
            self.var_course.set(data[1])
            self.var_year.set(data[2])
            self.var_semester.set(data[3])
            self.var_std_id.set(data[4])
            self.var_std_name.set(data[5])
            self.var_div.set(data[6])
            self.var_roll.set(data[7])
            self.var_gender.set(data[8])
            self.var_dob.set(data[9])
            self.var_email.set(data[10])
            self.var_phone.set(data[11])
            self.var_address.set(data[12])
            self.var_teacher.set(data[13])
            self.var_radio1.set(data[14])
    
    def update_data(self):
        if self.var_dep.get() == "Select Department" or self.var_std_name.get() == "" or self.var_std_id.get() == "":
            messagebox.showerror("Error", "All Fields are required", parent=self.root)
        else:
            try:
                if not os.path.exists("data/student.csv"):
                    messagebox.showerror("Error", "No data found", parent=self.root)
                    return
                
                data = []
                with open("data/student.csv", "r") as file:
                    reader = csv.reader(file)
                    data = list(reader)
                
                for i in range(len(data)):
                    if data[i][4] == self.var_std_id.get():
                        data[i] = [
                            self.var_dep.get(),
                            self.var_course.get(),
                            self.var_year.get(),
                            self.var_semester.get(),
                            self.var_std_id.get(),
                            self.var_std_name.get(),
                            self.var_div.get(),
                            self.var_roll.get(),
                            self.var_gender.get(),
                            self.var_dob.get(),
                            self.var_email.get(),
                            self.var_phone.get(),
                            self.var_address.get(),
                            self.var_teacher.get(),
                            self.var_radio1.get()
                        ]
                        break
                
                with open("data/student.csv", "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerows(data)
                
                messagebox.showinfo("Success", "Student details updated successfully", parent=self.root)
                self.fetch_data()
            except Exception as es:
                messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)
    
    def delete_data(self):
        if self.var_std_id.get() == "":
            messagebox.showerror("Error", "Student ID is required", parent=self.root)
        else:
            try:
                delete = messagebox.askyesno("Student Delete Page", "Do you want to delete this student", parent=self.root)
                if delete > 0:
                    if not os.path.exists("data/student.csv"):
                        messagebox.showerror("Error", "No data found", parent=self.root)
                        return
                    
                    data = []
                    with open("data/student.csv", "r") as file:
                        reader = csv.reader(file)
                        data = [row for row in reader if row[4] != self.var_std_id.get()]
                    
                    with open("data/student.csv", "w", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerows(data)
                    
                    messagebox.showinfo("Delete", "Student details deleted successfully", parent=self.root)
                    self.fetch_data()
                else:
                    if not delete:
                        return
            except Exception as es:
                messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)
    
    def reset_data(self):
        self.var_dep.set("Select Department")
        self.var_course.set("Select Course")
        self.var_year.set("Select Year")
        self.var_semester.set("Select Semester")
        self.var_std_id.set("")
        self.var_std_name.set("")
        self.var_div.set("A")
        self.var_roll.set("")
        self.var_gender.set("Male")
        self.var_dob.set("")
        self.var_email.set("")
        self.var_phone.set("")
        self.var_address.set("")
        self.var_teacher.set("")
        self.var_radio1.set("")
    
    # ==================== Generate data set or Take Photo Samples ====================
    def generate_dataset(self):
        if self.var_dep.get() == "Select Department" or self.var_std_name.get() == "" or self.var_std_id.get() == "":
            messagebox.showerror("Error", "All Fields are required", parent=self.root)
        else:
            try:
                # Create data directory if it doesn't exist
                if not os.path.exists("data"):
                    os.makedirs("data")
                
                # Load Haar Cascade
                face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
                
                if face_classifier.empty():
                    messagebox.showerror("Error", "Failed to load Haar Cascade file", parent=self.root)
                    return
                
                def face_cropped(img):
                    """Extract face from image with validation"""
                    if img is None or img.size == 0:
                        return None
                    
                    try:
                        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                        faces = face_classifier.detectMultiScale(gray, 1.3, 5)
                        
                        for (x, y, w, h) in faces:
                            face_cropped = img[y:y+h, x:x+w]
                            return face_cropped
                    except Exception as e:
                        print(f"Face detection error: {str(e)}")
                        return None
                    
                    return None
                
                # Open camera with robust backend selection
                cap, backend_name = open_camera_with_backend()
                
                if cap is None:
                    messagebox.showerror("Error", 
                        "Cannot access camera!\n\n"
                        "Please check:\n"
                        "1. Camera is connected\n"
                        "2. No other app is using camera\n"
                        "3. Camera permissions are enabled\n"
                        "4. Try restarting your computer", 
                        parent=self.root)
                    return
                
                messagebox.showinfo("Camera Ready", 
                    f"Camera opened with {backend_name}\n\n"
                    "✓ COLOR mode enabled\n"
                    "Press ENTER to stop capture\n"
                    "20 photos will be captured automatically", 
                    parent=self.root)
                
                img_id = 0
                
                try:
                    while True:
                        success, my_frame = safe_frame_read(cap)
                        
                        if not success or my_frame is None:
                            print("Warning: Failed to read frame, skipping...")
                            time.sleep(0.1)
                            continue
                        
                        cropped_face = face_cropped(my_frame)
                        
                        if cropped_face is not None:
                            img_id += 1
                            # Resize and KEEP COLOR (BGR format)
                            face = cv2.resize(cropped_face, (450, 450))
                            
                            # Save COLOR image (not grayscale)
                            file_name_path = f"data/user.{self.var_std_id.get()}.{img_id}.jpg"
                            cv2.imwrite(file_name_path, face)
                            
                            # Display the colored face with counter
                            display_face = face.copy()
                            cv2.putText(display_face, f"Photo {img_id}/20", (10, 30), 
                                       cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                            cv2.imshow("Capturing Color Images", display_face)
                        
                        # Stop after 20 images or when ENTER is pressed
                        key = cv2.waitKey(1) & 0xFF
                        if key == 13 or int(img_id) >= 20:
                            break
                
                except Exception as capture_error:
                    print(f"Capture error: {capture_error}")
                finally:
                    # Proper cleanup to avoid threading issues
                    if cap is not None:
                        cap.release()
                    
                    # Destroy windows with proper wait
                    cv2.destroyAllWindows()
                    cv2.waitKey(1)  # Process any pending window events
                    
                    # Small delay before showing messagebox
                    time.sleep(0.2)
                
                messagebox.showinfo("Success", 
                    f"Successfully captured {img_id} COLOR photos!\n\n"
                    f"Images saved in 'data' folder\n"
                    f"Data set generation completed!", 
                    parent=self.root)
                
            except Exception as es:
                messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)


# ==================== Train Data Window ====================
class Train:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Train Data")
        
        title_lbl = Label(self.root, text="TRAIN DATA SET", font=("times new roman", 35, "bold"), bg="white", fg="red")
        title_lbl.place(x=0, y=0, width=1530, height=45)
        
        # Button
        b1_1 = Button(self.root, text="TRAIN DATA", command=self.train_classifier, cursor="hand2",
                     font=("times new roman", 30, "bold"), bg="darkblue", fg="white")
        b1_1.place(x=0, y=380, width=1530, height=60)
        
        self.label = Label(self.root, text="", font=("times new roman", 20, "bold"), bg="white")
        self.label.place(x=0, y=450, width=1530, height=50)
    
    def train_classifier(self):
        data_dir = "data"
        path = [os.path.join(data_dir, file) for file in os.listdir(data_dir)]
        
        faces = []
        ids = []
        
        for image in path:
            img = Image.open(image).convert('L')  # Gray scale
            imageNp = np.array(img, 'uint8')
            id = int(os.path.split(image)[1].split('.')[1])
            
            faces.append(imageNp)
            ids.append(id)
            cv2.imshow("Training", imageNp)
            cv2.waitKey(1) == 13
        
        ids = np.array(ids)
        
        # Train the classifier
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces, ids)
        clf.write("classifier.xml")
        cv2.destroyAllWindows()
        self.label.config(text="Training datasets completed!!")
        messagebox.showinfo("Result", "Training datasets completed!!", parent=self.root)


# ==================== Face Recognition Window ====================
class FaceRecognition:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition")
        
        # Lazy import to avoid circulars at module load
        try:
            from advanced_attendance_system import open_best_camera
            self._open_best_camera = open_best_camera
        except Exception:
            self._open_best_camera = None

        # Initialize recognition components
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Config compatible with provided start/stop snippet (enable FaceNet by default)
        self.use_facenet = True
        self.model_file = "classifier.xml"  # Align with Train window output (LBPH fallback)
        self.names_file = "face_names.pkl"  # Optional (may not exist)
        self.names = []
        self.current_video = None
        self.recognition_active = False
        self.marked_today = set()
        # Advanced assets
        self.images_folder = "student_images"
        self.unknown_faces_folder = "unknown_faces"
        self.attendance_folder = "attendance_records"
        self.students_file = "students_database.csv"
        self.student_lookup_by_name = {}
        self.facenet_encodings = {}
        # Ensure folders
        for folder in [self.images_folder, self.unknown_faces_folder, self.attendance_folder]:
            if not os.path.exists(folder):
                try:
                    os.makedirs(folder)
                except Exception:
                    pass
        # Camera meta + FPS tracking
        self.current_camera_meta = None
        self._fps_counter = 0
        self._fps_t0 = time.time()
        self._fps_measured = 0.0
        # Load student database (for attendance enrichment)
        self._load_student_database()

        # UI
        title_lbl = Label(self.root, text="FACE RECOGNITION", font=("times new roman", 35, "bold"), bg="white", fg="green")
        title_lbl.place(x=0, y=0, width=1530, height=45)

        controls = Frame(self.root, bg="white")
        controls.place(x=0, y=55, width=1530, height=80)

        Button(controls, text="Start Recognition", command=self.start_recognition, cursor="hand2",
               font=("times new roman", 18, "bold"), bg="#27AE60", fg="white", width=20).pack(side=LEFT, padx=10, pady=10)
        Button(controls, text="Stop Recognition", command=self.stop_recognition, cursor="hand2",
               font=("times new roman", 18, "bold"), bg="#E74C3C", fg="white", width=20).pack(side=LEFT, padx=10, pady=10)
        Button(controls, text="Legacy Window", command=self.face_recog, cursor="hand2",
               font=("times new roman", 18, "bold"), bg="#8E44AD", fg="white", width=20).pack(side=LEFT, padx=10, pady=10)

        # Status + info
        self.status_label = Label(self.root, text="Status: Ready", font=("times new roman", 12, "bold"),
                                  bg="#2ECC71", fg="white")
        self.status_label.place(x=10, y=140, width=1510, height=30)

        # Video area
        self.video_label = Label(self.root, bg='black')
        self.video_label.place(x=10, y=180, width=1200, height=560)

        # Info panel
        info_frame = Frame(self.root, bg='white')
        info_frame.place(x=1220, y=180, width=300, height=560)
        Label(info_frame, text="Info", font=("times new roman", 16, "bold"), bg='white').pack(anchor='w', padx=10, pady=5)
        self.info_text = Text(info_frame, height=30, font=("Courier", 10), bg='#2C3E50', fg='#ECF0F1')
        self.info_text.pack(fill=BOTH, expand=True, padx=10, pady=5)
        self.update_info("Recognition window ready.")
    
    def mark_attendance(self, i, r, n, d):
        with open("attendance.csv", "r+", newline="\n") as f:
            myDataList = f.readlines()
            name_list = []
            for line in myDataList:
                entry = line.split(",")
                name_list.append(entry[0])
            
            if ((i not in name_list) and (r not in name_list) and (n not in name_list) and (d not in name_list)):
                now = datetime.now()
                d1 = now.strftime("%d/%m/%Y")
                dtString = now.strftime("%H:%M:%S")
                f.writelines(f"\n{i},{r},{n},{d},{dtString},{d1},Present")
    
    def face_recog(self):
        def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
            """Draw boundary around detected faces with validation"""
            if img is None or img.size == 0:
                return []
            
            try:
                gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)
                
                coord = []
                
                for (x, y, w, h) in features:
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 3)
                    id, predict = clf.predict(gray_image[y:y+h, x:x+w])
                    confidence = int((100 * (1 - predict / 300)))
                    
                    if not os.path.exists("data/student.csv"):
                        return coord
                    
                    with open("data/student.csv", "r") as file:
                        reader = csv.reader(file)
                        for row in reader:
                            if len(row) > 4 and row[4] == str(id):
                                i = row[4]
                                r = row[7]
                                n = row[5]
                                d = row[0]
                                
                                if confidence > 77:
                                    cv2.putText(img, f"ID: {i}", (x, y-75), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                                    cv2.putText(img, f"Roll: {r}", (x, y-55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                                    cv2.putText(img, f"Name: {n}", (x, y-30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                                    cv2.putText(img, f"Department: {d}", (x, y-5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                                    self.mark_attendance(i, r, n, d)
                                else:
                                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 3)
                                    cv2.putText(img, "Unknown Face", (x, y-5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                                
                                break
                    
                    coord = [x, y, w, h]
                
                return coord
            except Exception as e:
                print(f"Draw boundary error: {str(e)}")
                return []
        
        def recognize(img, clf, faceCascade):
            if img is not None and img.size > 0:
                coord = draw_boundary(img, faceCascade, 1.1, 10, (255, 25, 255), "Face", clf)
            return img
        
        try:
            # Load cascade and classifier
            faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
            
            if faceCascade.empty():
                messagebox.showerror("Error", "Failed to load Haar Cascade file", parent=self.root)
                return
            
            if not os.path.exists("classifier.xml"):
                messagebox.showerror("Error", "Classifier not found!\n\nPlease train the data first.", parent=self.root)
                return
            
            clf = cv2.face.LBPHFaceRecognizer_create()
            clf.read("classifier.xml")
            
            # Use optimized camera for better quality and reliability
            try:
                if OPTIMIZED_CAMERA_AVAILABLE:
                    camera = OptimizedCameraCapture(camera_index=0, resolution=(1280, 720))
                    messagebox.showinfo("Camera Ready",
                        "Optimized camera opened successfully!\n\n"
                        "Press ENTER to stop recognition",
                        parent=self.root)

                    try:
                        while True:
                            success, img = camera.capture_frame()

                            if not success or img is None:
                                print("Warning: Failed to read frame, skipping...")
                                time.sleep(0.1)
                                continue

                            img = recognize(img, clf, faceCascade)
                            cv2.imshow("Welcome To Face Recognition", img)

                            key = cv2.waitKey(1) & 0xFF
                            if key == 13:
                                break
                    finally:
                        camera.release()
                        cv2.destroyAllWindows()
                        cv2.waitKey(1)
                        time.sleep(0.2)
                else:
                    raise Exception("Optimized camera not available")

            except Exception as cam_error:
                print(f"Optimized camera error: {cam_error}")
                messagebox.showinfo("Info",
                    "Using standard camera mode...",
                    parent=self.root)

                # Fallback to original method
                video_cap, backend_name = open_camera_with_backend()

                if video_cap is None:
                    messagebox.showerror("Error",
                        "Cannot access camera!\n\n"
                        "Please check:\n"
                        "1. Camera is connected\n"
                        "2. No other app is using camera\n"
                        "3. Camera permissions are enabled\n"
                        "4. Try restarting your computer",
                        parent=self.root)
                    return

                messagebox.showinfo("Camera Ready",
                    f"Camera opened with {backend_name}\n\n"
                    "Press ENTER to stop recognition",
                    parent=self.root)

                try:
                    while True:
                        success, img = safe_frame_read(video_cap)

                        if not success or img is None:
                            print("Warning: Failed to read frame, skipping...")
                            time.sleep(0.1)
                            continue

                        img = recognize(img, clf, faceCascade)
                        cv2.imshow("Welcome To Face Recognition", img)

                        key = cv2.waitKey(1) & 0xFF
                        if key == 13:
                            break
                finally:
                    video_cap.release()
                    cv2.destroyAllWindows()
                    cv2.waitKey(1)
                    time.sleep(0.2)
            
        except Exception as e:
            messagebox.showerror("Error", f"Face Recognition Error: {str(e)}", parent=self.root)

    # ==================== New recognition controls (requested) ====================
    def update_status(self, message, color='#2ECC71'):
        try:
            self.status_label.config(text=f"Status: {message}", bg=color)
            self.root.update()
        except Exception:
            pass

    def update_info(self, message):
        try:
            ts = datetime.now().strftime("%H:%M:%S")
            self.info_text.insert(END, f"[{ts}] {message}\n")
            self.info_text.see(END)
            self.root.update()
        except Exception:
            # Fallback to console in case UI not ready
            print(message)

    def start_recognition(self):
        """Start face recognition"""
        if self.use_facenet:
            # Load FaceNet encodings
            self.update_status("Loading FaceNet encodings...", '#3498DB')
            self.update_info("Loading FaceNet encodings...")
            if not self._load_facenet_encodings():
                return
            self.update_info("✓ FaceNet encodings loaded successfully!")
        else:
            # Load LBPH model
            if not os.path.exists(self.model_file):
                messagebox.showerror("Error", "No trained model found! Please train the model first.")
                return
            try:
                self.recognizer.read(self.model_file)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load model: {e}")
                return
            if os.path.exists(self.names_file):
                try:
                    with open(self.names_file, 'rb') as f:
                        self.names = pickle.load(f)
                except Exception:
                    self.names = []
        self.update_status("Recognition active...", '#27AE60')
        self.update_info("Starting face recognition...")

        # Use robust camera selector
        cap = None
        if self._open_best_camera is not None:
            cap, meta = self._open_best_camera(lambda s: self.update_info(s))
        else:
            cap, meta = open_camera_with_backend()
        if cap is None:
            messagebox.showerror("Error", "Camera opened but sent only black frames. Close other apps using camera and try again.")
            return
        self.current_video = cap
        # Store camera meta and reset FPS counters
        if isinstance(meta, dict):
            self.current_camera_meta = meta
        else:
            self.current_camera_meta = {
                'backend': meta or 'Unknown',
                'codec': 'DEFAULT',
                'fps': int(cap.get(cv2.CAP_PROP_FPS) or 0),
            }
        self._fps_counter = 0
        self._fps_t0 = time.time()
        self._fps_measured = 0.0
        # Enrich meta with live width/height
        try:
            self.current_camera_meta['width'] = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
            self.current_camera_meta['height'] = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)
        except Exception:
            pass
        self.update_info(
            f"Camera selected: {self.current_camera_meta.get('backend','?')}/"
            f"{self.current_camera_meta.get('codec','?')} "
            f"{self.current_camera_meta.get('width','?')}x{self.current_camera_meta.get('height','?')}"
            f" @~{self.current_camera_meta.get('fps',0)}"
        )
        print(f"Recognition camera selected: {meta}")
        self.update_info("Camera ready - recognizing faces...")
        self.recognition_active = True
        self.marked_today = set()
        self.recognize_faces()

    def recognize_faces(self):
        """Recognize faces from live video and render into Tkinter label"""
        if not self.recognition_active or self.current_video is None:
            return
        ret, frame = self.current_video.read()
        # FPS measurement
        if ret and frame is not None and frame.size > 0:
            self._fps_counter += 1
            dt = time.time() - self._fps_t0
            if dt >= 1.0:
                self._fps_measured = self._fps_counter / max(dt, 1e-6)
                self._fps_counter = 0
                self._fps_t0 = time.time()
        if not ret or frame is None or frame.size == 0:
            # try once more before stopping
            ret2, frame2 = (self.current_video.read() if self.current_video else (False, None))
            if not ret2 or frame2 is None or frame2.size == 0:
                self.stop_recognition()
                return
            frame = frame2

        # Detect faces
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            if self.use_facenet:
                display_name = "Unknown"
                disp_color = (0, 0, 255)
                try:
                    padding = 20
                    y1 = max(0, y - padding)
                    y2 = min(frame.shape[0], y + h + padding)
                    x1 = max(0, x - padding)
                    x2 = min(frame.shape[1], x + w + padding)
                    face_img = frame[y1:y2, x1:x2]
                    if face_img.shape[0] < 50 or face_img.shape[1] < 50:
                        continue
                    # Save temp as BGR; DeepFace will handle loading
                    temp_face_path = "temp_face.jpg"
                    cv2.imwrite(temp_face_path, face_img)
                    # Lazy import to avoid heavy import on module load
                    try:
                        from deepface import DeepFace
                    except Exception as e:
                        self.update_info(f"DeepFace import error: {e}")
                        continue
                    embedding = DeepFace.represent(img_path=temp_face_path, model_name="Facenet", enforce_detection=False)
                    detected_encoding = np.array(embedding[0]['embedding'])
                    best_similarity = -1
                    recognized_name = "Unknown"
                    for student_name, stored_encoding in self.facenet_encodings.items():
                        stored_enc_array = np.array(stored_encoding)
                        # cosine similarity
                        denom = (np.linalg.norm(detected_encoding) * np.linalg.norm(stored_enc_array))
                        if denom == 0:
                            continue
                        cosine_similarity = float(np.dot(detected_encoding, stored_enc_array) / denom)
                        if cosine_similarity > best_similarity:
                            best_similarity = cosine_similarity
                            recognized_name = student_name
                    if best_similarity > 0.5:
                        display_name = recognized_name
                        disp_color = (0, 255, 0)
                        # attendance once per session by name
                        if display_name not in self.marked_today:
                            if self._mark_attendance_name(display_name):
                                self.update_info(f"✓ Attendance marked for: {display_name} (Similarity: {best_similarity:.2f})")
                            self.marked_today.add(display_name)
                    # cleanup temp
                    try:
                        if os.path.exists(temp_face_path):
                            os.remove(temp_face_path)
                    except Exception:
                        pass
                except Exception as e:
                    self.update_info(f"Recognition error: {e}")
                # Draw overlay
                cv2.rectangle(frame, (x, y), (x+w, y+h), disp_color, 2)
                cv2.rectangle(frame, (x, y-30), (x+w, y), disp_color, cv2.FILLED)
                cv2.putText(frame, display_name, (x+6, y-8), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                # Save unknown snapshots with throttling
                if display_name == "Unknown":
                    self._maybe_save_unknown_face(frame, x, y, w, h)
            else:
                # LBPH fallback
                face_roi = gray[y:y+h, x:x+w]
                try:
                    face_roi = cv2.resize(face_roi, (200, 200))
                except Exception:
                    continue
                try:
                    label, confidence = self.recognizer.predict(face_roi)
                except Exception:
                    label, confidence = -1, 999.0
                display_name = "Unknown"
                disp_color = (0, 0, 255)
                if confidence < 70 and label != -1:
                    student_id = str(label)
                    i = r = n = d = None
                    if os.path.exists("data/student.csv"):
                        try:
                            with open("data/student.csv", "r") as file:
                                reader = csv.reader(file)
                                for row in reader:
                                    if len(row) > 4 and row[4] == student_id:
                                        i = row[4]; r = row[7]; n = row[5]; d = row[0]
                                        display_name = f"{n}"
                                        disp_color = (0, 255, 0)
                                        key = (i, r, n, d)
                                        if key not in self.marked_today:
                                            try:
                                                self.mark_attendance(i, r, n, d)
                                                self.marked_today.add(key)
                                                self.update_info(f"✓ Attendance marked for: {n} ({i})")
                                            except Exception as e:
                                                self.update_info(f"Attendance mark error: {e}")
                                        break
                        except Exception as e:
                            self.update_info(f"CSV read error: {e}")
                cv2.rectangle(frame, (x, y), (x+w, y+h), disp_color, 2)
                cv2.rectangle(frame, (x, y-30), (x+w, y), disp_color, cv2.FILLED)
                cv2.putText(frame, display_name, (x+6, y-8), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # Add info overlay (mode, camera meta, FPS, brightness, timestamp)
        try:
            recognition_mode = "FaceNet" if self.use_facenet else "LBPH"
            cv2.putText(frame, f"Mode: {recognition_mode} | Recognized: {len(self.marked_today)}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            meta = self.current_camera_meta or {}
            curr_brightness = float(frame.mean()) if frame is not None and frame.size else 0.0
            res_w = frame.shape[1] if frame is not None else meta.get('width', '?')
            res_h = frame.shape[0] if frame is not None else meta.get('height', '?')
            meta_line1 = f"{meta.get('backend','?')}/{meta.get('codec','?')} | {res_w}x{res_h}"
            meta_line2 = f"Driver FPS~{meta.get('fps',0)} | Measured FPS~{self._fps_measured:.1f} | Brightness~{curr_brightness:.1f}"
            cv2.putText(frame, meta_line1, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            cv2.putText(frame, meta_line2, (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            cv2.putText(frame, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), (10, frame.shape[0]-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        except Exception:
            pass

        # Render to Tk Label
        try:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            # fit video area
            img = img.resize((1200, 560), Image.Resampling.LANCZOS)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
        except Exception:
            pass

        # schedule next frame
        self.root.after(10, self.recognize_faces)

    def stop_recognition(self):
        """Stop face recognition"""
        self.recognition_active = False
        if self.current_video:
            try:
                self.current_video.release()
            except Exception:
                pass
            self.current_video = None
        # Clear video display
        try:
            self.video_label.configure(image='')
            self.video_label.imgtk = None
        except Exception:
            pass
        # Clear meta/FPS
        self.current_camera_meta = None
        self._fps_counter = 0
        self._fps_measured = 0.0
        self.update_status("Recognition stopped", '#2ECC71')
        self.update_info("Face recognition stopped")

    # ==================== FaceNet helpers and attendance ====================
    def _load_student_database(self):
        if not os.path.exists(self.students_file):
            return
        try:
            with open(self.students_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    name_key = str(row.get('Name', '')).strip().lower()
                    if name_key:
                        self.student_lookup_by_name[name_key] = row
        except Exception as e:
            self.update_info(f"Student DB load error: {e}")

    def _load_facenet_encodings(self):
        self.facenet_encodings = {}
        if not os.path.exists(self.images_folder):
            messagebox.showerror("Error", "Student images folder not found!")
            return False
        encoding_files = [f for f in os.listdir(self.images_folder) if f.endswith('_encoding.pkl')]
        if len(encoding_files) == 0:
            messagebox.showerror("Error", "No FaceNet encodings found! Please capture student photos in Advanced System.")
            return False
        self.update_info(f"Found {len(encoding_files)} encoding files")
        for encoding_file in encoding_files:
            try:
                base_name = encoding_file.replace('_encoding.pkl', '')
                parts = base_name.split('_', 1)
                student_name = parts[1] if len(parts) >= 2 else parts[0]
                with open(os.path.join(self.images_folder, encoding_file), 'rb') as f:
                    encoding = pickle.load(f)
                    self.facenet_encodings[student_name] = encoding
                self.update_info(f"✓ Loaded encoding for: {student_name}")
            except Exception as e:
                self.update_info(f"Could not load {encoding_file}: {e}")
        return len(self.facenet_encodings) > 0

    def _mark_attendance_name(self, name: str) -> bool:
        from datetime import date
        today = date.today().strftime("%Y-%m-%d")
        attendance_file = os.path.join(self.attendance_folder, f"attendance_{today}.csv")
        is_new = not os.path.exists(attendance_file)
        try:
            # create file with header if new
            if is_new:
                with open(attendance_file, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['ID', 'Name', 'Department', 'Date', 'Time', 'Status'])
            else:
                # prevent duplicates (by exact name)
                with open(attendance_file, 'r') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if len(row) > 1 and row[1] == name:
                            return False
            # enrich from student DB
            sid = ''
            dept = ''
            rec = self.student_lookup_by_name.get(name.strip().lower()) if isinstance(name, str) else None
            if rec:
                sid = rec.get('ID', '')
                dept = rec.get('Department', '')
            with open(attendance_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([sid, name, dept, today, datetime.now().strftime("%H:%M:%S"), "Present"])
            return True
        except Exception as e:
            self.update_info(f"Attendance write error: {e}")
            return False

    def _maybe_save_unknown_face(self, frame, x, y, w, h):
        # throttle using attribute timestamp
        now = time.time()
        last = getattr(self, "_last_unknown_saved_at", 0.0)
        if now - last < 2.0:
            return
        setattr(self, "_last_unknown_saved_at", now)
        try:
            y1 = max(0, y-20); y2 = min(frame.shape[0], y+h+20)
            x1 = max(0, x-20); x2 = min(frame.shape[1], x+w+20)
            unknown_img = frame[y1:y2, x1:x2]
            if unknown_img.size > 0:
                ts = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
                save_path = os.path.join(self.unknown_faces_folder, f"unknown_{ts}.jpg")
                cv2.imwrite(save_path, unknown_img, [cv2.IMWRITE_JPEG_QUALITY, 95])
                self.update_info(f"Saved unknown face: {save_path}")
        except Exception as e:
            self.update_info(f"Could not save unknown face: {e}")


# ==================== Attendance Window ====================
class Attendance:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Attendance")
        
        title_lbl = Label(self.root, text="ATTENDANCE MANAGEMENT SYSTEM", 
                         font=("times new roman", 35, "bold"), bg="white", fg="darkgreen")
        title_lbl.place(x=0, y=0, width=1530, height=45)
        
        main_frame = Frame(self.root, bd=2, bg="white")
        main_frame.place(x=10, y=55, width=1510, height=730)
        
        # Left Frame
        Left_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE, 
                               text="Student Attendance Details", font=("times new roman", 12, "bold"))
        Left_frame.place(x=10, y=10, width=730, height=710)
        
        # Right Frame
        Right_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE, 
                                text="Attendance Details", font=("times new roman", 12, "bold"))
        Right_frame.place(x=750, y=10, width=750, height=710)
        
        # Table Frame
        table_frame = Frame(Right_frame, bd=2, bg="white", relief=RIDGE)
        table_frame.place(x=5, y=5, width=735, height=690)
        
        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)
        
        self.AttendanceReportTable = ttk.Treeview(table_frame, columns=("id", "roll", "name", "department", 
                                                                        "time", "date", "attendance"), 
                                                 xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.AttendanceReportTable.xview)
        scroll_y.config(command=self.AttendanceReportTable.yview)
        
        self.AttendanceReportTable.heading("id", text="Student ID")
        self.AttendanceReportTable.heading("roll", text="Roll")
        self.AttendanceReportTable.heading("name", text="Name")
        self.AttendanceReportTable.heading("department", text="Department")
        self.AttendanceReportTable.heading("time", text="Time")
        self.AttendanceReportTable.heading("date", text="Date")
        self.AttendanceReportTable.heading("attendance", text="Attendance")
        
        self.AttendanceReportTable["show"] = "headings"
        
        self.AttendanceReportTable.column("id", width=100)
        self.AttendanceReportTable.column("roll", width=100)
        self.AttendanceReportTable.column("name", width=100)
        self.AttendanceReportTable.column("department", width=100)
        self.AttendanceReportTable.column("time", width=100)
        self.AttendanceReportTable.column("date", width=100)
        self.AttendanceReportTable.column("attendance", width=100)
        
        self.AttendanceReportTable.pack(fill=BOTH, expand=1)
        
        self.fetch_data()
    
    def fetch_data(self):
        if os.path.exists("attendance.csv"):
            with open("attendance.csv", "r") as file:
                reader = csv.reader(file)
                data = list(reader)
            
            if len(data) != 0:
                self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())
                for i in data:
                    self.AttendanceReportTable.insert("", END, values=i)


# ==================== Developer Window ====================
class Developer:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Developer")
        
        title_lbl = Label(self.root, text="DEVELOPER", font=("times new roman", 35, "bold"), bg="white", fg="blue")
        title_lbl.place(x=0, y=0, width=1530, height=45)
        
        # Developer Info
        dev_label = Label(self.root, text="This Face Recognition System was developed using Python, OpenCV, and Tkinter", 
                         font=("times new roman", 20, "bold"), bg="white")
        dev_label.place(x=0, y=100, width=1530, height=100)


# ==================== Help Window ====================
class Help:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Help")
        
        title_lbl = Label(self.root, text="HELP & SUPPORT", font=("times new roman", 35, "bold"), bg="white", fg="blue")
        title_lbl.place(x=0, y=0, width=1530, height=45)
        
        # Help Info
        help_label = Label(self.root, text="For any help, please contact support@facereco.com", 
                          font=("times new roman", 20, "bold"), bg="white")
        help_label.place(x=0, y=100, width=1530, height=100)


if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition_System(root)
    root.mainloop()