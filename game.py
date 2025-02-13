import cv2
import numpy as np
from fruit import Fruit
from hand_tracker import HandTracker
import time

class FruitSlicingGame:
    def __init__(self):
        # Game state
        self.score = 0
        self.fruits = []
        
        # Spawn control
        self.spawn_timer = 0
        self.spawn_interval = 30
        
        # Speed control
        self.speed_multiplier = 1.0
        self.speed_increase_interval = 5  # seconds
        self.last_speed_increase = time.time()
        
        # Initialize devices
        self.cap = cv2.VideoCapture(0)
        self.hand_tracker = HandTracker()

    def update_speed(self):
        """Increase speed multiplier every 5 seconds"""
        current_time = time.time()
        if current_time - self.last_speed_increase >= self.speed_increase_interval:
            self.speed_multiplier += 0.2
            self.last_speed_increase = current_time

    def spawn_fruit(self, screen_width):
        """Spawn a new fruit at random x position"""
        if self.spawn_timer >= self.spawn_interval:
            new_fruit_x = np.random.randint(0, screen_width)
            self.fruits.append(Fruit(new_fruit_x, self.speed_multiplier))
            self.spawn_timer = 0

    def update_fruits(self, image):
        """Update and draw all fruits"""
        for fruit in self.fruits[:]:
            fruit.update()
            should_remove = fruit.draw(image)
            
            if should_remove or fruit.y > image.shape[0]:
                self.fruits.remove(fruit)

    def check_collision(self, point, fruits):
        """Check for collisions between point and fruits"""
        cx, cy = point
        for fruit in fruits[:]:
            if not fruit.is_exploding:
                distance = np.sqrt((cx - fruit.x)**2 + (cy - fruit.y)**2)
                if distance < fruit.size/2:
                    fruit.explode()
                    self.score += 1

    def draw_score(self, image):
        """Draw score box in bottom right corner"""
        score_text = f'Score: {self.score}'
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        thickness = 2
        color = (255, 255, 255)
        
        # Calculate position
        (text_width, text_height), _ = cv2.getTextSize(score_text, font, font_scale, thickness)
        padding = 20
        x = image.shape[1] - text_width - padding
        y = image.shape[0] - padding
        
        # Draw background
        cv2.rectangle(image, 
                     (x - 10, y - text_height - 10),
                     (x + text_width + 10, y + 10),
                     (0, 0, 0), -1)
        
        # Draw text
        cv2.putText(image, score_text, (x, y), 
                    font, font_scale, color, thickness)

    def process_hand_tracking(self, image, results):
        """Process hand tracking results"""
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.hand_tracker.draw_landmarks(image, hand_landmarks)
                
                for id, lm in enumerate(hand_landmarks.landmark):
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    
                    if id == 8:  # Index fingertip
                        self.hand_tracker.update_trail((cx, cy))
                        self.hand_tracker.draw_trail(image)
                        self.check_collision((cx, cy), self.fruits)
        else:
            self.hand_tracker.clear_trail()

    def run(self):
        """Main game loop"""
        while True:
            # Capture frame
            success, image = self.cap.read()
            if not success:
                break

            # Update game state
            self.update_speed()
            self.spawn_timer += 1
            self.spawn_fruit(image.shape[1])
            self.update_fruits(image)

            # Process hand tracking
            results = self.hand_tracker.process_frame(image)
            self.process_hand_tracking(image, results)

            # Draw final frame
            image = cv2.flip(image, 1)
            self.draw_score(image)
            cv2.imshow("Fruit Ninja", image)
            
            # Check for quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Cleanup
        self.cap.release()
        cv2.waitKey(0)
        cv2.destroyAllWindows() 