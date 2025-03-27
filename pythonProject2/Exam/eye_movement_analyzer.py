"""import json


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