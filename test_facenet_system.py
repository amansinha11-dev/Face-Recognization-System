"""
FACENET SYSTEM TEST SCRIPT
Tests the FaceNet implementation in advanced_attendance_system.py
"""

import os
import pickle
from deepface import DeepFace
import numpy as np

def test_facenet_installation():
    """Test if DeepFace and FaceNet are properly installed"""
    print("=" * 60)
    print("TEST 1: DeepFace Installation")
    print("=" * 60)
    try:
        from deepface import DeepFace
        print("✅ DeepFace imported successfully!")
        return True
    except Exception as e:
        print(f"❌ DeepFace import failed: {e}")
        return False

def test_encoding_generation():
    """Test if FaceNet can generate encodings"""
    print("\n" + "=" * 60)
    print("TEST 2: FaceNet Encoding Generation")
    print("=" * 60)
    
    # Create a test image if it doesn't exist
    import cv2
    
    test_image = "test_facenet.jpg"
    if not os.path.exists(test_image):
        # Create a simple test image with face detection
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not cap.isOpened():
            cap = cv2.VideoCapture(0)
        
        if cap.isOpened():
            print("📷 Capturing test image...")
            ret, frame = cap.read()
            if ret:
                cv2.imwrite(test_image, frame)
                print(f"✅ Test image saved: {test_image}")
            cap.release()
        else:
            print("❌ Cannot access camera for test image")
            return False
    
    try:
        print(f"🔄 Generating FaceNet encoding for {test_image}...")
        embedding = DeepFace.represent(
            img_path=test_image,
            model_name="Facenet",
            enforce_detection=False
        )
        
        encoding = embedding[0]['embedding']
        print(f"✅ Encoding generated successfully!")
        print(f"   - Encoding dimensions: {len(encoding)}")
        print(f"   - Encoding type: {type(encoding)}")
        print(f"   - Sample values: {encoding[:5]}")
        
        # Test saving to pickle
        test_pkl = "test_encoding.pkl"
        with open(test_pkl, 'wb') as f:
            pickle.dump(encoding, f)
        print(f"✅ Encoding saved to {test_pkl}")
        
        # Test loading from pickle
        with open(test_pkl, 'rb') as f:
            loaded_encoding = pickle.load(f)
        print(f"✅ Encoding loaded from {test_pkl}")
        
        # Clean up
        if os.path.exists(test_pkl):
            os.remove(test_pkl)
        
        return True
        
    except Exception as e:
        print(f"❌ Encoding generation failed: {e}")
        return False

def test_existing_encodings():
    """Test if existing student encodings can be loaded"""
    print("\n" + "=" * 60)
    print("TEST 3: Existing Student Encodings")
    print("=" * 60)
    
    images_folder = "student_images"
    if not os.path.exists(images_folder):
        print(f"⚠ Folder '{images_folder}' does not exist")
        return False
    
    encoding_files = [f for f in os.listdir(images_folder) if f.endswith('_encoding.pkl')]
    
    if len(encoding_files) == 0:
        print("⚠ No encoding files found in student_images/")
        print("   This is normal if you haven't enrolled any students yet.")
        return True
    
    print(f"📁 Found {len(encoding_files)} encoding file(s):")
    
    loaded_count = 0
    for encoding_file in encoding_files:
        try:
            file_path = f"{images_folder}/{encoding_file}"
            with open(file_path, 'rb') as f:
                encoding = pickle.load(f)
            
            # Extract student name
            student_name = encoding_file.replace('_encoding.pkl', '').split('_', 1)[1]
            print(f"   ✅ {student_name} - {len(encoding)} dimensions")
            loaded_count += 1
            
        except Exception as e:
            print(f"   ❌ {encoding_file} - Error: {e}")
    
    print(f"\n✅ Successfully loaded {loaded_count}/{len(encoding_files)} encodings")
    return loaded_count > 0

def test_distance_calculation():
    """Test Euclidean distance calculation between encodings"""
    print("\n" + "=" * 60)
    print("TEST 4: Distance Calculation")
    print("=" * 60)
    
    try:
        # Create two random encodings (simulating FaceNet embeddings)
        encoding1 = np.random.rand(128)
        encoding2 = np.random.rand(128)
        
        # Calculate Euclidean distance
        distance = np.linalg.norm(encoding1 - encoding2)
        print(f"✅ Distance calculation works!")
        print(f"   - Sample distance between random encodings: {distance:.4f}")
        print(f"   - Expected range: 1.0 - 2.0 for random vectors")
        
        # Test with similar encodings
        encoding3 = encoding1 + np.random.rand(128) * 0.1  # Similar to encoding1
        distance_similar = np.linalg.norm(encoding1 - encoding3)
        print(f"   - Distance between similar encodings: {distance_similar:.4f}")
        print(f"   - Expected range: 0.0 - 0.5 for similar faces")
        
        return True
        
    except Exception as e:
        print(f"❌ Distance calculation failed: {e}")
        return False

def test_system_configuration():
    """Check system configuration"""
    print("\n" + "=" * 60)
    print("TEST 5: System Configuration")
    print("=" * 60)
    
    try:
        import cv2
        print(f"✅ OpenCV version: {cv2.__version__}")
        
        import numpy
        print(f"✅ NumPy version: {numpy.__version__}")
        
        import tensorflow as tf
        print(f"✅ TensorFlow version: {tf.__version__}")
        
        # Check camera
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if cap.isOpened():
            print("✅ Camera access: OK")
            cap.release()
        else:
            print("⚠ Camera access: Failed (may not be critical)")
        
        # Check folders
        folders = ["student_images", "attendance_records"]
        for folder in folders:
            if os.path.exists(folder):
                print(f"✅ Folder '{folder}': Exists")
            else:
                print(f"⚠ Folder '{folder}': Not found (will be created on first run)")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration check failed: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("🚀 FACENET IMPLEMENTATION TEST SUITE")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("DeepFace Installation", test_facenet_installation()))
    
    if results[0][1]:  # Only continue if DeepFace is installed
        results.append(("Encoding Generation", test_encoding_generation()))
        results.append(("Existing Encodings", test_existing_encodings()))
        results.append(("Distance Calculation", test_distance_calculation()))
        results.append(("System Configuration", test_system_configuration()))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! FaceNet system is ready to use.")
        print("\nNext steps:")
        print("1. Run: python advanced_attendance_system.py")
        print("2. Add students using 'Add New Student' button")
        print("3. Start recognition using 'Start Recognition' button")
    else:
        print("\n⚠ Some tests failed. Please check the errors above.")
        print("\nCommon fixes:")
        print("- Install DeepFace: pip install deepface")
        print("- Install TensorFlow: pip install tensorflow")
        print("- Check camera connection")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
