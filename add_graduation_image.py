"""
Add Graduation Banner Image to Student Details
Instructions for adding your graduation/university image
"""
import os
from PIL import Image

def add_graduation_image():
    """
    Instructions to add your graduation/university banner image
    """
    print("=" * 60)
    print("ADDING GRADUATION BANNER TO STUDENT DETAILS")
    print("=" * 60)
    
    images_folder = "images"
    target_file = os.path.join(images_folder, "graduation_banner.jpg")
    
    print("\n📋 INSTRUCTIONS:")
    print("-" * 60)
    print("1. Save your graduation image (the green one with students)")
    print("   to this location:")
    print(f"   {os.path.abspath(target_file)}")
    print()
    print("2. The image should be:")
    print("   - Name: graduation_banner.jpg")
    print("   - Format: JPG or PNG")
    print("   - Recommended size: 1530x130 pixels (will be auto-resized)")
    print()
    print("3. After saving the image, run:")
    print("   python main.py")
    print()
    print("4. Click 'Student Details' button to see the banner!")
    print("-" * 60)
    
    # Check if image exists
    if os.path.exists(target_file):
        print("\n✅ SUCCESS! Graduation banner found:")
        try:
            img = Image.open(target_file)
            print(f"   Image size: {img.size[0]}x{img.size[1]}")
            print(f"   Format: {img.format}")
            print(f"   Mode: {img.mode}")
            print("\n✓ Your graduation banner is ready!")
            print("✓ Run 'python main.py' and click 'Student Details'")
        except Exception as e:
            print(f"\n⚠ Warning: Could not read image: {e}")
    else:
        print("\n⏳ WAITING FOR IMAGE...")
        print(f"   Please save your graduation image to:")
        print(f"   {os.path.abspath(target_file)}")
        print()
        print("📂 Current 'images' folder contents:")
        if os.path.exists(images_folder):
            files = os.listdir(images_folder)
            if files:
                for f in files:
                    print(f"   - {f}")
            else:
                print("   (empty)")
        else:
            print("   (folder not found)")
    
    print("\n" + "=" * 60)
    
    # Create a sample placeholder if no image exists
    if not os.path.exists(target_file):
        print("\n💡 TIP: Would you like to create a sample banner?")
        print("   The system will use a green placeholder until you add your image.")
        print("   Your image will automatically replace it when added.")
        print()
        
        # Create sample
        try:
            sample = Image.new('RGB', (1530, 130), color='#1a5f1a')
            from PIL import ImageDraw, ImageFont
            draw = ImageDraw.Draw(sample)
            # Draw decorative elements
            draw.rectangle([(0, 100), (1530, 130)], fill='#2e8b2e')
            draw.rectangle([(10, 10), (1510, 120)], outline='#ffffff', width=3)
            
            # Add text
            try:
                # Try to add text (may fail if font not available)
                draw.text((765, 55), "STUDENT MANAGEMENT SYSTEM", 
                         fill='white', anchor='mm')
            except:
                pass
            
            sample_path = os.path.join(images_folder, "sample_banner.jpg")
            sample.save(sample_path)
            print(f"✓ Sample banner created: {sample_path}")
            print("  (This is just a placeholder)")
        except Exception as e:
            print(f"Could not create sample: {e}")

if __name__ == "__main__":
    add_graduation_image()
