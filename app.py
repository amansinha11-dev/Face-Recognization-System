from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'face_recognition_secret_key_2025'

# Valid user credentials
VALID_USERS = {
    "admin": {"password": "admin123", "role": "Administrator", "name": "Admin"},
    "user": {"password": "user123", "role": "User", "name": "User"},
    "test": {"password": "test123", "role": "Test", "name": "Test"}
}

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/do_login', methods=['POST'])
def do_login():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    
    if username == "" or password == "":
        flash('All fields are required!', 'error')
        return redirect(url_for('login'))
    
    if username in VALID_USERS and VALID_USERS[username]["password"] == password:
        user_info = VALID_USERS[username]
        session['logged_in'] = True
        session['username'] = username
        session['name'] = user_info['name']
        session['role'] = user_info['role']
        flash(f'Welcome {user_info["name"]}!', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid username or password!', 'error')
        return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        flash('Please login first!', 'error')
        return redirect(url_for('login'))
    return render_template('dashboard.html', 
                          name=session.get('name'), 
                          role=session.get('role'))

@app.route('/run_face_recognition')
def run_face_recognition():
    if not session.get('logged_in'):
        flash('Please login first!', 'error')
        return redirect(url_for('login'))
    
    flash('Face Recognition System is not available in web deployment. This feature requires desktop application.', 'error')
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully!', 'success')
    return redirect(url_for('login'))

    # Student Details Route
@app.route('/student_details')
def student_details():
    if not session.get('logged_in'):
        flash('Please login first!', 'error')
        return redirect(url_for('login'))
    
    # Sample student data
    students = [
        {'id': 1, 'name': 'John Doe', 'email': 'john@example.com', 'enrollment': '2024-01-15'},
        {'id': 2, 'name': 'Jane Smith', 'email': 'jane@example.com', 'enrollment': '2024-02-10'},
        {'id': 3, 'name': 'Mike Johnson', 'email': 'mike@example.com', 'enrollment': '2024-03-20'},
        {'id': 4, 'name': 'Sarah Williams', 'email': 'sarah@example.com', 'enrollment': '2024-01-25'},
        {'id': 5, 'name': 'Tom Brown', 'email': 'tom@example.com', 'enrollment': '2024-04-05'},
    ]
    return render_template('student_details.html', students=students, name=session.get('name'), role=session.get('role'))

# Attendance Records Route
@app.route('/attendance')
def attendance():
    if not session.get('logged_in'):
        flash('Please login first!', 'error')
        return redirect(url_for('login'))
    
    # Sample attendance data
    attendance_records = [
        {'id': 1, 'name': 'John Doe', 'date': '2025-11-07', 'time': '09:15 AM', 'status': 'Present'},
        {'id': 2, 'name': 'Jane Smith', 'date': '2025-11-07', 'time': '09:20 AM', 'status': 'Present'},
        {'id': 3, 'name': 'Mike Johnson', 'date': '2025-11-07', 'time': '09:35 AM', 'status': 'Late'},
        {'id': 4, 'name': 'Sarah Williams', 'date': '2025-11-06', 'time': '09:10 AM', 'status': 'Present'},
        {'id': 5, 'name': 'Tom Brown', 'date': '2025-11-06', 'time': '---', 'status': 'Absent'},
    ]
    return render_template('attendance.html', records=attendance_records, name=session.get('name'), role=session.get('role'))

# Train Data Route
@app.route('/train_data')
def train_data():
    if not session.get('logged_in'):
        flash('Please login first!', 'error')
        return redirect(url_for('login'))
    
    return render_template('train_data.html', name=session.get('name'), role=session.get('role'))

# Photos Gallery Route
@app.route('/photos')
def photos():
    if not session.get('logged_in'):
        flash('Please login first!', 'error')
        return redirect(url_for('login'))
    
    # Sample photos data
    photo_gallery = [
        {'id': 1, 'name': 'Capture_001.jpg', 'date': '2025-11-07', 'student': 'John Doe'},
        {'id': 2, 'name': 'Capture_002.jpg', 'date': '2025-11-07', 'student': 'Jane Smith'},
        {'id': 3, 'name': 'Capture_003.jpg', 'date': '2025-11-06', 'student': 'Mike Johnson'},
        {'id': 4, 'name': 'Capture_004.jpg', 'date': '2025-11-06', 'student': 'Sarah Williams'},
        {'id': 5, 'name': 'Capture_005.jpg', 'date': '2025-11-05', 'student': 'Tom Brown'},
    ]
    return render_template('photos.html', photos=photo_gallery, name=session.get('name'), role=session.get('role'))

# Developer Info Route
@app.route('/developer')
def developer():
    if not session.get('logged_in'):
        flash('Please login first!', 'error')
        return redirect(url_for('login'))
    
    developer_info = {
        'name': 'Aman Sinha',
        'email': 'amansinha11.dev@gmail.com',
        'github': 'https://github.com/amansinha11-dev',
        'project': 'Face Recognition Attendance System',
        'version': '1.0.0',
        'year': '2025',
        'description': 'Advanced face recognition system for automated attendance tracking using Flask and facial recognition technology.'
    }
    return render_template('developer.html', dev_info=developer_info, name=session.get('name'), role=session.get('role'))

# Help & Documentation Route
@app.route('/help')
def help():
    if not session.get('logged_in'):
        flash('Please login first!', 'error')
        return redirect(url_for('login'))
    
    help_items = [
        {'title': 'Student Details', 'description': 'View and manage all registered students in the system. Click on a student to view detailed information.'},
        {'title': 'Face Detector', 'description': 'Start the face recognition system to detect and identify faces. This feature is available only in desktop mode.'},
        {'title': 'Attendance Records', 'description': 'View all attendance records. Filter by date, student name, or status to find specific records.'},
        {'title': 'Train Data', 'description': 'Train the face recognition model with new face data. Upload face images to improve accuracy.'},
        {'title': 'Photos Gallery', 'description': 'Browse all captured face images from the system. Download or delete photos as needed.'},
        {'title': 'Account', 'description': 'Manage your account settings. Change password or update profile information.'},
    ]
    return render_template('help.html', help_items=help_items, name=session.get('name'), role=session.get('role'))
