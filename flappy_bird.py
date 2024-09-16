import pygame
import sys
import random

# Constants
WIDTH, HEIGHT = 400, 600
BIRD_WIDTH, BIRD_HEIGHT = 40, 30
GRAVITY = 0.4
JUMP_FORCE = -8
PIPE_WIDTH = 70
PIPE_HEIGHT = 500
PIPE_GAP = 200
PIPE_SPEED = 4

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)


def draw_bird(screen, bird_image, bird_x, bird_y):
    screen.blit(bird_image, (bird_x, bird_y))


def draw_pipe(screen, pipe_x, pipe_height):
    pygame.draw.rect(screen, GREEN, (pipe_x, 0, PIPE_WIDTH, pipe_height))
    pygame.draw.rect(screen, GREEN, (pipe_x, pipe_height + PIPE_GAP, PIPE_WIDTH, HEIGHT - pipe_height - PIPE_GAP))


def check_collision(bird_x, bird_y, pipe_x, pipe_height):
    if bird_x + BIRD_WIDTH > pipe_x and bird_x < pipe_x + PIPE_WIDTH:
        if bird_y < pipe_height or bird_y + BIRD_HEIGHT > pipe_height + PIPE_GAP:
            return True


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()

    bird_image = pygame.image.load("bird.png").convert_alpha()
    bird_x, bird_y = 50, HEIGHT // 2
    bird_dy = 0

    pipes = []
    score = 0
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird_dy = JUMP_FORCE

        bird_dy += GRAVITY
        bird_y += bird_dy

        # Generate pipes
        if pipes and pipes[-1][0] < WIDTH - WIDTH // 2:
            pipe_height = random.randint(50, HEIGHT - PIPE_GAP - 50)
            pipes.append((WIDTH, pipe_height))
        elif not pipes:
            pipe_height = random.randint(50, HEIGHT - PIPE_GAP - 50)
            pipes.append((WIDTH, pipe_height))

        # Move pipes
        pipes = [(pipe_x - PIPE_SPEED, pipe_height) for pipe_x, pipe_height in pipes]

        # Remove off-screen pipes
        pipes = [(pipe_x, pipe_height) for pipe_x, pipe_height in pipes if pipe_x > -PIPE_WIDTH]

        # Check for collisions
        for pipe_x, pipe_height in pipes:
            if check_collision(bird_x, bird_y, pipe_x, pipe_height):
                game_over = True

        # Check for score
        if pipes and pipes[0][0] + PIPE_WIDTH < bird_x:
            score += 1
            pipes.pop(0)

        # Draw everything
        screen.fill(WHITE)
        draw_bird(screen, bird_image, bird_x, bird_y)
        for pipe_x, pipe_height in pipes:
            draw_pipe(screen, pipe_x, pipe_height)

        pygame.display.set_caption(f"Flappy Bird - Score: {score}")

        pygame.display.update()
        clock.tick(60)

    print(f"Final Score: {score}")  # Print final score after the game loop ends


if __name__ == "__main__":
    main()
