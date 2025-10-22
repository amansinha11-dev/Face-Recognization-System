"""
Debug script to test face recognition and encodings
"""

import os
import pickle
import numpy as np
from deepface import DeepFace
import cv2

def test_encodings():
    """Test if encodings are properly loaded and compared"""
    
    images_folder = "student_images"
    
    print("=" * 60)
    print("DEBUGGING FACE RECOGNITION SYSTEM")
    print("=" * 60)
    
    # 1. List all files in student_images folder
    print("\n1. FILES IN STUDENT_IMAGES FOLDER:")
    if os.path.exists(images_folder):
        files = os.listdir(images_folder)
        for f in files:
            print(f"   - {f}")
    else:
        print("   ERROR: student_images folder not found!")
        return
    
    # 2. Load all encodings
    print("\n2. LOADING ENCODINGS:")
    encodings = {}
    encoding_files = [f for f in files if f.endswith('_encoding.pkl')]
    
    for enc_file in encoding_files:
        base_name = enc_file.replace('_encoding.pkl', '')
        parts = base_name.split('_', 1)
        
        if len(parts) >= 2:
            student_name = parts[1]
        else:
            student_name = parts[0]
        
        try:
            with open(f"{images_folder}/{enc_file}", 'rb') as f:
                encoding = pickle.load(f)
                encodings[student_name] = np.array(encoding)
                print(f"   ✓ Loaded: {student_name}")
                print(f"      - Encoding shape: {np.array(encoding).shape}")
                print(f"      - Encoding type: {type(encoding)}")
                print(f"      - First 5 values: {np.array(encoding)[:5]}")
        except Exception as e:
            print(f"   ✗ Error loading {enc_file}: {e}")
    
    # 3. Test recognition with camera
    print("\n3. TESTING LIVE RECOGNITION:")
    print("   Opening camera... Press 'c' to capture and test, 'q' to quit")
    
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("   ERROR: Cannot access camera!")
        return
    
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        cv2.putText(frame, "Press 'c' to test recognition, 'q' to quit", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.imshow('Debug Recognition Test', frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            break
        elif key == ord('c'):
            if len(faces) > 0:
                print("\n   Face detected! Testing recognition...")
                
                # Save temp face
                temp_path = "debug_temp_face.jpg"
                cv2.imwrite(temp_path, frame)
                
                try:
                    # Generate embedding
                    print("   Generating FaceNet embedding...")
                    embedding = DeepFace.represent(
                        img_path=temp_path,
                        model_name="Facenet",
                        enforce_detection=False
                    )
                    
                    detected_encoding = np.array(embedding[0]['embedding'])
                    print(f"   Detected encoding shape: {detected_encoding.shape}")
                    print(f"   First 5 values: {detected_encoding[:5]}")
                    
                    # Compare with all stored encodings
                    print("\n   COMPARISON RESULTS:")
                    for student_name, stored_encoding in encodings.items():
                        # Euclidean distance
                        euclidean = np.linalg.norm(detected_encoding - stored_encoding)
                        
                        # Cosine similarity
                        cosine = np.dot(detected_encoding, stored_encoding) / (
                            np.linalg.norm(detected_encoding) * np.linalg.norm(stored_encoding)
                        )
                        
                        print(f"\n   {student_name}:")
                        print(f"      Euclidean Distance: {euclidean:.2f}")
                        print(f"      Cosine Similarity: {cosine:.4f} ({cosine * 100:.1f}%)")
                        
                        if cosine > 0.5:
                            print(f"      ✓ MATCH! (similarity > 50%)")
                        else:
                            print(f"      ✗ No match (similarity < 50%)")
                    
                    # Clean up
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                        
                except Exception as e:
                    print(f"   ✗ Error: {e}")
            else:
                print("   No face detected!")
    
    cap.release()
    cv2.destroyAllWindows()
    
    print("\n" + "=" * 60)
    print("DEBUG COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    test_encodings()
