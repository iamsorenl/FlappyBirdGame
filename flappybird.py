import asyncio
import random

import pygame

WIDTH, HEIGHT = 400, 600
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

BIRD_X = 50
BIRD_W, BIRD_H = 40, 40
GRAVITY = 0.25
FLAP = -5

PIPE_W = 70
GAP = 200
PIPE_FREQ_MS = 1500
PIPE_SPEED = 5


def initial_state():
    return {
        "bird_y": HEIGHT // 2,
        "bird_movement": 0,
        "pipes": [],
        "last_pipe": pygame.time.get_ticks(),
        "game_over": False,
    }


async def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 32)

    state = initial_state()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if state["game_over"]:
                    state = initial_state()
                else:
                    state["bird_movement"] = FLAP
            if event.type == pygame.MOUSEBUTTONDOWN:
                if state["game_over"]:
                    state = initial_state()
                else:
                    state["bird_movement"] = FLAP

        if not state["game_over"]:
            state["bird_movement"] += GRAVITY
            state["bird_y"] += state["bird_movement"]

            now = pygame.time.get_ticks()
            if now - state["last_pipe"] > PIPE_FREQ_MS:
                pipe_height = random.randint(100, 400)
                state["pipes"].append(
                    pygame.Rect(WIDTH, HEIGHT - pipe_height, PIPE_W, pipe_height)
                )
                state["pipes"].append(
                    pygame.Rect(WIDTH, 0, PIPE_W, HEIGHT - pipe_height - GAP)
                )
                state["last_pipe"] = now

            for pipe in state["pipes"]:
                pipe.x -= PIPE_SPEED
            state["pipes"] = [p for p in state["pipes"] if p.right >= 0]

            bird_rect = pygame.Rect(BIRD_X, state["bird_y"], BIRD_W, BIRD_H)
            if any(bird_rect.colliderect(p) for p in state["pipes"]):
                state["game_over"] = True
            if state["bird_y"] > HEIGHT or state["bird_y"] < 0:
                state["game_over"] = True

        screen.fill(WHITE)
        pygame.draw.rect(screen, RED, pygame.Rect(BIRD_X, state["bird_y"], BIRD_W, BIRD_H))
        for pipe in state["pipes"]:
            pygame.draw.rect(screen, GREEN, pipe)

        if state["game_over"]:
            msg = font.render("Game Over — press SPACE to restart", True, BLACK)
            screen.blit(msg, msg.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        else:
            hint = font.render("SPACE / click to flap", True, BLACK)
            screen.blit(hint, (10, 10))

        pygame.display.update()
        clock.tick(30)
        await asyncio.sleep(0)


asyncio.run(main())
