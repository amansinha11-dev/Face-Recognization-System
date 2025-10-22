"""
Process Attendance From Video File/Stream using DeepFace (FaceNet)
- Loads known faces from images/StudentName/* or student_images/*
- Optionally loads cached encodings if available
- Reads frames from a video file, YouTube/RTSP URL, or webcam index
- Marks attendance into attendance_records/attendance_YYYY-MM-DD.csv

Usage examples (PowerShell):
  python process_video_attendance.py --video path/to/video.mp4
  python process_video_attendance.py --video 0            # webcam index
  python process_video_attendance.py --video "rtsp://..." # network stream
  python process_video_attendance.py --images images      # change known faces folder

Requirements: deepface, opencv-python, numpy
"""
import os
import sys
import csv
import time
import argparse
from datetime import datetime, date

import cv2
import numpy as np
from deepface import DeepFace

KNOWN_FOLDERS = [
    "images",          # default repo folder (organized as images/Name/xxx.jpg)
    "student_images",  # GUI-captured faces folder
]

ATTENDANCE_DIR = "attendance_records"

def ensure_dirs():
    if not os.path.exists(ATTENDANCE_DIR):
        os.makedirs(ATTENDANCE_DIR, exist_ok=True)

class Encoder:
    def __init__(self, images_folder: str):
        self.images_folder = images_folder
        self.known_names: list[str] = []
        self.known_encodings: list[np.ndarray] = []

    def _load_from_folder(self) -> bool:
        if not os.path.exists(self.images_folder):
            return False
        for entry in os.listdir(self.images_folder):
            person_dir = os.path.join(self.images_folder, entry)
            if not os.path.isdir(person_dir):
                # also allow single-file naming like ID_Name.jpg inside folder
                if entry.lower().endswith((".jpg", ".jpeg", ".png")):
                    person_name = os.path.splitext(entry)[0]
                    img_path = person_dir
                    try:
                        emb = DeepFace.represent(img_path=img_path, model_name="Facenet", enforce_detection=False)
                        if emb:
                            self.known_names.append(person_name)
                            self.known_encodings.append(np.array(emb[0]["embedding"]))
                    except Exception:
                        pass
                continue
            person_name = entry
            for img_name in os.listdir(person_dir):
                if not img_name.lower().endswith((".jpg", ".jpeg", ".png")):
                    continue
                img_path = os.path.join(person_dir, img_name)
                try:
                    emb = DeepFace.represent(img_path=img_path, model_name="Facenet", enforce_detection=False)
                    if emb:
                        self.known_names.append(person_name)
                        self.known_encodings.append(np.array(emb[0]["embedding"]))
                except Exception:
                    pass
        return len(self.known_names) > 0

    def load(self) -> bool:
        return self._load_from_folder()

class AttendanceWriter:
    def __init__(self):
        ensure_dirs()
        self.today = date.today().strftime("%Y-%m-%d")
        self.path = os.path.join(ATTENDANCE_DIR, f"attendance_{self.today}.csv")
        self._ensure_header()
        self._marked = set(self._load_existing_names())

    def _ensure_header(self):
        if not os.path.exists(self.path):
            with open(self.path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Name", "Date", "Time", "Status"])  # keep simple for CLI tool

    def _load_existing_names(self):
        names = []
        try:
            with open(self.path, "r", newline="") as f:
                r = csv.reader(f)
                next(r, None)
                for row in r:
                    if row:
                        names.append(row[0])
        except Exception:
            pass
        return names

    def mark(self, name: str):
        if name in self._marked:
            return False
        with open(self.path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([name, self.today, datetime.now().strftime("%H:%M:%S"), "Present"])
        self._marked.add(name)
        return True


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return -1.0
    return float(np.dot(a, b) / denom)


def recognize_from_stream(src, encoder: Encoder, threshold: float = 0.5, process_every_n: int = 15):
    cap: cv2.VideoCapture
    if isinstance(src, int):
        cap = cv2.VideoCapture(src, cv2.CAP_DSHOW)
    else:
        cap = cv2.VideoCapture(src)

    if not cap.isOpened():
        print("Error: cannot open video source")
        return

    writer = AttendanceWriter()
    print(f"Attendance target: {writer.path}")

    frame_idx = 0
    marked_today = set()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("End of stream or read error.")
            break

        frame_idx += 1
        if frame_idx % process_every_n != 0:
            cv2.imshow("Video Attendance", frame)
        else:
            # Save temp and get embedding for the whole frame faces
            tmp = "_tmp_video_frame.jpg"
            cv2.imwrite(tmp, frame)
            try:
                faces = DeepFace.extract_faces(img_path=tmp, enforce_detection=False, detector_backend='opencv')
            except Exception:
                faces = []

            for face in faces:
                fa = face.get('facial_area') or {}
                x, y, w, h = fa.get('x', 0), fa.get('y', 0), fa.get('w', 0), fa.get('h', 0)
                x2, y2 = x + w, y + h
                color = (0, 0, 255)
                label = "Unknown"
                conf_pct = 0

                try:
                    emb_pack = DeepFace.represent(img_path=tmp, model_name="Facenet", enforce_detection=False, detector_backend='opencv')
                    if emb_pack:
                        det_emb = np.array(emb_pack[0]['embedding'])
                        best_sim = -1.0
                        best_name = "Unknown"
                        for known_emb, name in zip(encoder.known_encodings, encoder.known_names):
                            sim = cosine_similarity(det_emb, np.array(known_emb))
                            if sim > best_sim:
                                best_sim = sim
                                best_name = name
                        if best_sim >= threshold:
                            label = best_name
                            color = (0, 255, 0)
                            conf_pct = int(best_sim * 100)
                            if label not in marked_today and writer.mark(label):
                                marked_today.add(label)
                                print(f"✓ Marked: {label} @ {datetime.now().strftime('%H:%M:%S')} (sim {best_sim:.2f})")
                        else:
                            conf_pct = int(max(0.0, best_sim) * 100)
                except Exception:
                    pass

                # Draw box and label
                cv2.rectangle(frame, (x, y), (x2, y2), color, 2)
                cv2.rectangle(frame, (x, y - 20), (x2, y), color, -1)
                cv2.putText(frame, f"{label} ({conf_pct}%)", (x + 4, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

            cv2.imshow("Video Attendance", frame)
            try:
                os.remove(tmp)
            except Exception:
                pass

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Done. Recognized {len(marked_today)} unique people.")


def parse_args():
    p = argparse.ArgumentParser(description="Process attendance from a video/stream using DeepFace")
    p.add_argument("--video", required=True, help="Path/URL to video, or integer index for webcam (e.g., 0)")
    p.add_argument("--images", default=None, help="Folder with known faces; defaults to images or student_images")
    p.add_argument("--threshold", type=float, default=0.5, help="Cosine similarity threshold (0.0-1.0)")
    p.add_argument("--every", type=int, default=15, help="Process every Nth frame")
    return p.parse_args()


def main():
    args = parse_args()

    # Determine source type
    src = args.video
    if src.isdigit():
        src = int(src)

    # Pick known faces folder
    images_folder = args.images
    if not images_folder:
        for f in KNOWN_FOLDERS:
            if os.path.exists(f):
                images_folder = f
                break
    if not images_folder:
        images_folder = KNOWN_FOLDERS[0]

    print(f"Using known faces from: {images_folder}")

    encoder = Encoder(images_folder)
    if not encoder.load():
        print("No known faces found. Please add folders as images/Name/*.jpg or use the GUI to capture.")
        sys.exit(1)

    print(f"Loaded {len(encoder.known_names)} known people.")
    recognize_from_stream(src, encoder, threshold=args.threshold, process_every_n=args.every)


if __name__ == "__main__":
    main()
