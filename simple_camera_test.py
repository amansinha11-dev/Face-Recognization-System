"""
Simple Camera Test - No Tkinter Interference
Tests camera opening and color image capture
"""
import cv2
import os
import time

def simple_camera_test():
    """Simple camera test without Tkinter"""
    print("=" * 60)
    print("SIMPLE CAMERA TEST")
    print("=" * 60)
    
    # Fix threading issues
    cv2.setNumThreads(1)
    
    # Try to open camera
    print("\n1. Opening camera with DirectShow...")
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
    if not cap.isOpened():
        print("   ✗ Failed with DirectShow, trying default...")
        cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("   ✗ FAILED: Cannot open camera!")
        print("\nTroubleshooting:")
        print("  - Close other apps using camera (Zoom, Skype, Teams)")
        print("  - Check Windows Settings > Privacy > Camera")
        print("  - Restart your computer")
        return False
    
    # Set properties
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    
    print("   ✓ Camera opened successfully!")
    
    # Warm up camera
    print("\n2. Warming up camera...")
    for i in range(10):
        ret, frame = cap.read()
        time.sleep(0.1)
    print("   ✓ Camera warmed up")
    
    # Test frame capture
    print("\n3. Testing frame capture...")
    ret, frame = cap.read()
    
    if not ret or frame is None:
        print("   ✗ FAILED: Cannot read frame!")
        cap.release()
        return False
    
    print(f"   ✓ Frame captured: {frame.shape}")
    print(f"   ✓ Color channels: {frame.shape[2]}")
    print(f"   ✓ Resolution: {frame.shape[1]}x{frame.shape[0]}")
    
    # Verify color
    if frame.shape[2] == 3:
        print("   ✓ COLOR MODE: YES (BGR format)")
    else:
        print("   ✗ COLOR MODE: NO (Grayscale)")
    
    # Create output directory
    output_dir = "camera_test_output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print(f"\n4. Starting live preview...")
    print("\nControls:")
    print("  SPACE - Capture and save image")
    print("  'q'   - Quit")
    print("  ENTER - Quit")
    
    capture_count = 0
    
    try:
        while True:
            ret, frame = cap.read()
            
            if not ret or frame is None:
                print("Failed to read frame!")
                break
            
            # Add text overlay
            text = f"Captures: {capture_count} | Press SPACE to save | Q to quit"
            cv2.putText(frame, text, (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Show frame
            cv2.imshow('Simple Camera Test - COLOR', frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            
            # Save image (SPACE)
            if key == ord(' '):
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"{output_dir}/color_{timestamp}_{capture_count+1}.jpg"
                
                success = cv2.imwrite(filename, frame)
                if success:
                    capture_count += 1
                    print(f"✓ Saved: {filename}")
                else:
                    print(f"✗ Failed to save: {filename}")
            
            # Quit (q or ENTER)
            elif key == ord('q') or key == 13:
                print("\nExiting...")
                break
    
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    
    finally:
        # Proper cleanup
        cap.release()
        cv2.destroyAllWindows()
        cv2.waitKey(1)
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)
    print(f"Total images captured: {capture_count}")
    if capture_count > 0:
        print(f"Images saved in: {os.path.abspath(output_dir)}")
    
    return True

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("FACE RECOGNITION SYSTEM - SIMPLE CAMERA TEST")
    print("This test runs independently without Tkinter")
    print("=" * 60)
    
    success = simple_camera_test()
    
    if success:
        print("\n✓ Camera is working correctly!")
        print("You can now use the main Face Recognition System.")
    else:
        print("\n✗ Camera test failed!")
        print("Please fix camera issues before using the main system.")
    
    input("\nPress ENTER to exit...")
