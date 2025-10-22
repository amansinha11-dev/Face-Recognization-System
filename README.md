# Face Recognition Attendance System

A complete Python-based attendance management system using face recognition technology with real-time detection, Excel reports, and secure login.

## 🎯 Features

### 1. **Login Security System** 
- Username & Password authentication
- Secure access control
- Multiple user support

**Default Credentials:**
- Username: `admin` | Password: `admin123`
- Username: `user` | Password: `user123`
- Username: `test` | Password: `test123`

### 2. **Student Management System**
- ✅ Add new students
- ✅ Update student information
- ✅ Delete student records
- ✅ Clear all fields
- ✅ Take photo samples (100 images per student)
- ✅ Search and filter students
- ✅ Export to CSV

**Student Fields:**
- Department, Course, Year, Semester
- Student ID, Name, Division, Roll Number
- Gender, DOB, Email, Phone, Address
- Teacher Name, Photo Sample

### 3. **Train Photo Samples**
- Automated training of face recognition model
- LBPH (Local Binary Patterns Histograms) algorithm
- Generates classifier.xml file
- Real-time training progress display

### 4. **Face Recognition & Attendance**
- Real-time face detection using Haar Cascade
- Automatic attendance marking
- Confidence threshold (77%)
- Shows student details on detection:
  - Student ID
  - Roll Number
  - Name
  - Department
- Saves to attendance.csv automatically

### 5. **Attendance Report System** ⭐ NEW
- 📊 View all attendance records
- 🔍 Search by:
  - Date
  - Student Name
  - Student ID
  - Department
- 📈 Real-time statistics (Total records, Present count)
- 📤 Export to Excel (.xlsx)
- 🗑️ Delete individual records
- 🔄 Reset filters
- 📋 Sortable table view

### 6. **Developer Page**
- System information
- Developer details
- Contact information

### 7. **Help Desk**
- User guide
- FAQ
- Troubleshooting tips

### 8. **Exit System**
- Confirmation dialog
- Proper resource cleanup

## 🖥️ System Requirements

### Software:
- Python 3.8 or higher
- Windows 10/11 (optimized for Windows)
- Webcam/Camera

### Python Packages:
```bash
pip install opencv-python opencv-contrib-python
pip install numpy pillow
pip install pandas openpyxl
```

Or install all at once:
```bash
pip install -r requirements.txt
```

## 📦 Installation

### Step 1: Clone/Download the project
```bash
cd "Face Recognization System"
```

### Step 2: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Verify camera
```bash
python test_camera.py
```

### Step 4: Run the application

**Option A: With Login System**
```bash
python login.py
```

**Option B: Direct Access**
```bash
python main.py
```

**Option C: Unified Launcher (Login first, then auto-open Main)**
On Windows, double-click `START_UNIFIED_SYSTEM.bat` or run:
```powershell
python unified_launcher.py
```

## 🚀 Usage Guide

### First Time Setup:

1. **Run Login**
   ```bash
   python login.py
   ```
   - Login with default credentials

2. **Add Students**
   - Click "Student Details"
   - Fill in student information
   - Click "Save"

3. **Take Photos**
   - Select student
   - Click "Take Photo Sample"
   - Wait for 100 photos to be captured
   - Press ENTER to stop early

4. **Train Model**
   - Click "Train Data"
   - Wait for training to complete
   - classifier.xml will be generated

5. **Mark Attendance**
   - Click "Face Detector"
   - Camera will open
   - Face will be detected and matched
   - Attendance saved automatically
   - Press ENTER to stop

6. **View Reports**
   - Click "Attendance" button
   - Search by date/name/ID
   - Export to Excel
   - Delete records if needed

### Process From a Video File (YouTube/RTSP/local)

If you have a recorded lecture/class video or a stream URL and want to auto-mark attendance using your known faces:

1. Prepare known faces inside `images/` (folders per student) or capture via the Advanced GUI (`student_images/`).
2. Run the video processor:

```powershell
python process_video_attendance.py --video "C:\path\to\class.mp4"
# Or webcam index
python process_video_attendance.py --video 0
# Or a network/RTSP URL
python process_video_attendance.py --video "rtsp://your-camera/stream"
```

Options:
- `--images <folder>`: choose faces source (defaults to `images` or `student_images`).
- `--threshold <0.0-1.0>`: cosine similarity threshold (default 0.5).
- `--every <N>`: process every Nth frame to keep it smooth (default 15).

Results are saved into `attendance_records/attendance_YYYY-MM-DD.csv`.

## 📁 File Structure

```
Face Recognization System/
│
├── main.py                          # Main application
├── login.py                         # Login system
├── process_video_attendance.py      # Mark attendance from a video file/stream
├── attendance_report.py             # Attendance report viewer
├── test_camera.py                   # Camera diagnostic tool
├── requirements.txt                 # Python dependencies
│
├── haarcascade_frontalface_default.xml  # Face detection model
├── classifier.xml                   # Trained face recognition model (generated)
│
├── data/                            # Student photos folder
│   └── user.<ID>.<number>.jpg      # Training images
│
├── images/                          # UI images (optional)
│
├── attendance.csv                   # Attendance records
└── data/student.csv                 # Student database
```

## 🎨 Button Layout

### Main Screen (4x2 Grid):

**Row 1:**
| Student Details | Face Detector | Attendance | Train Data |

**Row 2:**
| Photos | Developer | Help | Exit |

**Colors:**
- 🔵 Blue: Student Details, Developer
- 🔴 Red: Face Detector
- 🟢 Green: Attendance
- 🟣 Purple: Train Data
- 🟠 Orange: Photos
- 🟡 Yellow: Help
- 🩷 Pink: Exit

## 🔧 Configuration

### Adjust Button Sizes:
Edit `main.py`:
```python
btn_width = 250   # Button width
btn_height = 165  # Button height
btn_label_height = 48  # Label height
```

### Change Login Credentials:
Edit `login.py`:
```python
valid_users = {
    "admin": "admin123",
    "your_username": "your_password"
}
```

### Adjust Face Recognition Confidence:
Edit `main.py` (in face_recog method):
```python
if confidence > 77:  # Change threshold (0-100)
```

### Camera Resolution:
Edit `main.py` (in open_camera_with_backend):
```python
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
```

## 📊 Attendance Data Format

### attendance.csv:
```csv
StudentID,RollNo,Name,Department,Time,Date,Status
101,1001,John Doe,Computer Science,14:30:25,15/10/2025,Present
```

### student.csv:
```csv
Department,Course,Year,Semester,ID,Name,Division,Roll,Gender,DOB,Email,Phone,Address,Teacher,PhotoSample
```

## 🐛 Troubleshooting

### Camera Not Working:
1. Run diagnostic: `python test_camera.py`
2. Close other apps using camera
3. Check Windows camera permissions
4. Restart computer
5. Try external USB webcam

### Face Not Detected:
- Ensure good lighting
- Face camera directly
- Remove glasses/hat
- Train with more photos (100)
- Adjust Haar Cascade parameters

### Excel Export Error:
```bash
pip install pandas openpyxl
```

### Import Errors:
```bash
pip install --upgrade opencv-python opencv-contrib-python
```

## 🔐 Security Features

- ✅ Login authentication
- ✅ Password masking
- ✅ Exit confirmation
- ✅ Secure data storage
- ✅ Access control

## 📈 Future Enhancements

- [ ] MySQL database integration
- [ ] PDF report generation
- [ ] Email notifications
- [ ] SMS alerts
- [ ] Multiple camera support
- [ ] Cloud backup
- [ ] Mobile app
- [ ] Dashboard with charts
- [ ] QR code integration
- [ ] Fingerprint authentication

## 👨‍💻 Development

### Add New Features:
1. Create new window class in separate file
2. Import in `main.py`
3. Add button in main window
4. Link button to new window function

### Database Integration:
See commented MySQL code in requirements.txt

### Custom Styling:
Modify colors, fonts, and layouts in each class

## 📝 Credits

- **OpenCV**: Face detection and recognition
- **Pillow**: Image processing
- **pandas**: Excel export
- **tkinter**: GUI framework

## 📄 License

This project is for educational purposes.

## 📞 Support

For issues or questions:
1. Check troubleshooting section
2. Run test_camera.py for diagnostics
3. Verify all dependencies installed

## 🎓 Educational Use

Perfect for:
- College projects
- Learning Python
- Understanding face recognition
- GUI development
- OpenCV basics
- Attendance automation

---

**Developed with ❤️ using Python**

**Version:** 2.0  
**Last Updated:** October 15, 2025  
**Status:** ✅ Production Ready
