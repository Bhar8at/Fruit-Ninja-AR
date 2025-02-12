import cv2
import mediapipe as mp
import numpy as np
import random

# Initialize MediaPipe Hand tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# Initialize fruits

class Fruit:
    def __init__(self, x):
        self.x = x
        self.y = 0
        self.speed = random.uniform(5, 15)
        self.size = 30



fruits = []
spawn_timer = 0
spawn_interval = 30

# Initialize webcam
cap = cv2.VideoCapture(0)

while True:
    success, image = cap.read()
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Spawn fruits
    spawn_timer += 1
    if spawn_timer >= spawn_interval:
        new_fruit_x = random.randint(0, image.shape[1])
        fruits.append(Fruit(new_fruit_x))
        spawn_timer = 0

    # Update and draw fruits
    for fruit in fruits[:]:
        fruit.y += fruit.speed
        cv2.circle(image, (int(fruit.x), int(fruit.y)), fruit.size, (0, 255, 0), -1)
        
        # Remove fruits that fall off screen
        if fruit.y > image.shape[0]:
            fruits.remove(fruit)

    # Detect hands
    results = hands.process(image_rgb)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw hand landmarks
            mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Get coordinates of hand points
            for id, lm in enumerate(hand_landmarks.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # You can use these coordinates for collision detection later
                
                # Check collision with fruits (using index finger tip - point 8)
                if id == 8:  # Index fingertip
                    for fruit in fruits[:]:  # Create a copy of the list to safely remove items
                        # Simple collision detection
                        distance = np.sqrt((cx - fruit.x)**2 + (cy - fruit.y)**2)
                        if distance < fruit.size:
                            fruits.remove(fruit)
                            # You could add score here

    # Mirror the image before display
    image = cv2.flip(image, 1)
    cv2.imshow("Hand Tracking", image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.waitKey(0)
cv2.destroyAllWindows() 