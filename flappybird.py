import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Bird properties
bird_x, bird_y = 50, HEIGHT // 2
bird_width, bird_height = 40, 40
bird_movement = 0
gravity = 0.25

# Pipe properties
pipe_width = 70
gap_size = 200
pipe_frequency = 1500  # milliseconds
last_pipe = pygame.time.get_ticks()

pipes = []

# Game loop
running = True
while running:
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = -5

    # Bird physics
    bird_movement += gravity
    bird_y += bird_movement

    # Pipe mechanics
    time_now = pygame.time.get_ticks()
    if time_now - last_pipe > pipe_frequency:
        pipe_height = random.randint(100, 400)
        bottom_pipe = pygame.Rect(WIDTH, HEIGHT - pipe_height, pipe_width, pipe_height)
        top_pipe = pygame.Rect(WIDTH, 0, pipe_width, HEIGHT - pipe_height - gap_size)
        pipes.append(bottom_pipe)
        pipes.append(top_pipe)
        last_pipe = time_now

    for pipe in pipes:
        pipe.x -= 5
        if pipe.right < 0:
            pipes.remove(pipe)

    # Collision detection
    bird_rect = pygame.Rect(bird_x, bird_y, bird_width, bird_height)
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            running = False

    if bird_y > HEIGHT or bird_y < 0:
        running = False

    # Drawing
    screen.fill(WHITE)
    pygame.draw.rect(screen, (255, 0, 0), bird_rect)
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, pipe)

    pygame.display.update()

    # Frame rate
    pygame.time.Clock().tick(30)

pygame.quit()
