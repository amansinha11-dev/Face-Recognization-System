from flask import Flask, render_template, request, redirect, url_for, flash, session
import subprocess
import sys
import os

app = Flask(__name__)
app.secret_key = 'face_recognition_secret_key_2025'

# Valid user credentials (matching login.py)
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
    
    try:
        # Launch main.py (Face Recognition System)
        subprocess.Popen([sys.executable, 'main.py'])
        flash('Face Recognition System launched successfully!', 'success')
    except Exception as e:
        flash(f'Error launching Face Recognition System: {str(e)}', 'error')
    
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully!', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Check if required files exist
    if not os.path.exists('main.py'):
        print('Warning: main.py not found!')
    if not os.path.exists('login.py'):
        print('Warning: login.py not found!')
    
    print('Starting Flask Web Application...')
    print('Access the application at: http://localhost:5000')
    app.run(debug=True, host='0.0.0.0', port=5000)
