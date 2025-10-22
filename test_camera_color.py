"""
Camera Test Script - Color Image Capture
Tests different camera backends and captures color images
"""
import cv2
import time
import os
from datetime import datetime

def test_camera_backends():
    """Test all available camera backends and indices"""
    print("=" * 60)
    print("CAMERA DETECTION TEST")
    print("=" * 60)
    
    backends = [
        (cv2.CAP_DSHOW, "DirectShow (Windows)"),
        (cv2.CAP_MSMF, "Media Foundation"),
        (0, "Default Backend")
    ]
    
    camera_indices = [0, 1, -1]
    working_cameras = []
    
    for backend, backend_name in backends:
        for camera_idx in camera_indices:
            try:
                print(f"\nTesting Camera {camera_idx} with {backend_name}...")
                
                # Open camera
                if isinstance(backend, int):
                    cap = cv2.VideoCapture(camera_idx)
                else:
                    cap = cv2.VideoCapture(camera_idx, backend)
                
                time.sleep(0.3)  # Wait for initialization
                
                if cap.isOpened():
                    # Try to read a frame
                    ret, frame = cap.read()
                    
                    if ret and frame is not None and frame.size > 0:
                        # Check if it's color (3 channels)
                        if len(frame.shape) == 3 and frame.shape[2] == 3:
                            print(f"  ✓ SUCCESS!")
                            print(f"    Resolution: {frame.shape[1]}x{frame.shape[0]}")
                            print(f"    Color Mode: BGR (3 channels)")
                            print(f"    Frame Size: {frame.size} bytes")
                            working_cameras.append((camera_idx, backend, backend_name))
                        else:
                            print(f"  ✗ Camera opened but returned grayscale image")
                    else:
                        print(f"  ✗ Camera opened but failed to read frame")
                    
                    cap.release()
                else:
                    print(f"  ✗ Failed to open camera")
                    
            except Exception as e:
                print(f"  ✗ Error: {str(e)}")
                try:
                    cap.release()
                except:
                    pass
    
    print("\n" + "=" * 60)
    print(f"SUMMARY: Found {len(working_cameras)} working camera(s)")
    print("=" * 60)
    
    return working_cameras

def capture_color_images(camera_idx=0, backend=cv2.CAP_DSHOW):
    """Capture and save color images"""
    print("\n" + "=" * 60)
    print("COLOR IMAGE CAPTURE TEST")
    print("=" * 60)
    
    # Open camera
    if isinstance(backend, int):
        cap = cv2.VideoCapture(camera_idx)
    else:
        cap = cv2.VideoCapture(camera_idx, backend)
    
    if not cap.isOpened():
        print("✗ Failed to open camera!")
        return False
    
    # Set properties
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # Create output directory
    output_dir = "test_images"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print("\nCamera opened successfully!")
    print("Controls:")
    print("  SPACE - Capture and save image")
    print("  'c'   - Capture without saving (test)")
    print("  'q'   - Quit")
    print("\nPress any key to start...")
    
    capture_count = 0
    
    while True:
        ret, frame = cap.read()
        
        if not ret or frame is None:
            print("✗ Failed to read frame")
            break
        
        # Verify it's color
        if len(frame.shape) != 3 or frame.shape[2] != 3:
            print("✗ Warning: Frame is not in color mode!")
        
        # Add status text
        status_text = f"Camera: {frame.shape[1]}x{frame.shape[0]} | Mode: COLOR (BGR) | Captured: {capture_count}"
        cv2.putText(frame, status_text, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        cv2.putText(frame, "SPACE=Capture | C=Test | Q=Quit", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        
        # Display frame
        cv2.imshow('Color Camera Test', frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        # Capture and save (SPACE key)
        if key == ord(' '):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{output_dir}/color_image_{timestamp}_{capture_count+1:03d}.jpg"
            
            success = cv2.imwrite(filename, frame)
            
            if success:
                capture_count += 1
                print(f"✓ Saved: {filename}")
                
                # Verify saved image
                test_img = cv2.imread(filename)
                if test_img is not None and len(test_img.shape) == 3:
                    print(f"  Verified: Image is COLOR ({test_img.shape})")
                else:
                    print(f"  ✗ Warning: Saved image may not be color!")
            else:
                print(f"✗ Failed to save image")
        
        # Test capture (without saving)
        elif key == ord('c'):
            print(f"Test capture - Frame shape: {frame.shape}, Color channels: {frame.shape[2]}")
        
        # Quit
        elif key == ord('q'):
            print("\nExiting...")
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    print(f"\n✓ Total images captured: {capture_count}")
    if capture_count > 0:
        print(f"✓ Images saved in: {os.path.abspath(output_dir)}")
    
    return True

def main():
    """Main test function"""
    print("\n" + "=" * 60)
    print("FACE RECOGNITION SYSTEM - CAMERA TEST")
    print("=" * 60)
    
    # Step 1: Detect cameras
    working_cameras = test_camera_backends()
    
    if not working_cameras:
        print("\n✗ No working cameras found!")
        print("\nTroubleshooting:")
        print("  1. Check if camera is connected")
        print("  2. Close other apps using camera (Skype, Teams, etc.)")
        print("  3. Check Windows Settings > Privacy > Camera")
        print("  4. Restart your computer")
        return
    
    # Step 2: Use the first working camera
    camera_idx, backend, backend_name = working_cameras[0]
    print(f"\n✓ Using Camera {camera_idx} with {backend_name}")
    
    # Step 3: Test color capture
    input("\nPress ENTER to start color image capture test...")
    capture_color_images(camera_idx, backend)
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
