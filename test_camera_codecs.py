"""
Test camera with Windows-specific fixes for black screen issue
"""
import cv2
import numpy as np
import time

print("="*70)
print("TESTING CAMERA WITH WINDOWS FIXES")
print("="*70)

# Method 1: Try with explicit FOURCC codec
print("\n[Method 1] Testing with explicit MJPG codec...")
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if cap.isOpened():
    # Try setting MJPEG codec explicitly
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    # Flush buffer
    for _ in range(10):
        cap.read()
    time.sleep(0.5)
    
    ret, frame = cap.read()
    if ret and frame is not None:
        mean = np.mean(frame)
        print(f"  MJPG Result: {'✓ SUCCESS' if mean > 5 else '✗ BLACK'} (mean={mean:.1f})")
        if mean > 5:
            cv2.imshow('MJPG Test', frame)
            cv2.waitKey(2000)
            cv2.destroyAllWindows()
    cap.release()

# Method 2: Try with YUYV codec
print("\n[Method 2] Testing with YUYV codec...")
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if cap.isOpened():
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('Y','U','Y','V'))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    for _ in range(10):
        cap.read()
    time.sleep(0.5)
    
    ret, frame = cap.read()
    if ret and frame is not None:
        mean = np.mean(frame)
        print(f"  YUYV Result: {'✓ SUCCESS' if mean > 5 else '✗ BLACK'} (mean={mean:.1f})")
        if mean > 5:
            cv2.imshow('YUYV Test', frame)
            cv2.waitKey(2000)
            cv2.destroyAllWindows()
    cap.release()

# Method 3: Try Media Foundation with longer warmup
print("\n[Method 3] Testing Media Foundation with longer warmup...")
cap = cv2.VideoCapture(0, cv2.CAP_MSMF)

if cap.isOpened():
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    print("  Warming up camera for 2 seconds...")
    # Longer warmup time
    for i in range(60):  # ~2 seconds at 30fps
        cap.read()
        if i % 10 == 0:
            print(f"    Reading frame {i}...")
    
    time.sleep(1)
    
    ret, frame = cap.read()
    if ret and frame is not None:
        mean = np.mean(frame)
        print(f"  MSMF Result: {'✓ SUCCESS' if mean > 5 else '✗ BLACK'} (mean={mean:.1f})")
        if mean > 5:
            cv2.imshow('MSMF Test', frame)
            cv2.waitKey(2000)
            cv2.destroyAllWindows()
    cap.release()

# Method 4: Try VFW (Video for Windows) - legacy but sometimes works
print("\n[Method 4] Testing VFW (legacy)...")
cap = cv2.VideoCapture(0, cv2.CAP_VFW)

if cap.isOpened():
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    for _ in range(10):
        cap.read()
    time.sleep(0.5)
    
    ret, frame = cap.read()
    if ret and frame is not None:
        mean = np.mean(frame)
        print(f"  VFW Result: {'✓ SUCCESS' if mean > 5 else '✗ BLACK'} (mean={mean:.1f})")
        if mean > 5:
            cv2.imshow('VFW Test', frame)
            cv2.waitKey(2000)
            cv2.destroyAllWindows()
    cap.release()

# Method 5: Try different camera index
print("\n[Method 5] Testing camera index 1...")
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

if cap.isOpened():
    for _ in range(10):
        cap.read()
    time.sleep(0.5)
    
    ret, frame = cap.read()
    if ret and frame is not None:
        mean = np.mean(frame)
        print(f"  Camera 1 Result: {'✓ SUCCESS' if mean > 5 else '✗ BLACK'} (mean={mean:.1f})")
        if mean > 5:
            cv2.imshow('Camera 1 Test', frame)
            cv2.waitKey(2000)
            cv2.destroyAllWindows()
    cap.release()
else:
    print("  Camera index 1 not available")

print("\n" + "="*70)
print("TESTING COMPLETE!")
print("="*70)
