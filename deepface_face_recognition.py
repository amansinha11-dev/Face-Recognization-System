"""
Simple Face Recognition Attendance System using DeepFace
DeepFace provides high accuracy face recognition without requiring dlib
"""
import cv2
import numpy as np
import os
from datetime import datetime
import pickle
from deepface import DeepFace

class DeepFaceRecognitionAttendance:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.attendance_file = "attendance_deepface.csv"
        self.encodings_file = "face_encodings_deepface.pkl"
        self.names_file = "face_names_deepface.pkl"
        self.is_trained = False

    def load_known_faces(self, images_folder="images"):
        """Load and encode faces from images folder using DeepFace"""
        print("Loading known faces with DeepFace...")

        if not os.path.exists(images_folder):
            os.makedirs(images_folder)
            print(f"Created {images_folder} folder. Please add student images there.")
            print("Format: StudentName.jpg or StudentName.png")
            return False

        self.known_face_encodings = []
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

                        try:
                            # Use DeepFace to represent (encode) the face
                            embedding = DeepFace.represent(img_path=image_path, model_name="Facenet", enforce_detection=False)

                            if len(embedding) > 0:
                                self.known_face_encodings.append(embedding[0]['embedding'])
                                self.known_face_names.append(student_name)
                                print(f"  ✓ Encoded face from {image_file}")
                            else:
                                print(f"  ✗ No face found in {image_file}")
                        except Exception as e:
                            print(f"  ✗ Error processing {image_file}: {str(e)}")

        if len(self.known_face_encodings) == 0:
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

    def save_encodings(self):
        """Save face encodings and names"""
        if not self.is_trained:
            print("Model not trained yet!")
            return

        with open(self.encodings_file, 'wb') as f:
            pickle.dump(self.known_face_encodings, f)
        with open(self.names_file, 'wb') as f:
            pickle.dump(self.known_face_names, f)
        print(f"✓ Encodings saved to {self.encodings_file}")

    def load_encodings(self):
        """Load face encodings and names"""
        if os.path.exists(self.encodings_file) and os.path.exists(self.names_file):
            with open(self.encodings_file, 'rb') as f:
                self.known_face_encodings = pickle.load(f)
            with open(self.names_file, 'rb') as f:
                self.known_face_names = pickle.load(f)
            self.is_trained = True
            print(f"✓ Loaded encodings with {len(self.known_face_names)} students")
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
        print("Starting DeepFace Recognition Attendance System")
        print("="*50)
        print("Controls:")
        print("  'q' - Quit")
        print("  's' - Save current encodings")
        print("="*50 + "\n")

        # Open webcam with DirectShow backend (Windows)
        video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        if not video_capture.isOpened():
            print("✗ Cannot access camera!")
            return

        print("✓ Camera opened successfully")
        print("Looking for faces...\n")

        marked_today = set()
        frame_count = 0
        process_every_n_frames = 30  # Process only every 30th frame to avoid lag
        temp_image_path = "temp_frame.jpg"

        while True:
            ret, frame = video_capture.read()

            if not ret or frame is None or frame.size == 0:
                print("Failed to grab frame")
                continue

            # Only process face recognition every N frames
            frame_count += 1
            should_process = (frame_count % process_every_n_frames == 0)

            if should_process:
                # Save frame temporarily for DeepFace
                temp_image_path = "temp_frame.jpg"
                cv2.imwrite(temp_image_path, frame)

                try:
                    # Use DeepFace to find faces in the frame
                    faces = DeepFace.extract_faces(img_path=temp_image_path, enforce_detection=False, detector_backend='opencv')

                    for face_data in faces:
                        facial_area = face_data['facial_area']
                        x, y, w, h = facial_area['x'], facial_area['y'], facial_area['w'], facial_area['h']

                        # Get face embedding
                        embedding = DeepFace.represent(img_path=temp_image_path, model_name="Facenet", enforce_detection=False, detector_backend='opencv')

                        if len(embedding) > 0:
                            face_embedding = embedding[0]['embedding']

                            # Compare with known faces
                            min_distance = float('inf')
                            best_match_name = "Unknown"

                            for known_embedding, name in zip(self.known_face_encodings, self.known_face_names):
                                # Calculate cosine distance
                                distance = np.linalg.norm(np.array(known_embedding) - np.array(face_embedding))
                                if distance < min_distance:
                                    min_distance = distance
                                    best_match_name = name

                            # Threshold for recognition
                            if min_distance < 0.8:  # Adjust threshold as needed
                                name = best_match_name
                                color = (0, 255, 0)  # Green for recognized

                                # Mark attendance
                                if name not in marked_today:
                                    if self.mark_attendance(name):
                                        print(f"✓ Attendance marked: {name} at {datetime.now().strftime('%H:%M:%S')}")
                                        marked_today.add(name)
                            else:
                                name = "Unknown"
                                color = (0, 0, 255)  # Red for unknown

                            # Draw rectangle around face
                            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

                            # Draw label with name
                            confidence = max(0, int((1 - min_distance) * 100))
                            label_text = f"{name} ({confidence}%)"
                            cv2.rectangle(frame, (x, y + h - 35), (x + w, y + h), color, cv2.FILLED)
                            cv2.putText(frame, label_text, (x + 6, y + h - 6),
                                        cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)

                except Exception as e:
                    # Silently continue if face detection fails
                    pass

            # Display the frame
            cv2.imshow('DeepFace Recognition Attendance', frame)

            # Handle key presses
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                print("\nExiting...")
                break
            elif key == ord('s'):
                self.save_encodings()
                print("✓ Encodings saved!")

        # Cleanup
        video_capture.release()
        cv2.destroyAllWindows()
        
        # Clean up temp file
        try:
            if os.path.exists(temp_image_path):
                os.remove(temp_image_path)
        except:
            pass

        print("\n" + "="*50)
        print("Attendance Session Completed")
        print(f"Total people recognized: {len(marked_today)}")
        print(f"Attendance saved to: {self.attendance_file}")
        print("="*50)

def main():
    """Main function"""
    system = DeepFaceRecognitionAttendance()

    print("="*50)
    print("Face Recognition Attendance System (DeepFace)")
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
