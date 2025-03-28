import cv2
import mediapipe as mp
import time
import json
import tkinter as tk
from tkinter import messagebox
import threading

"""
class EyeMovementAnalyzer:
    @staticmethod
    def calculate_eye_direction(face_landmarks):
        left_eye_x = (face_landmarks.landmark[33].x + face_landmarks.landmark[133].x) / 2
        right_eye_x = (face_landmarks.landmark[362].x + face_landmarks.landmark[263].x) / 2
        nose_x = face_landmarks.landmark[168].x

        if left_eye_x < nose_x and right_eye_x < nose_x:
            return "left"
        elif left_eye_x > nose_x and right_eye_x > nose_x:
            return "right"
        else:
            return "center"

    @staticmethod
    def detect_suspicious_movements(eye_data):
        suspicious_movements = 0
        for i in range(1, len(eye_data)):
            if eye_data[i]['eye_direction'] in ['left', 'right']:
                suspicious_movements += 1

        return suspicious_movements > 5  # אם היו יותר מ-5 מבטים חשודים, יש חשד להעתקה
"""


class EyeMovementAnalyzer:
    @staticmethod
    def calculate_eye_direction(face_landmarks):
        left_eye_x = (face_landmarks.landmark[33].x + face_landmarks.landmark[133].x) / 2
        right_eye_x = (face_landmarks.landmark[362].x + face_landmarks.landmark[263].x) / 2
        nose_x = face_landmarks.landmark[168].x

        if left_eye_x < nose_x and right_eye_x < nose_x:
            return "left"
        elif left_eye_x > nose_x and right_eye_x > nose_x:
            return "right"
        else:
            return "center"

    @staticmethod
    def detect_suspicious_movements(eye_data):
        suspicious_movements = 0
        previous_direction = None
        previous_time = None

        for data in eye_data:
            # אם יש שינוי פתאומי בתנועה
            if previous_direction is not None and previous_time is not None:
                time_diff = data['time'] - previous_time
                if time_diff < 1 and data['eye_direction'] != previous_direction:  # תנועה תוך שניה שהשתנתה
                    suspicious_movements += 1

            previous_direction = data['eye_direction']
            previous_time = data['time']

        # אם יש יותר מ-5 תנועות חשודות, חשד להעתקה
        return suspicious_movements > 5
"""branch1"""

class EyeMovementTracking:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(refine_landmarks=True)
        self.mp_drawing = mp.solutions.drawing_utils
        self.eye_data = []  # לשמירת תנועות עיניים זמניות
        self.start_time = time.time()
        self.cap = None  # משתנה לשמירת המצלמה
        self.is_running = False

    def open_camera(self):
        self.cap = cv2.VideoCapture(0)
        self.is_running = True
        while self.cap.isOpened() and self.is_running:
            ret, frame = self.cap.read()
            if not ret:
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(rgb_frame)

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    self.mp_drawing.draw_landmarks(frame, face_landmarks, self.mp_face_mesh.FACEMESH_CONTOURS)
                    eye_direction = EyeMovementAnalyzer.calculate_eye_direction(face_landmarks)
                    self.log_movements(eye_direction)

            cv2.imshow('Eye Tracking', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def stop_camera(self):
        self.is_running = False

    def log_movements(self, eye_direction):
        timestamp = time.time() - self.start_time
        self.eye_data.append({'time': timestamp, 'eye_direction': eye_direction})

    def save_to_db(self):
        with open("eye_movements.json", "w") as file:
            json.dump(self.eye_data, file, indent=4)

    def analyze_cheating_risks(self):
        return EyeMovementAnalyzer.detect_suspicious_movements(self.eye_data)


# יצירת ממשק גרפי עם Tkinter
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("מעקב תנועות עיניים")

        # יצירת כפתור "התחלת מבחן"
        self.start_button = tk.Button(self.root, text="התחל מבחן", command=self.start_exam)
        self.start_button.pack(pady=10)

        # יצירת כפתור "סיים מבחן"
        self.end_button = tk.Button(self.root, text="סיים מבחן", command=self.end_exam, state=tk.DISABLED)
        self.end_button.pack(pady=10)

        # אובייקט המעקב
        self.tracker = None

    def start_exam(self):
        self.tracker = EyeMovementTracking()
        self.start_button.config(state=tk.DISABLED)
        self.end_button.config(state=tk.NORMAL)

        # הפעלת המצלמה והמבחן באשכול נפרד
        threading.Thread(target=self.tracker.open_camera, daemon=True).start()

    def end_exam(self):
        if self.tracker:
            self.tracker.stop_camera()  # עצירת המצלמה
            self.tracker.save_to_db()
            is_cheating = self.tracker.analyze_cheating_risks()
            result_message = "חשד להעתקה: " + ("כן" if is_cheating else "לא")
            messagebox.showinfo("סיום מבחן", result_message)

        # סיום המבחן
        self.root.quit()


# יצירת חלון Tkinter
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
