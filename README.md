# 🎓 Face Recognition Attendance System

A comprehensive face recognition-based attendance management system built with Python, OpenCV, and Tkinter. This system uses advanced facial recognition algorithms (LBPH and FaceNet) to automatically mark student attendance.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.5+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Table of Contents

- [Features](#features)
- [Screenshots](#screenshots)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [How It Works](#how-it-works)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## ✨ Features

### Core Functionality
- 👤 **Student Management** - Add, update, delete student records with complete details
- 📸 **Photo Capture** - Automated face sample collection (20+ images per student)
- 🎯 **Face Detection** - Real-time face detection using Haar Cascade
- 🧠 **Dual Recognition System**:
  - LBPH (Local Binary Patterns Histograms) for basic recognition
  - FaceNet deep learning model for advanced accuracy
- ✅ **Automated Attendance** - Real-time attendance marking with timestamp
- 📊 **Attendance Reports** - View and export attendance records

### User Interface
- 🎨 **Modern GUI** - Clean, intuitive interface with animated icons
- 🎬 **Animated Buttons** - GIF animations for interactive experience
- 📱 **Responsive Design** - Optimized window layouts
- 🎭 **Visual Feedback** - Color-coded buttons and status indicators

### Advanced Features
- 🎥 **Optimized Camera** - Multiple backend support (DirectShow, MSMF, etc.)
- 🔍 **Unknown Face Detection** - Saves snapshots of unrecognized faces
- 📁 **Database Management** - CSV-based storage for easy data handling
- 🔄 **Model Training** - Custom LBPH face recognizer training
- 🎯 **High Accuracy** - Confidence threshold filtering (77%+)

## 📸 Screenshots

### Main Dashboard
![Main Dashboard](images/Three%20colour%20images.png)

The main interface provides easy access to all system features with animated icon buttons.

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Webcam/Camera
- Windows/Linux/Mac OS

### Step 1: Clone the Repository

```bash
git clone https://github.com/amansinha11-dev/Face-Recognization-System.git
cd Face-Recognization-System
```

### Step 2: Install Required Packages

```bash
pip install -r requirements.txt
```

### Step 3: Install Additional Dependencies

```bash
pip install opencv-python opencv-contrib-python
pip install pillow
pip install numpy
pip install deepface
pip install tf-keras
```

### Step 4: Verify Installation

```bash
python main.py
```

## 📖 Usage

### 1️⃣ Add Student Details

1. Click on **"Student Details"** button
2. Fill in student information:
   - Department, Course, Year, Semester
   - Student ID, Name, Division, Roll Number
   - Gender, DOB, Email, Phone
   - Address, Teacher Name
3. Click **"Save"** to store the record

### 2️⃣ Capture Photos

1. In Student Details window, select student
2. Choose **"Take Photo Sample"** radio button
3. Click **"Take Photo Sample"** button
4. Camera opens - face the camera
5. System captures 20 photos automatically
6. Press **ENTER** when complete

### 3️⃣ Train the Model

1. Click **"Train Data"** button from main menu
2. System processes all captured photos
3. Creates `classifier.xml` model file
4. Wait for "Training completed" message

### 4️⃣ Mark Attendance

1. Click **"Face Detector"** button
2. Camera opens with real-time recognition
3. System automatically detects and recognizes faces
4. Attendance marked automatically with:
   - Student ID
   - Name
   - Department
   - Timestamp
5. Press **ENTER** to stop

### 5️⃣ View Attendance

1. Click **"Attendance"** button
2. View all attendance records
3. Filter by date, student, or department
4. Export to CSV if needed

## 📁 Project Structure

```
Face-Recognization-System/
│
├── main.py                          # Main application entry point
├── advanced_attendance_system.py    # FaceNet-based advanced system
├── simple_opencv_attendance.py      # LBPH-based basic system
├── attendance_report.py             # Attendance viewing and reports
├── optimized_camera.py              # Enhanced camera handling
├── unified_launcher.py              # System launcher
│
├── data/                            # Student database
│   └── student.csv                  # Student records
│
├── images/                          # UI Icons and images
│   ├── Student Details.jpg
│   ├── Face Detector.gif
│   ├── Attendance.png
│   ├── Train Data.png
│   ├── Photos.gif
│   ├── Developer.gif
│   ├── help.gif
│   ├── Exit.gif
│   └── Three colour images.png
│
├── student_images/                  # Stored student photos
├── unknown_faces/                   # Unrecognized face snapshots
├── attendance_records/              # Daily attendance CSV files
│
├── haarcascade_frontalface_default.xml  # Face detection model
├── classifier.xml                   # Trained LBPH model (generated)
├── students_database.csv            # Complete student database
│
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## 🛠️ Technologies Used

### Programming Language
- **Python 3.8+** - Core programming language

### Computer Vision & ML
- **OpenCV** - Face detection and recognition
- **DeepFace** - FaceNet model implementation
- **NumPy** - Numerical operations
- **TensorFlow/Keras** - Deep learning backend

### GUI Framework
- **Tkinter** - Desktop GUI application
- **PIL (Pillow)** - Image processing and display

### Data Management
- **CSV** - Database storage
- **Pickle** - Model serialization

### Algorithms
- **Haar Cascade** - Face detection
- **LBPH** - Local Binary Patterns Histogram face recognition
- **FaceNet** - Deep learning face recognition
- **Cosine Similarity** - Face matching metric

## 🔧 How It Works

### 1. Face Detection
```
Camera Input → Grayscale Conversion → Haar Cascade Detection → Face ROI Extraction
```

### 2. Training Process (LBPH)
```
Collect Samples → Convert to Grayscale → Extract Features → Train LBPH Model → Save classifier.xml
```

### 3. Recognition Process
```
Detect Face → Extract Features → Compare with Trained Model → 
Match Found (Confidence > 77%) → Mark Attendance
```

### 4. FaceNet Recognition
```
Detect Face → Extract 128D Embedding → Calculate Cosine Similarity → 
Similarity > 0.5 → Identify Student → Mark Attendance
```

## ⚙️ Configuration

### Camera Settings
Edit in `main.py` or `optimized_camera.py`:
```python
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)   # Camera width
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)   # Camera height
cap.set(cv2.CAP_PROP_FPS, 30)             # Frame rate
```

### Recognition Threshold
Adjust confidence threshold in `main.py`:
```python
if confidence > 77:  # Change this value (0-100)
    # Recognize student
```

### FaceNet Similarity Threshold
Modify in `advanced_attendance_system.py`:
```python
if best_similarity > 0.5:  # Change this value (0-1)
    # Recognize student
```

## 🎯 Key Components

### Student Details Module
- Complete student information management
- CRUD operations (Create, Read, Update, Delete)
- Photo sample collection
- Data validation

### Face Recognition Module
- Real-time face detection
- Dual recognition engines (LBPH + FaceNet)
- Confidence-based filtering
- Unknown face handling

### Training Module
- Automated dataset processing
- LBPH model generation
- Progress visualization
- Model persistence

### Attendance Module
- Automatic attendance marking
- Duplicate prevention (same session)
- CSV export functionality
- Date-wise organization

## 📊 Database Schema

### students_database.csv
```csv
ID, Name, Department, Course, Year, Semester, Division, Roll, Gender, DOB, Email, Phone, Address, Teacher
```

### attendance_records/attendance_YYYY-MM-DD.csv
```csv
ID, Name, Department, Date, Time, Status
```

## 🔒 Security Features

- ✅ Input validation
- ✅ Duplicate attendance prevention
- ✅ Confidence threshold filtering
- ✅ Unknown face logging
- ✅ Secure file handling

## 🐛 Troubleshooting

### Camera Not Opening
```python
# Check camera permissions
# Try different camera indices (0, 1, 2)
# Close other applications using camera
```

### Low Recognition Accuracy
```python
# Capture more training samples (30-50 images)
# Ensure good lighting during capture
# Train model again after adding samples
# Adjust confidence threshold
```

### Performance Issues
```python
# Reduce camera resolution
# Lower frame rate
# Use LBPH instead of FaceNet for faster recognition
```

## 🚧 Future Enhancements

- [ ] Cloud database integration (MySQL/PostgreSQL)
- [ ] Multi-camera support
- [ ] Email notifications for attendance
- [ ] Mobile app integration
- [ ] Admin dashboard with analytics
- [ ] Face mask detection
- [ ] Multiple face recognition in single frame
- [ ] Attendance statistics and graphs
- [ ] Export to Excel/PDF
- [ ] User authentication system

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Developer

**Aman Sinha**
- GitHub: [@amansinha11-dev](https://github.com/amansinha11-dev)
- Repository: [Face-Recognization-System](https://github.com/amansinha11-dev/Face-Recognization-System)

## 🙏 Acknowledgments

- OpenCV community for excellent documentation
- DeepFace library for FaceNet implementation
- Python Tkinter for GUI framework
- All contributors and testers

## 📞 Contact & Support

For support, email: sinhaaman473@gmail.com
For issues and bugs: [GitHub Issues](https://github.com/amansinha11-dev/Face-Recognization-System/issues)

---

**⭐ Star this repository if you find it helpful!**

