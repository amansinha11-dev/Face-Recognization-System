"""
Test Camera Script - Diagnose Camera Issues
This script tests camera access with different backends
"""
import cv2
import time

print("=" * 60)
print("CAMERA DIAGNOSTIC TOOL")
print("=" * 60)

# Check OpenCV build info
print("\n1. OpenCV Version:")
print(f"   {cv2.__version__}")
print(f"\n2. OpenCV Build Info (GUI Support):")
build_info = cv2.getBuildInformation()
for line in build_info.split('\n'):
    if 'GUI' in line or 'Win32' in line:
        print(f"   {line}")

print("\n3. Testing Camera Backends...")
print("-" * 60)

backends = [
    (cv2.CAP_DSHOW, "DirectShow (CAP_DSHOW)"),
    (cv2.CAP_MSMF, "Media Foundation (CAP_MSMF)"),
    (cv2.CAP_ANY, "Default (CAP_ANY)")
]

success = False
cap = None

for backend_id, backend_name in backends:
    print(f"\nTesting {backend_name}...")
    
    for camera_idx in [0, 1, 2]:
        try:
            print(f"  Camera Index {camera_idx}...", end=" ")
            cap = cv2.VideoCapture(camera_idx, backend_id)
            
            if cap.isOpened():
                # Configure camera
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                
                # Wait for initialization
                time.sleep(0.5)
                
                # Discard first few frames
                for _ in range(5):
                    cap.read()
                
                # Try to capture a frame
                ret, frame = cap.read()
                
                if ret and frame is not None and frame.size > 0:
                    print(f"✓ SUCCESS!")
                    print(f"    Frame shape: {frame.shape}")
                    print(f"    Frame size: {frame.size} pixels")
                    
                    # Save test image
                    filename = f"test_capture_{backend_name.split()[0]}_camera{camera_idx}.jpg"
                    cv2.imwrite(filename, frame)
                    print(f"    Test image saved: {filename}")
                    
                    success = True
                    
                    # Try to display the frame
                    try:
                        cv2.imshow("Camera Test - Press any key to continue", frame)
                        print(f"    Display window opened successfully!")
                        cv2.waitKey(2000)  # Show for 2 seconds
                        cv2.destroyAllWindows()
                    except Exception as display_error:
                        print(f"    Warning: Could not display window: {display_error}")
                    
                    cap.release()
                    break
                else:
                    print(f"✗ Failed (No valid frame)")
                    cap.release()
            else:
                print(f"✗ Failed (Cannot open)")
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            if cap:
                cap.release()
    
    if success:
        break

print("\n" + "=" * 60)
if success:
    print("RESULT: ✓ Camera is working!")
    print("Your Face Recognition System should work now.")
else:
    print("RESULT: ✗ Camera NOT accessible!")
    print("\nTroubleshooting steps:")
    print("1. Check if camera is physically connected")
    print("2. Close any apps using the camera (Zoom, Teams, etc.)")
    print("3. Check Windows Settings > Privacy > Camera permissions")
    print("4. Try a different USB port (for external webcams)")
    print("5. Restart your computer")
    print("6. Update camera drivers in Device Manager")
    print("7. Try an external USB webcam")
print("=" * 60)
