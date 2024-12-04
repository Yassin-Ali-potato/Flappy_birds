import pygame
import random
import time
import os

pygame.init()

# Constants
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600
GRAVITY = 0.25
JUMP_SPEED = -5
PIPE_SPEED = 3
PIPE_GAP = 150
PIPE_FREQUENCY = 1500

# Colors
SKY_BLUE = (137, 207, 240)
GREEN = (76, 187, 23)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()

class Bird:
    def __init__(self):
        self.x = WINDOW_WIDTH // 3
        self.y = WINDOW_HEIGHT // 2
        self.velocity = 0
        self.size = 30
        
        # Load bird image
        self.image = pygame.image.load(r"C:\Users\youseef\Myproject\bird.png")  # Make sure to have bird.png in same directory
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        
    def jump(self):
        self.velocity = JUMP_SPEED
        
    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        
    def draw(self):
        # Rotate bird based on velocity
        angle = -self.velocity * 2
        rotated_bird = pygame.transform.rotate(self.image, angle)
        screen.blit(rotated_bird, (self.x, self.y))

class Pipe:
    def __init__(self):
        self.gap_y = random.randint(200, WINDOW_HEIGHT - 200)
        self.x = WINDOW_WIDTH
        self.width = 50
        self.scored = False
        
    def update(self):
        self.x -= PIPE_SPEED
        
    def draw(self):
        pygame.draw.rect(screen, GREEN, 
                        (self.x, 0, self.width, self.gap_y - PIPE_GAP//2))
        pygame.draw.rect(screen, GREEN, 
                        (self.x, self.gap_y + PIPE_GAP//2, 
                         self.width, WINDOW_HEIGHT))

    def check_collision(self, bird):
        bird_rect = pygame.Rect(bird.x, bird.y, bird.size, bird.size)
        top_pipe = pygame.Rect(self.x, 0, 
                             self.width, self.gap_y - PIPE_GAP//2)
        bottom_pipe = pygame.Rect(self.x, self.gap_y + PIPE_GAP//2,
                                self.width, WINDOW_HEIGHT)
        return bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe)

def countdown():
    font = pygame.font.Font(None, 74)
    for i in range(3, 0, -1):
        screen.fill(SKY_BLUE)
        count_text = font.render(str(i), True, (255, 255, 255))
        screen.blit(count_text, (WINDOW_WIDTH//2 - 20, WINDOW_HEIGHT//2 - 50))
        pygame.display.flip()
        time.sleep(1)

def game_over_screen(score):
    font = pygame.font.Font(None, 48)
    running = True
    while running:
        screen.fill(SKY_BLUE)
        
        game_over_text = font.render("Game Over!", True, RED)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        restart_text = font.render("Press SPACE to restart", True, (255, 255, 255))
        
        screen.blit(game_over_text, (WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 - 50))
        screen.blit(score_text, (WINDOW_WIDTH//2 - 70, WINDOW_HEIGHT//2))
        screen.blit(restart_text, (WINDOW_WIDTH//2 - 150, WINDOW_HEIGHT//2 + 50))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True

def main():
    # Check if bird image exists
    if not os.path.exists('bird.png'):
        print("Error: bird.png not found! Please add a bird image to the same directory.")
        return

    while True:
        bird = Bird()
        pipes = []
        score = 0
        last_pipe = pygame.time.get_ticks()
        font = pygame.font.Font(None, 36)
        
        countdown()
        
        running = True
        while running:
            current_time = pygame.time.get_ticks()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bird.jump()
            
            if current_time - last_pipe > PIPE_FREQUENCY:
                pipes.append(Pipe())
                last_pipe = current_time
            
            bird.update()
            for pipe in pipes:
                pipe.update()
                if not pipe.scored and pipe.x < bird.x:
                    score += 1
                    pipe.scored = True
            
            pipes = [pipe for pipe in pipes if pipe.x > -pipe.width]
            
            for pipe in pipes:
                if pipe.check_collision(bird):
                    running = False
            
            if bird.y < 0 or bird.y > WINDOW_HEIGHT:
                running = False
                
            screen.fill(SKY_BLUE)
            bird.draw()
            for pipe in pipes:
                pipe.draw()
                
            score_text = font.render(str(score), True, (255, 255, 255))
            screen.blit(score_text, (WINDOW_WIDTH//2, 50))
            
            pygame.display.flip()
            clock.tick(60)
        
        if not game_over_screen(score):
            break

    pygame.quit()

if __name__ == "__main__":
    main()