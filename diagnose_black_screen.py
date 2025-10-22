"""
Diagnose Black Screen Issue with Camera
Tests various camera settings to find the issue
"""
import cv2
import numpy as np
import time

print("="*70)
print("CAMERA BLACK SCREEN DIAGNOSTIC")
print("="*70)

# Test different backends
backends = [
    (cv2.CAP_DSHOW, "DirectShow"),
    (cv2.CAP_MSMF, "Media Foundation"),
    (cv2.CAP_ANY, "Auto/Default")
]

for backend_id, backend_name in backends:
    print(f"\n{'='*70}")
    print(f"Testing: {backend_name} (ID: {backend_id})")
    print("="*70)
    
    cap = cv2.VideoCapture(0, backend_id)
    
    if not cap.isOpened():
        print(f"✗ Could not open camera with {backend_name}")
        continue
    
    print(f"✓ Camera opened with {backend_name}")
    
    # Get camera properties
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
    
    print(f"  Default Resolution: {width}x{height}")
    print(f"  FPS: {fps}")
    print(f"  FOURCC: {fourcc}")
    
    # Try to set properties
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    
    # Flush buffer
    print("  Flushing camera buffer...")
    for i in range(5):
        cap.read()
    time.sleep(0.3)
    
    # Test frame capture
    print("  Testing frame capture...")
    success_count = 0
    black_count = 0
    fail_count = 0
    
    for i in range(10):
        ret, frame = cap.read()
        
        if not ret:
            fail_count += 1
            print(f"    Frame {i+1}: ✗ Failed to read")
            continue
        
        if frame is None or frame.size == 0:
            fail_count += 1
            print(f"    Frame {i+1}: ✗ Empty frame")
            continue
        
        # Check if frame is all black or very dark
        mean_brightness = np.mean(frame)
        
        if mean_brightness < 5:
            black_count += 1
            print(f"    Frame {i+1}: ⚠ BLACK (mean={mean_brightness:.1f})")
        else:
            success_count += 1
            print(f"    Frame {i+1}: ✓ OK (shape={frame.shape}, mean={mean_brightness:.1f})")
        
        time.sleep(0.1)
    
    print(f"\n  RESULTS:")
    print(f"    ✓ Success: {success_count}/10")
    print(f"    ⚠ Black: {black_count}/10")
    print(f"    ✗ Failed: {fail_count}/10")
    
    # Try to display if we got good frames
    if success_count > 0:
        print(f"\n  Attempting to display live feed...")
        print(f"  Press 'q' to test next backend, 's' to save frame")
        
        frame_count = 0
        while frame_count < 100:  # Max 100 frames
            ret, frame = cap.read()
            
            if ret and frame is not None and frame.size > 0:
                frame_count += 1
                mean_brightness = np.mean(frame)
                
                # Add info overlay
                cv2.putText(frame, f"{backend_name} - Frame {frame_count}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(frame, f"Brightness: {mean_brightness:.1f}", (10, 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(frame, "Press 'q' to continue", (10, 90),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                cv2.imshow(f'Test: {backend_name}', frame)
                
                key = cv2.waitKey(30) & 0xFF
                if key == ord('q'):
                    print(f"  User quit after {frame_count} frames")
                    break
                elif key == ord('s'):
                    filename = f"test_{backend_name.replace('/', '_')}_{frame_count}.jpg"
                    cv2.imwrite(filename, frame)
                    print(f"  ✓ Saved: {filename}")
        
        cv2.destroyAllWindows()
    
    cap.release()
    time.sleep(0.5)

print("\n" + "="*70)
print("DIAGNOSTIC COMPLETE!")
print("="*70)
print("\nRECOMMENDATIONS:")
print("1. Use the backend that showed the most success")
print("2. If all frames were black, check:")
print("   - Camera privacy settings in Windows")
print("   - Camera is not covered or blocked")
print("   - Camera drivers are up to date")
print("   - Try a different camera app to verify hardware works")
print("="*70)
