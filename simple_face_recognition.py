"""
Simple Face Recognition Attendance System
Using DeepFace library for accurate face recognition (No dlib required!)
"""
import cv2
import numpy as np
import os
from datetime import datetime
import pickle
from deepface import DeepFace

class FaceRecognitionAttendance:
    def __init__(self):
        self.known_face_paths = []
        self.known_face_names = []
        self.attendance_file = "attendance.csv"
        self.data_file = "face_data.pkl"
        self.is_trained = False

    def load_known_faces(self, images_folder="images"):
        """Load known faces from images folder using DeepFace"""
        print("Loading known faces with DeepFace...")

        if not os.path.exists(images_folder):
            os.makedirs(images_folder)
            print(f"Created {images_folder} folder. Please add student images there.")
            print("Format: StudentName.jpg or StudentName.png")
            return False

        self.known_face_paths = []
        self.known_face_names = []

        # Get all subdirectories (each student has their own folder)
        for student_name in os.listdir(images_folder):
            student_path = os.path.join(images_folder, student_name)

            if os.path.isdir(student_path):
                print(f"Processing: {student_name}")

                # Process all images for this student
                for image_file in os.listdir(student_path):
                    if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                        image_path = os.path.join(student_path, image_file)

                        # Store the image path and name
                        self.known_face_paths.append(image_path)
                        self.known_face_names.append(student_name)
                        print(f"  ✓ Added: {image_file}")

        if len(self.known_face_paths) == 0:
            print(f"No faces found in {images_folder} folder!")
            print("\nPlease organize images like this:")
            print("  images/")
            print("    StudentName1/")
            print("      photo1.jpg")
            print("      photo2.jpg")
            print("    StudentName2/")
            print("      photo1.jpg")
            return False

        self.is_trained = True
        print(f"✓ Training completed! {len(self.known_face_names)} students loaded")
        return True
    
    def save_data(self):
        """Save face data"""
        if not self.is_trained:
            print("Model not trained yet!")
            return

        data = {
            'paths': self.known_face_paths,
            'names': self.known_face_names
        }
        with open(self.data_file, 'wb') as f:
            pickle.dump(data, f)
        print(f"✓ Data saved to {self.data_file}")

    def load_data(self):
        """Load face data"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'rb') as f:
                data = pickle.load(f)
                self.known_face_paths = data['paths']
                self.known_face_names = data['names']
            self.is_trained = True
            print(f"✓ Loaded data with {len(self.known_face_names)} students")
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
        """Start face recognition from webcam using DeepFace"""
        if not self.is_trained:
            print("❌ Model not trained! Please train first.")
            return

        print("\n" + "="*50)
        print("Starting Face Recognition Attendance System")
        print("="*50)
        print("Controls:")
        print("  'q' - Quit")
        print("  's' - Save current data")
        print("="*50 + "\n")

        # Open webcam with DirectShow backend (Windows)
        video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        if not video_capture.isOpened():
            print("✗ Cannot access camera!")
            return

        print("✓ Camera opened successfully")
        print("Looking for faces...\n")

        marked_today = set()

        while True:
            ret, frame = video_capture.read()

            if not ret:
                print("Failed to grab frame")
                break

            # Save current frame to temp file for DeepFace
            temp_frame_path = "temp_frame.jpg"
            cv2.imwrite(temp_frame_path, frame)

            try:
                # Use DeepFace to find faces in the current frame
                detections = DeepFace.find(
                    img_path=temp_frame_path,
                    db_path="images",
                    model_name="VGG-Face",
                    enforce_detection=False,
                    silent=True
                )

                # Process detections
                for detection_df in detections:
                    if not detection_df.empty:
                        for _, row in detection_df.iterrows():
                            # Get the identity (filename)
                            identity = row['identity']
                            distance = row['distance']

                            # Extract name from path
                            name = os.path.basename(os.path.dirname(identity))

                            # Confidence threshold (lower distance = better match)
                            if distance < 0.3:  # Adjust threshold as needed
                                color = (0, 255, 0)  # Green for recognized

                                # Mark attendance
                                if name not in marked_today:
                                    if self.mark_attendance(name):
                                        print(f"✓ Attendance marked: {name} at {datetime.now().strftime('%H:%M:%S')}")
                                        marked_today.add(name)
                            else:
                                name = "Unknown"
                                color = (0, 0, 255)  # Red for unknown

                            # Get face location from the row data
                            if 'source_x' in row and 'source_y' in row and 'source_w' in row and 'source_h' in row:
                                x = int(row['source_x'])
                                y = int(row['source_y'])
                                w = int(row['source_w'])
                                h = int(row['source_h'])

                                # Draw rectangle around face
                                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)

                                # Draw label with name and confidence
                                confidence = int((1 - distance) * 100) if distance < 1 else 0
                                label_text = f"{name} ({confidence}%)"
                                cv2.rectangle(frame, (x, y-35), (x+w, y), color, cv2.FILLED)
                                cv2.putText(frame, label_text, (x+6, y-6),
                                            cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)

            except Exception as e:
                # If DeepFace fails, just show the frame without processing
                pass

            # Display the frame
            cv2.imshow('Face Recognition Attendance', frame)

            # Handle key presses
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                print("\nExiting...")
                break
            elif key == ord('s'):
                self.save_data()
                print("✓ Data saved!")

            # Clean up temp file
            if os.path.exists(temp_frame_path):
                os.remove(temp_frame_path)

        # Cleanup
        video_capture.release()
        cv2.destroyAllWindows()

        print("\n" + "="*50)
        print("Attendance Session Completed")
        print(f"Total people recognized: {len(marked_today)}")
        print(f"Attendance saved to: {self.attendance_file}")
        print("="*50)

def main():
    """Main function"""
    system = FaceRecognitionAttendance()
    
    print("="*50)
    print("Face Recognition Attendance System (face_recognition)")
    print("="*50)
    
    # Try to load existing model
    if not system.load_encodings():
        print("\nNo saved model found. Training from images...")
        
        # Load faces from images folder
        if not system.load_known_faces():
            print("\n❌ ERROR: No face data available!")
            print("\nPlease organize images like this:")
            print("  images/")
            print("    StudentName1/")
            print("      photo1.jpg")
            print("      photo2.jpg")
            print("      photo3.jpg")
            print("    StudentName2/")
            print("      photo1.jpg")
            print("      photo2.jpg")
            print("\nTip: Use the Advanced GUI System to easily capture student photos:")
            print("  python advanced_attendance_system.py")
            return
        
        # Save model for faster loading next time
        system.save_encodings()
    
    # Start recognition
    system.start_recognition()

if __name__ == "__main__":
    main()
