"""
Unified Launcher
- Opens the Login window first
- After successful login, launches the classic main app by default
- Exposes a `main()` function so it can be imported and tested easily

Extendable: You can change `launch_after_login()` to open the advanced GUI
(advanced_attendance_system.py) or show a small selection menu.
"""
from tkinter import Tk

def launch_classic_main():
    import main
    root = Tk()
    app = main.Face_Recognition_System(root)
    root.mainloop()


def launch_advanced_gui():
    import advanced_attendance_system as adv
    root = Tk()
    app = adv.AdvancedFaceAttendanceSystem(root)
    root.mainloop()


def launch_after_login():
    # Default: classic main
    launch_classic_main()
    # Alternative: advanced FaceNet GUI
    # launch_advanced_gui()


def main():
    from login import LoginWindow
    root = Tk()
    # Pass a callback so that after successful login we control what opens next
    app = LoginWindow(root, on_success=launch_after_login)
    root.mainloop()


if __name__ == "__main__":
    main()
