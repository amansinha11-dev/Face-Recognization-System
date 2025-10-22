"""
Button Layout Quick Reference
Face Recognition Attendance System
"""

# ===== OPTIMIZED BUTTON CONFIGURATION =====

# Dimensions (All buttons use these exact values)
BUTTON_WIDTH = 300
BUTTON_HEIGHT = 200
LABEL_HEIGHT = 50

# Spacing Calculation
TOTAL_WIDTH = 1366
SPACING = (TOTAL_WIDTH - (4 * BUTTON_WIDTH)) // 5  # = 33px

# Vertical Positioning
TITLE_Y = 0
TITLE_HEIGHT = 55
ROW1_Y = 70
ROW1_LABEL_Y = 270  # (70 + 200)
ROW2_Y = 335        # (270 + 50 + 15)
ROW2_LABEL_Y = 535  # (335 + 200)

# Horizontal Positioning (4 columns)
COL1_X = 33         # spacing
COL2_X = 366        # spacing + (300 + spacing)
COL3_X = 699        # spacing + 2*(300 + spacing)
COL4_X = 1032       # spacing + 3*(300 + spacing)

# ===== BUTTON DETAILS =====

BUTTONS = {
    'Student Details': {
        'position': (COL1_X, ROW1_Y),
        'color': '#0000FF',  # Blue
        'command': 'student_details'
    },
    'Face Detector': {
        'position': (COL2_X, ROW1_Y),
        'color': '#FF0000',  # Red
        'command': 'face_recognition'
    },
    'Attendance': {
        'position': (COL3_X, ROW1_Y),
        'color': '#008000',  # Green
        'command': 'attendance'
    },
    'Train Data': {
        'position': (COL4_X, ROW1_Y),
        'color': '#800080',  # Purple
        'command': 'train_data'
    },
    'Photos': {
        'position': (COL1_X, ROW2_Y),
        'color': '#FFA500',  # Orange
        'command': 'open_img'
    },
    'Developer': {
        'position': (COL2_X, ROW2_Y),
        'color': '#00FFFF',  # Cyan
        'command': 'developer'
    },
    'Help': {
        'position': (COL3_X, ROW2_Y),
        'color': '#FFFF00',  # Yellow
        'command': 'help'
    },
    'Exit': {
        'position': (COL4_X, ROW2_Y),
        'color': '#FFC0CB',  # Pink
        'command': 'exit_app'
    }
}

# ===== STYLE SETTINGS =====

BUTTON_STYLE = {
    'cursor': 'hand2',
    'bd': 0,
    'relief': 'FLAT'
}

LABEL_STYLE = {
    'font': ('Arial', 16, 'bold'),
    'bg': 'darkblue',
    'fg': 'white',
    'bd': 0,
    'relief': 'FLAT',
    'activebackground': 'blue',
    'cursor': 'hand2'
}

# ===== LAYOUT VALIDATION =====

# Check if all buttons fit
TOTAL_HEIGHT_USED = ROW2_LABEL_Y + LABEL_HEIGHT  # 585px
AVAILABLE_HEIGHT = 558  # Background label height
FITS = TOTAL_HEIGHT_USED <= AVAILABLE_HEIGHT  # False ✗

print(f"Total height used: {TOTAL_HEIGHT_USED}px")
print(f"Available height: {AVAILABLE_HEIGHT}px")
print(f"Remaining space: {AVAILABLE_HEIGHT - TOTAL_HEIGHT_USED}px")
print(f"Layout fits: {'✓ YES' if FITS else '✗ NO'}")

# ===== USAGE EXAMPLE =====

"""
# In your Tkinter code:

def create_button_image(color, width, height):
    img = Image.new('RGB', (width, height), color=color)
    return ImageTk.PhotoImage(img)

# For each button:
self.photoimg1 = create_button_image('#0000FF', 300, 200)
b1 = Button(bg_lbl, image=self.photoimg1, command=self.student_details,
            cursor='hand2', bd=0, relief=FLAT)
b1.place(x=33, y=70, width=300, height=200)

b1_label = Button(bg_lbl, text="Student Details", command=self.student_details,
                  font=("Arial", 16, "bold"), bg="darkblue", fg="white",
                  bd=0, relief=FLAT, activebackground="blue", cursor="hand2")
b1_label.place(x=33, y=270, width=300, height=50)
"""
