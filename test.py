import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 8000, 6000

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aiming Game")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Cannon properties
cannon_x = WIDTH // 2
cannon_y = HEIGHT - 50
cannon_radius = 20

# Bullet properties
bullet_radius = 5
bullet_speed = 7
bullets = []

# Target properties
target_radius = 30
target_x = random.randint(target_radius, WIDTH - target_radius)
target_y = random.randint(target_radius, HEIGHT // 2)
target_speed = 3

# Score
score = 0

# Main game loop
running = True
while running:
    screen.fill(WHITE)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Fire a bullet towards the mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()
            angle = math.atan2(mouse_y - cannon_y, mouse_x - cannon_x)
            bullets.append({
                "x": cannon_x,
                "y": cannon_y,
                "dx": bullet_speed * math.cos(angle),
                "dy": bullet_speed * math.sin(angle)
            })

    # Update target position
    target_x += target_speed
    if target_x - target_radius < 0 or target_x + target_radius > WIDTH:
        target_speed = -target_speed

    # Draw target
    pygame.draw.circle(screen, RED, (target_x, target_y), target_radius)

    # Update and draw bullets
    for bullet in bullets[:]:
        bullet["x"] += bullet["dx"]
        bullet["y"] += bullet["dy"]

        # Remove bullet if it leaves the screen
        if bullet["x"] < 0 or bullet["x"] > WIDTH or bullet["y"] < 0 or bullet["y"] > HEIGHT:
            bullets.remove(bullet)

        # Check for collision with the target
        if math.hypot(bullet["x"] - target_x, bullet["y"] - target_y) < target_radius:
            bullets.remove(bullet)
            score += 1
            target_x = random.randint(target_radius, WIDTH - target_radius)
            target_y = random.randint(target_radius, HEIGHT // 2)

        # Draw bullet
        pygame.draw.circle(screen, BLUE, (int(bullet["x"]), int(bullet["y"])), bullet_radius)

    # Draw cannon
    pygame.draw.circle(screen, BLACK, (cannon_x, cannon_y), cannon_radius)

    # Display score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
