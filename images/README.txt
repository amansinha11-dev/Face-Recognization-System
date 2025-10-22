# IMAGES FOLDER - STUDENT PHOTOS

## How to Add Student Photos

### 1. Photo Requirements
- **Format:** JPG, PNG, or JPEG
- **Content:** One face per image
- **Quality:** Clear, front-facing photo
- **Lighting:** Good lighting (not too dark)
- **Size:** Any reasonable size (system will resize)

### 2. Naming Convention
Name each file with the student's name:

**Examples:**
```
JohnDoe.jpg
JaneSmith.png
MikeBrown.jpg
SarahJones.jpeg
RobertWilson.jpg
```

**Important:**
- No spaces in filename (use CamelCase or underscore)
- Extension: .jpg, .png, or .jpeg
- Name will appear in attendance records

### 3. Adding Photos

**Option A: Take Photos**
1. Use Windows Camera app
2. Take clear front-facing photo
3. Save to this folder with student name
4. Rename if needed

**Option B: Use Existing Photos**
1. Copy student ID photos
2. Paste into this folder
3. Rename to: StudentName.jpg

**Option C: Bulk Add**
1. Collect all student photos
2. Rename them properly
3. Copy all to this folder at once

### 4. Example Structure
```
images/
├── AliceJohnson.jpg
├── BobSmith.jpg
├── CarolWhite.jpg
├── DavidBrown.jpg
├── EmilyDavis.jpg
└── ... (add more)
```

### 5. After Adding Photos

Run the system:
```bash
python simple_face_recognition.py
```

System will:
1. Load all images from this folder
2. Detect faces automatically
3. Create face encodings
4. Save for future use
5. Start recognition

### 6. Tips for Best Results

✅ **DO:**
- Use recent photos
- Ensure face is clearly visible
- Use good lighting
- Face should be front-facing
- One person per image
- Use high-quality images

❌ **DON'T:**
- Use blurry photos
- Have multiple faces in one image
- Use photos with sunglasses
- Use very dark or backlit photos
- Use side-profile photos

### 7. Testing

Start with 2-3 test images to verify the system works before adding all students!

---

**Ready?** Add your first image and run: `python simple_face_recognition.py`
