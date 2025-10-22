"""
Simple Camera Test - Diagnose OpenCV Camera Issues
"""
import cv2
import sys

print("=" * 60)
print("CAMERA TEST - OpenCV")
print("=" * 60)

# Test 1: Try DirectShow backend (Windows)
print("\n[Test 1] Trying DirectShow backend (cv2.CAP_DSHOW)...")
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if cap.isOpened():
    print("✓ Camera opened with DirectShow!")
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"  Resolution: {width}x{height}")
    print(f"  FPS: {fps}")
else:
    print("✗ DirectShow failed, trying default backend...")
    cap.release()
    cap = cv2.VideoCapture(0)
    
    if cap.isOpened():
        print("✓ Camera opened with default backend!")
    else:
        print("✗ Cannot open camera with any backend!")
        print("\nPossible issues:")
        print("  - Camera is being used by another application")
        print("  - Camera drivers not installed")
        print("  - Camera permissions not granted")
        sys.exit(1)

# Test 2: Read a frame
print("\n[Test 2] Testing frame capture...")
ret, frame = cap.read()

if ret:
    print(f"✓ Frame captured successfully!")
    print(f"  Frame shape: {frame.shape}")
    print(f"  Frame dtype: {frame.dtype}")
else:
    print("✗ Failed to capture frame!")
    cap.release()
    sys.exit(1)

# Test 3: Display the feed
print("\n[Test 3] Opening camera window...")
print("\nINSTRUCTIONS:")
print("  - Press 'q' to quit")
print("  - Press 's' to save a test image")
print("=" * 60)

frame_count = 0
while True:
    ret, frame = cap.read()
    
    if not ret:
        print(f"\n✗ Failed to read frame at count {frame_count}")
        break
    
    frame_count += 1
    
    # Add frame counter
    cv2.putText(frame, f"Frame: {frame_count}", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, "Press 'q' to quit | Press 's' to save", (10, 70), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    # Show the frame
    cv2.imshow('Camera Test - Press q to quit', frame)
    
    # Check for key press
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord('q'):
        print(f"\n✓ User quit. Total frames captured: {frame_count}")
        break
    elif key == ord('s'):
        filename = f"test_capture_{frame_count}.jpg"
        cv2.imwrite(filename, frame)
        print(f"✓ Saved: {filename}")

# Cleanup
cap.release()
cv2.destroyAllWindows()

print("\n" + "=" * 60)
print("CAMERA TEST COMPLETE!")
print("=" * 60)
