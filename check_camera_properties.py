"""
Check what properties and codecs the camera supports
This helps us match what Windows Camera app is using
"""
import cv2

def fourcc_to_string(fourcc):
    """Convert FOURCC code to readable string"""
    return "".join([chr((int(fourcc) >> 8 * i) & 0xFF) for i in range(4)])

print("="*70)
print("CAMERA PROPERTIES INSPECTION")
print("="*70)

backends = [
    (cv2.CAP_MSMF, "Media Foundation (Windows Camera default)"),
    (cv2.CAP_DSHOW, "DirectShow"),
]

for backend_id, backend_name in backends:
    print(f"\n{'='*70}")
    print(f"Backend: {backend_name}")
    print("="*70)
    
    cap = cv2.VideoCapture(0, backend_id)
    
    if not cap.isOpened():
        print(f"✗ Cannot open with {backend_name}")
        continue
    
    print(f"✓ Opened successfully\n")
    
    # Get all properties
    properties = {
        'FRAME_WIDTH': cv2.CAP_PROP_FRAME_WIDTH,
        'FRAME_HEIGHT': cv2.CAP_PROP_FRAME_HEIGHT,
        'FPS': cv2.CAP_PROP_FPS,
        'FOURCC': cv2.CAP_PROP_FOURCC,
        'FORMAT': cv2.CAP_PROP_FORMAT,
        'MODE': cv2.CAP_PROP_MODE,
        'BRIGHTNESS': cv2.CAP_PROP_BRIGHTNESS,
        'CONTRAST': cv2.CAP_PROP_CONTRAST,
        'SATURATION': cv2.CAP_PROP_SATURATION,
        'HUE': cv2.CAP_PROP_HUE,
        'GAIN': cv2.CAP_PROP_GAIN,
        'EXPOSURE': cv2.CAP_PROP_EXPOSURE,
        'CONVERT_RGB': cv2.CAP_PROP_CONVERT_RGB,
        'BUFFERSIZE': cv2.CAP_PROP_BUFFERSIZE,
    }
    
    print("Current Properties:")
    print("-" * 70)
    for name, prop_id in properties.items():
        value = cap.get(prop_id)
        if name == 'FOURCC' and value != 0:
            codec = fourcc_to_string(value)
            print(f"  {name:20s}: {value:10.0f} ({codec})")
        else:
            print(f"  {name:20s}: {value:10.2f}")
    
    # Test different codecs
    print(f"\n{'-'*70}")
    print("Testing Common Codecs:")
    print("-" * 70)
    
    codecs_to_test = [
        ('MJPG', 'Motion JPEG'),
        ('YUYV', 'YUYV 4:2:2'),
        ('YUY2', 'YUY2'),
        ('RGB3', 'RGB 24-bit'),
        ('I420', 'I420'),
        ('NV12', 'NV12'),
    ]
    
    for codec_str, codec_desc in codecs_to_test:
        test_cap = cv2.VideoCapture(0, backend_id)
        test_cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*codec_str))
        test_cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        test_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Warm up
        for _ in range(10):
            test_cap.read()
        
        ret, frame = test_cap.read()
        
        if ret and frame is not None and frame.size > 0:
            mean = frame.mean()
            status = "✓ WORKS" if mean > 5 else "✗ BLACK"
            actual_fourcc = test_cap.get(cv2.CAP_PROP_FOURCC)
            actual_codec = fourcc_to_string(actual_fourcc)
            print(f"  {codec_str} ({codec_desc:20s}): {status:10s} | Mean: {mean:6.2f} | Actual: {actual_codec}")
        else:
            print(f"  {codec_str} ({codec_desc:20s}): ✗ FAILED")
        
        test_cap.release()
    
    cap.release()

print("\n" + "="*70)
print("INSPECTION COMPLETE!")
print("="*70)
print("\nRECOMMENDATION:")
print("Windows Camera app typically uses Media Foundation (MSMF) backend")
print("with whatever codec the camera driver provides by default.")
print("The codec marked as 'WORKS' with highest mean brightness is best.")
print("="*70)
