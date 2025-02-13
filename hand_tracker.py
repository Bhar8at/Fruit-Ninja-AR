import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.trail_points = []
        self.max_trail_length = 8

    def process_frame(self, image):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return self.hands.process(image_rgb)

    def draw_landmarks(self, image, hand_landmarks):
        self.mp_draw.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

    def update_trail(self, point):
        self.trail_points.append(point)
        if len(self.trail_points) > self.max_trail_length:
            self.trail_points.pop(0)

    def draw_trail(self, image):
        for i in range(1, len(self.trail_points)):
            cv2.line(image, self.trail_points[i-1], self.trail_points[i],
                    (255, 255, 255), thickness=max(1, int(i)), lineType=cv2.LINE_AA)

    def clear_trail(self):
        self.trail_points.clear() 