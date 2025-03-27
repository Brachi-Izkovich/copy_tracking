"""import cv2
import mediapipe as mp
import time
from eye_movement_analyzer import EyeMovementAnalyzer

class EyeMovementTracking:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(refine_landmarks=True)
        self.mp_drawing = mp.solutions.drawing_utils
        self.eye_data = []  # לשמירת תנועות עיניים זמניות
        self.start_time = time.time()

    def open_camera(self):
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            ret, frame = cap.read()
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

        cap.release()
        cv2.destroyAllWindows()

    def log_movements(self, eye_direction):
        timestamp = time.time() - self.start_time
        self.eye_data.append({'time': timestamp, 'eye_direction': eye_direction})

    def save_to_db(self):
        with open("eye_movements.json", "w") as file:
            json.dump(self.eye_data, file, indent=4)

    def analyze_cheating_risks(self):
        return EyeMovementAnalyzer.detect_suspicious_movements(self.eye_data)
"""