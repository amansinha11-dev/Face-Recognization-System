"""
Optimized Camera Capture for Face Recognition
Fixes low quality camera issues with HD resolution and proper settings
"""
import cv2
import numpy as np
import time


def fix_camera_quality(camera_index=0):
    """
    Quick fix function to improve camera quality
    Drop-in replacement for cv2.VideoCapture()
    
    Args:
        camera_index: Camera device index (default 0)
    
    Returns:
        Configured VideoCapture object with optimized settings
    """
    # Use CAP_DSHOW backend for better Windows camera control
    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
    
    if not cap.isOpened():
        print("Warning: CAP_DSHOW failed, trying default backend")
        cap = cv2.VideoCapture(camera_index)
    
    # Set MJPG codec for better quality and performance
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
    
    # Set HD resolution (1280x720)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    # Set manual exposure for consistent lighting
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)  # Manual mode
    cap.set(cv2.CAP_PROP_EXPOSURE, -6)  # Adjust based on lighting
    
    # Optimize other settings
    cap.set(cv2.CAP_PROP_BRIGHTNESS, 128)  # 0-255, 128 is neutral
    cap.set(cv2.CAP_PROP_CONTRAST, 32)     # Increase contrast
    cap.set(cv2.CAP_PROP_SATURATION, 64)   # Color saturation
    cap.set(cv2.CAP_PROP_SHARPNESS, 128)   # Sharpness
    cap.set(cv2.CAP_PROP_GAIN, 0)          # Reduce gain/noise
    
    # Set focus to auto or manual (if supported)
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
    
    # Set FPS
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    # Reduce buffer to minimize lag
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    
    # Let camera warm up
    time.sleep(0.5)
    
    # Discard first few frames
    for _ in range(5):
        cap.read()
    
    print(f"✓ Camera optimized:")
    print(f"  Resolution: {int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}")
    print(f"  FPS: {int(cap.get(cv2.CAP_PROP_FPS))}")
    print(f"  Backend: CAP_DSHOW")
    
    return cap


class OptimizedCameraCapture:
    """
    Advanced camera capture class with quality optimization and face detection
    """
    
    def __init__(self, camera_index=0, resolution=(1280, 720)):
        """
        Initialize optimized camera capture
        
        Args:
            camera_index: Camera device index
            resolution: Tuple (width, height) for camera resolution
        """
        self.camera_index = camera_index
        self.resolution = resolution
        self.cap = None
        self.initialize_camera()
    
    def initialize_camera(self):
        """Initialize camera with optimized settings"""
        print("Initializing optimized camera...")
        
        # Try CAP_DSHOW first (best for Windows)
        self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)
        
        if not self.cap.isOpened():
            print("Warning: CAP_DSHOW failed, trying CAP_MSMF")
            self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_MSMF)
        
        if not self.cap.isOpened():
            print("Warning: CAP_MSMF failed, using default backend")
            self.cap = cv2.VideoCapture(self.camera_index)
        
        if not self.cap.isOpened():
            raise RuntimeError("Failed to open camera!")
        
        # Apply optimal settings
        self._apply_optimal_settings()
        
        # Verify settings
        self._verify_settings()
        
        # Warm up camera
        self._warm_up()
    
    def _apply_optimal_settings(self):
        """Apply all optimal camera settings"""
        # Codec
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        
        # Resolution
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
        
        # Exposure control
        self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)  # Manual
        self.cap.set(cv2.CAP_PROP_EXPOSURE, -6)
        
        # Image quality
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, 128)
        self.cap.set(cv2.CAP_PROP_CONTRAST, 32)
        self.cap.set(cv2.CAP_PROP_SATURATION, 64)
        self.cap.set(cv2.CAP_PROP_SHARPNESS, 128)
        self.cap.set(cv2.CAP_PROP_GAIN, 0)
        
        # Focus
        self.cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
        
        # Performance
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    
    def _verify_settings(self):
        """Verify and display current camera settings"""
        print("\n✓ Camera Settings:")
        print(f"  Resolution: {int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}")
        print(f"  FPS: {int(self.cap.get(cv2.CAP_PROP_FPS))}")
        print(f"  Brightness: {int(self.cap.get(cv2.CAP_PROP_BRIGHTNESS))}")
        print(f"  Contrast: {int(self.cap.get(cv2.CAP_PROP_CONTRAST))}")
        print(f"  Exposure: {int(self.cap.get(cv2.CAP_PROP_EXPOSURE))}")
    
    def _warm_up(self):
        """Warm up camera and discard initial frames"""
        time.sleep(0.5)
        for _ in range(10):
            self.cap.read()
        print("✓ Camera ready\n")
    
    def capture_frame(self):
        """
        Capture a single high-quality frame
        
        Returns:
            Tuple (success, frame)
        """
        ret, frame = self.cap.read()
        
        if ret and frame is not None:
            # Apply additional processing for better quality
            frame = self._enhance_frame(frame)
        
        return ret, frame
    
    def _enhance_frame(self, frame):
        """
        Enhance frame quality with post-processing
        
        Args:
            frame: Input frame
        
        Returns:
            Enhanced frame
        """
        # Denoise
        frame = cv2.fastNlMeansDenoisingColored(frame, None, 10, 10, 7, 21)
        
        # Sharpen
        kernel = np.array([[-1,-1,-1],
                          [-1, 9,-1],
                          [-1,-1,-1]])
        frame = cv2.filter2D(frame, -1, kernel)
        
        return frame
    
    def calculate_sharpness(self, frame):
        """
        Calculate frame sharpness using Laplacian variance
        
        Args:
            frame: Input frame
        
        Returns:
            Sharpness score (higher = sharper)
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.Laplacian(gray, cv2.CV_64F).var()
    
    def capture_best_frame(self, num_samples=5):
        """
        Capture multiple frames and return the sharpest one
        
        Args:
            num_samples: Number of frames to compare
        
        Returns:
            Best quality frame
        """
        best_frame = None
        best_sharpness = 0
        
        for _ in range(num_samples):
            ret, frame = self.cap.read()
            if ret and frame is not None:
                sharpness = self.calculate_sharpness(frame)
                if sharpness > best_sharpness:
                    best_sharpness = sharpness
                    best_frame = frame.copy()
            time.sleep(0.1)  # Brief pause between captures
        
        if best_frame is not None:
            best_frame = self._enhance_frame(best_frame)
        
        return best_frame
    
    def capture_high_quality_image(self, save_path=None, show_preview=True):
        """
        Capture and save a high-quality image
        
        Args:
            save_path: Path to save image (optional)
            show_preview: Whether to show preview window
        
        Returns:
            Captured image
        """
        print("Capturing high-quality image...")
        
        # Capture best frame from multiple samples
        frame = self.capture_best_frame(num_samples=5)
        
        if frame is None:
            print("❌ Failed to capture image")
            return None
        
        # Calculate and display quality metrics
        sharpness = self.calculate_sharpness(frame)
        print(f"✓ Image captured - Sharpness: {sharpness:.2f}")
        
        # Save if path provided
        if save_path:
            cv2.imwrite(save_path, frame)
            print(f"✓ Saved to: {save_path}")
        
        # Show preview if requested
        if show_preview:
            cv2.imshow("High Quality Capture", frame)
            cv2.waitKey(2000)
            cv2.destroyAllWindows()
        
        return frame
    
    def capture_face_dataset(self, student_id, output_folder="data", num_images=100):
        """
        Capture high-quality face dataset for training
        
        Args:
            student_id: Student ID for naming files
            output_folder: Folder to save images
            num_images: Number of images to capture
        
        Returns:
            Number of images successfully captured
        """
        import os
        
        # Create output folder if needed
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        # Load face detector
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        
        captured_count = 0
        print(f"\nCapturing {num_images} high-quality face images...")
        print("Position your face and press 'c' to capture, 'q' to quit")
        
        while captured_count < num_images:
            ret, frame = self.capture_frame()
            
            if not ret:
                continue
            
            # Detect faces
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
            # Draw rectangles and info
            display_frame = frame.copy()
            for (x, y, w, h) in faces:
                cv2.rectangle(display_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(display_frame, f"Captured: {captured_count}/{num_images}", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            cv2.imshow("Face Capture - Press 'c' to capture", display_frame)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('c') and len(faces) > 0:
                # Capture face
                (x, y, w, h) = faces[0]
                face = frame[y:y+h, x:x+w]
                
                # Resize and save
                face_resized = cv2.resize(face, (450, 450))
                filename = f"{output_folder}/user.{student_id}.{captured_count + 1}.jpg"
                cv2.imwrite(filename, face_resized)
                
                captured_count += 1
                print(f"✓ Captured image {captured_count}/{num_images}")
                
                # Brief pause
                time.sleep(0.1)
            
            elif key == ord('q'):
                break
        
        cv2.destroyAllWindows()
        print(f"\n✓ Capture complete: {captured_count} images saved")
        return captured_count
    
    def release(self):
        """Release camera resources"""
        if self.cap:
            self.cap.release()
            cv2.destroyAllWindows()
            print("✓ Camera released")
    
    def __del__(self):
        """Cleanup on deletion"""
        self.release()


# Test function
if __name__ == "__main__":
    print("=" * 60)
    print("OPTIMIZED CAMERA QUALITY TEST")
    print("=" * 60)
    
    # Test quick fix
    print("\n1. Testing Quick Fix Function...")
    cap = fix_camera_quality(0)
    
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            cv2.imshow("Quick Fix - Press any key", frame)
            cv2.waitKey(3000)
            cv2.destroyAllWindows()
        cap.release()
    
    # Test optimized class
    print("\n2. Testing Optimized Camera Class...")
    camera = OptimizedCameraCapture(0, resolution=(1280, 720))
    
    # Capture high quality image
    image = camera.capture_high_quality_image("test_hq_capture.jpg", show_preview=True)
    
    if image is not None:
        print(f"\n✓ Image quality: {image.shape}")
        print(f"✓ Resolution: {image.shape[1]}x{image.shape[0]}")
    
    camera.release()
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)
