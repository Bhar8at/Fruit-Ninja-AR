import random
import cv2
import numpy as np

class Fruit:
    def __init__(self, x, speed_multiplier=1.0):
        self.x = x
        self.y = 0
        self.speed = random.uniform(5, 15) * speed_multiplier
        self.size = 120
        self.is_exploding = False
        self.particles = []
        self.particle_lifetime = 20
        self.current_lifetime = 0
        
        # Load image once during initialization
        self.image = cv2.imread('apple.png', cv2.IMREAD_UNCHANGED)
        if self.image is not None:
            self.image = cv2.resize(self.image, (self.size, self.size))

    def update(self):
        if not self.is_exploding:
            self.y += self.speed
        else:
            # Update explosion particles
            for particle in self.particles:
                particle[0] += particle[2]  # x position
                particle[1] += particle[3]  # y position
                particle[3] += 0.5  # gravity
            self.current_lifetime += 1

    def draw(self, background):
        if self.is_exploding:
            # Draw explosion particles
            for particle in self.particles:
                cv2.circle(background, (int(particle[0]), int(particle[1])), 
                          8, (0, 0, 255), -1)
            return self.current_lifetime > self.particle_lifetime
        else:
            # Draw the fruit normally
            y1 = int(self.y - self.size/2)
            x1 = int(self.x - self.size/2)
            cv2.circle(background, (int(self.x), int(self.y)), 
                      self.size//2, (0, 0, 255), -1)  # Red circle
            cv2.circle(background, (int(self.x), int(self.y - self.size/3)), 
                      self.size//6, (0, 100, 0), -1)  # Green stem
            return False

    def explode(self):
        self.is_exploding = True
        # Create more particles with larger size
        num_particles = 30
        for _ in range(num_particles):
            angle = random.uniform(0, 2 * np.pi)
            speed = random.uniform(8, 20)
            # [x, y, dx, dy]
            self.particles.append([
                self.x,
                self.y,
                speed * np.cos(angle),
                speed * np.sin(angle)
            ])