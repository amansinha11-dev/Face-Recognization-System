"""
Simple Face Recognition Attendance System - OpenCV Only Version
Works without face_recognition library (Windows compatible)
Uses LBPH Face Recognizer for recognition
"""
import cv2
import numpy as np
import os
from datetime import datetime
import pickle

class SimpleFaceAttendance:
    def __init__(self):
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.names = []
        self.model_file = "face_model.yml"
        self.names_file = "face_names.pkl"
        self.attendance_file = "attendance.csv"
        
    def load_training_data(self, images_folder="images"):
        """Load and train from images folder"""
        print("="*60)
        print("Loading and training faces...")
        print("="*60)
        
        if not os.path.exists(images_folder):
            os.makedirs(images_folder)
            print(f"✗ Created {images_folder} folder. Please add student images there.")
            return False
            
        images = [f for f in os.listdir(images_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        if len(images) == 0:
            print(f"✗ No images found in {images_folder} folder!")
            return False
        
        faces_data = []
        labels = []
        
        for idx, image_file in enumerate(images):
            # Get name from filename
            name = os.path.splitext(image_file)[0]
            self.names.append(name)
            
            # Load image
            image_path = os.path.join(images_folder, image_file)
            image = cv2.imread(image_path)
            
            if image is None:
                print(f"✗ Failed to load: {image_file}")
                continue
            
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            if len(faces) == 0:
                print(f"✗ No face found in: {image_file}")
                continue
            
            # Use the first (largest) face found
            (x, y, w, h) = faces[0]
            face_roi = gray[y:y+h, x:x+w]
            face_roi = cv2.resize(face_roi, (200, 200))  # Normalize size
            
            faces_data.append(face_roi)
            labels.append(idx)
            
            print(f"✓ Loaded: {name}")
        
        if len(faces_data) == 0:
            print("\n✗ No valid face data loaded!")
            return False
        
        print(f"\nTotal faces loaded: {len(faces_data)}")
        print("Training model...")
        
        # Train the recognizer
        self.recognizer.train(faces_data, np.array(labels))
        
        # Save model
        self.recognizer.write(self.model_file)
        with open(self.names_file, 'wb') as f:
            pickle.dump(self.names, f)
        
        print(f"✓ Model saved to {self.model_file}")
        print(f"✓ Names saved to {self.names_file}")
        
        return True
    
    def load_model(self):
        """Load trained model"""
        if os.path.exists(self.model_file) and os.path.exists(self.names_file):
            self.recognizer.read(self.model_file)
            with open(self.names_file, 'rb') as f:
                self.names = pickle.load(f)
            print(f"✓ Loaded model with {len(self.names)} known faces")
            return True
        return False
    
    def mark_attendance(self, name):
        """Mark attendance in CSV file"""
        # Create file with header if it doesn't exist
        if not os.path.exists(self.attendance_file):
            with open(self.attendance_file, 'w') as f:
                f.write("Name,Date,Time\n")
        
        # Check if already marked today
        today = datetime.now().strftime("%Y-%m-%d")
        
        with open(self.attendance_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if name in line and today in line:
                    return False  # Already marked
        
        # Mark attendance
        with open(self.attendance_file, 'a') as f:
            now = datetime.now()
            date_string = now.strftime("%Y-%m-%d")
            time_string = now.strftime("%H:%M:%S")
            f.write(f"{name},{date_string},{time_string}\n")
        
        return True
    
    def start_recognition(self):
        """Start face recognition from webcam"""
        print("\n" + "="*60)
        print("Starting Face Recognition Attendance System")
        print("="*60)
        print("Controls:")
        print("  'q' - Quit")
        print("  'r' - Retrain model")
        print("="*60 + "\n")
        
        # Open webcam with DirectShow backend (Windows)
        video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        
        if not video_capture.isOpened():
            print("✗ Cannot access camera!")
            print("\nTrying alternative method...")
            video_capture = cv2.VideoCapture(0)
            
        if not video_capture.isOpened():
            print("✗ Still cannot access camera!")
            return
        
        # Set resolution
        video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        print("✓ Camera opened successfully")
        print("Looking for faces...\n")
        
        marked_today = set()
        frame_count = 0
        
        while True:
            ret, frame = video_capture.read()
            
            if not ret:
                print("Failed to grab frame")
                break
            
            frame_count += 1
            
            # Convert to grayscale for detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            # Process each detected face
            for (x, y, w, h) in faces:
                # Extract face ROI
                face_roi = gray[y:y+h, x:x+w]
                face_roi = cv2.resize(face_roi, (200, 200))
                
                # Recognize face
                try:
                    label, confidence = self.recognizer.predict(face_roi)
                    
                    # Confidence threshold (lower is better for LBPH)
                    if confidence < 70:  # Recognized
                        name = self.names[label] if label < len(self.names) else "Unknown"
                        color = (0, 255, 0)  # Green
                        
                        # Mark attendance
                        if name != "Unknown" and name not in marked_today:
                            if self.mark_attendance(name):
                                print(f"✓ Attendance marked: {name} at {datetime.now().strftime('%H:%M:%S')} (confidence: {confidence:.1f})")
                                marked_today.add(name)
                    else:
                        name = "Unknown"
                        color = (0, 0, 255)  # Red
                    
                    # Draw rectangle and label
                    cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                    cv2.rectangle(frame, (x, y-35), (x+w, y), color, cv2.FILLED)
                    
                    # Show name and confidence
                    text = f"{name} ({confidence:.1f})"
                    cv2.putText(frame, text, (x+6, y-6), 
                               cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
                
                except:
                    # No model or error in recognition
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                    cv2.putText(frame, "Unknown", (x, y-10), 
                               cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 255), 2)
            
            # Show FPS and info
            cv2.putText(frame, f"Recognized: {len(marked_today)}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, "Q=Quit | R=Retrain", (10, frame.shape[0]-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Display the frame
            cv2.imshow('Face Recognition Attendance - OpenCV', frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                print("\nExiting...")
                break
            elif key == ord('r'):
                print("\nRetraining model...")
                video_capture.release()
                cv2.destroyAllWindows()
                if self.load_training_data():
                    print("✓ Retraining complete!")
                    return self.start_recognition()
                break
        
        # Cleanup
        video_capture.release()
        cv2.destroyAllWindows()
        
        print("\n" + "="*60)
        print("Attendance Session Completed")
        print(f"Total people recognized today: {len(marked_today)}")
        if len(marked_today) > 0:
            print(f"Recognized: {', '.join(marked_today)}")
        print(f"Attendance saved to: {self.attendance_file}")
        print("="*60)

def main():
    """Main function"""
    print("="*60)
    print("FACE RECOGNITION ATTENDANCE SYSTEM")
    print("OpenCV LBPH Version (Windows Compatible)")
    print("="*60)
    
    system = SimpleFaceAttendance()
    
    # Try to load existing model
    if not system.load_model():
        print("\nNo trained model found. Training from images...")
        
        # Load and train from images
        if not system.load_training_data():
            print("\n" + "="*60)
            print("ERROR: No face data available!")
            print("="*60)
            print("\nPlease add student images to 'images' folder:")
            print("  1. Create 'images' folder if it doesn't exist")
            print("  2. Add photos named: StudentName.jpg")
            print("  3. Make sure faces are clearly visible")
            print("  4. Run this program again")
            print("\nExample:")
            print("  images/JohnDoe.jpg")
            print("  images/JaneSmith.jpg")
            print("  images/MikeBrown.jpg")
            print("="*60)
            return
    
    # Start recognition
    system.start_recognition()

if __name__ == "__main__":
    main()
