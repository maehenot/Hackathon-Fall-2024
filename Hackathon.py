import pygame
import random
import math

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1414, 1000))
clock = pygame.time.Clock()

# screen dimensions
screen_width = screen.get_width()
screen_height = screen.get_height()

pygame.display.set_caption("Rescue in the Shadow of the Singularity")
font = pygame.font.Font(None, 40)
font2 = pygame.font.Font(None, 55)

# initial variables
MAX_TIME = 60
score = 0
start = True # when running the program
running = False # starting the game
playing = False # starting the timer
dragging = False # for the slider
send = False # if the particle should be sent of not
dt = 0
PEACH = (237,142,113)
blackhole_mass = random.randint(1000, 2250) # between 10 and 30 Solar mass

# Slider settings
SILVER = (192, 192, 192)
slider_width = 400
slider_height = 5
slider_x = 100
slider_y = screen_height - 50

knob_radius = 10
knob_x = slider_x + slider_width // 2  # Start in the middle of the slider
knob_y = slider_y + slider_height // 2 # Aligned with slider bar

# blackhole image
image_blackhole = pygame.image.load("blackhole.png")
image_blackhole_resize = pygame.transform.scale(image_blackhole, (200 * (1+blackhole_mass/2000), 283 * (1+blackhole_mass/2000)))
black_hole_pos = [screen_width/2 - image_blackhole.get_width() / 2, screen_height / 2 - image_blackhole.get_height() / 2]

# guy image
image_guy = pygame.image.load("guy.png")
image_guy = pygame.transform.scale(image_guy, (210, 270))
guy_pos = [200 - image_guy.get_width() / 2, screen_height / 2 - image_guy.get_height() / 2]

# spaceship image
image_spaceship = pygame.image.load("spaceship.png")
image_spaceship = pygame.transform.scale(image_spaceship, (168, 119))
spaceship_height = image_spaceship.get_height()
spaceship_width = image_spaceship.get_width()

# arrow image
arrow = pygame.Surface((80, 20), pygame.SRCALPHA)
pygame.draw.polygon(arrow, PEACH, [(0, 5), (40, 0), (40, 10)])

# Welcome image
image_welcome = pygame.image.load("welcome.png")

# Game over message
image_gameover = pygame.image.load("gameover.png")

# Range for theta
theta_min = 1
theta_max = 80
theta = 25.5  # Initial value

x_initial = 220  # Starting position for x
y_initial = 495  # Starting position for y

M_SUN = 1.988 * 10 ** 30  # Mass of the Sun
G = 6.6743 * 10 ** -11  # Gravitational Constant
C = 299792458  # Speed of Light
M_BH = blackhole_mass * M_SUN

distance_x = (screen_width / 2 - x_initial)  # distance between astronaut and BH

x = x_initial
y = y_initial
radius = 7  # Circle radius
r = (10 / math.pi) * (2 * G * M_SUN * 1000 / (C ** 2))  #

# Angles
b = math.tan(theta * math.pi / 180) * r  # impact parameter
phi = (4 * G * M_BH) / (C ** 2 * b)
beta = phi - theta * math.pi / 180

# adjusting the angle
if beta >= math.pi / 2:
    beta = math.pi / 2.01

dx_1, dy_1 = 5, math.tan(theta * math.pi / 180) * 5/3  # towards the BH
dx_2, dy_2 = 5, math.tan(beta) * 5/3 # Away from the BH


# rotating the pointing arrow
def draw_rotated_arrow(value):
    angle = value + 180  # maps the slider value to an angle between 0 and 360
    rotated_arrow = pygame.transform.rotate(arrow, angle)
    new_rect = rotated_arrow.get_rect(center=(220, 495))  # center the arrow
    screen.blit(rotated_arrow, new_rect.topleft)


# position of the stars
x_small, x_big = [], []
y_small, y_big = [], []
for i in range(200):
    x_small.append(random.random() * screen_width)
    x_big.append(random.random() * screen_width)
    y_small.append(random.random() * screen_height)
    y_big.append(random.random() * screen_height)
# forming stars at random places
star_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
star_surface.fill((0, 0, 0, 0))
for i in range(200):
    pygame.draw.circle(star_surface, "white", [x_small[i], y_small[i]], 2.5)
    pygame.draw.circle(star_surface, "white", [x_big[i], y_big[i]], 1)

# position of the target
min_pos_x_target = 3 * screen_width / 5 + 100
min_pos_y_target = screen_height / 3
pos_x_target = min_pos_x_target + random.random() * screen_width / 4
pos_y_target = min_pos_y_target + random.random() * screen_width / 3


# Welcome page
while start:
    # Allowing for the user to quit the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False

    # Displaying the screen
    pygame.display.flip()
    screen.blit(image_welcome, (0,0))

    # Checking if the user started the game by pressing the space key
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        start = False
        running = True
        playing = True
        start_ticks = pygame.time.get_ticks()


# game play
while running:

    # Allowing for the user to quit the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # pygame.QUIT == clicked X to close window
            running = False

        # slider
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos # Event.pos saves coordinates where mouse clicked when button was pressed

            # Checks whether mouse is in slider area usng pythagorian thrm
            if (mouse_x - knob_x) ** 2 + (mouse_y - knob_y) ** 2 <= knob_radius ** 2:
                dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False

        elif event.type == pygame.MOUSEMOTION and dragging:
            # Drag knob within the slider's range
            mouse_x, _ = event.pos
            knob_x = max(slider_x, min(mouse_x, slider_x + slider_width)) # Ensures it stays within bounds


    if playing:
        # Calculate remaining time
        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
        remaining_time = max(0, MAX_TIME - elapsed_time)

        # Displaying objects on the screen
        screen.fill("black")
        screen.blit(star_surface, (0, 0))
        black_hole_pos = [screen_width / 2 - image_blackhole_resize.get_width() / 2,\
                          screen_height / 2 - image_blackhole_resize.get_height() / 2]
        screen.blit(image_blackhole_resize, black_hole_pos)
        screen.blit(image_guy, guy_pos)
        # screen.blit(arrow_image_rotated, arrow_rotated_pos)

        # The target to hit
        screen.blit(image_spaceship, [pos_x_target - spaceship_width / 2, pos_y_target - spaceship_height / 2])

        # Display timer
        timer_text = f"{remaining_time:.1f} s"
        text_surface = font.render(timer_text, True, "white")
        text_rect = text_surface.get_rect(topright=(screen_width - 10, 10))  # Top-right corner
        screen.blit(text_surface, text_rect)

        # Display score
        score_text = f"Score: {score}"
        text_surface_score = font.render(score_text, True, "white")
        text_rect_score = text_surface_score.get_rect(topright=(screen_width - 10, 40))
        screen.blit(text_surface_score, text_rect_score)

        # Display mass blackhole
        mass_text = f"Mass of the black hole: {blackhole_mass} Solar Masses"
        text_surface_mass = font.render(mass_text, True, "white")
        text_rect_mass = text_surface_mass.get_rect(bottomright=(screen_width - 20, screen_height - 20))
        screen.blit(text_surface_mass, text_rect_mass)

        # Display instructions
        instructions1_text = "Use the slider to vary the angle and aim at the ship"
        text_surface_instructions1 = font.render(instructions1_text, True, "white")
        text_rect_instructions1 = text_surface_instructions1.get_rect(center = (screen_width // 2, 60))
        screen.blit(text_surface_instructions1, text_rect_instructions1)

        instructions2_text = "Press ENTER to send the signal"
        text_surface_instructions2 = font.render(instructions2_text, True, "white")
        text_rect_instructions2 = text_surface_instructions2.get_rect(center = (screen_width // 2, 100))
        screen.blit(text_surface_instructions2, text_rect_instructions2)

        # Display slider
        theta = theta_min + (knob_x - slider_x) / slider_width * (theta_max - theta_min) # Map the knob position to theta
        pygame.draw.rect(screen, "white", (slider_x, slider_y, slider_width, slider_height)) # Draw slider bar
        pygame.draw.circle(screen, SILVER, (knob_x, knob_y), knob_radius) # Draw slider knob
        # Display the current theta value
        theta_text = font.render(f"Angle: {theta:.1f}°", True, "white")
        text_rect = theta_text.get_rect(bottomleft=(100, slider_y - 30))
        screen.blit(theta_text, text_rect)

        # Rotating the aiming arrow
        draw_rotated_arrow(theta)

        # The user wants to send the message: update the value
        if pygame.key.get_pressed()[pygame.K_RETURN] and not send:

            M_BH = blackhole_mass * M_SUN
            # Angles
            b = math.tan(theta * math.pi / 180) * r  # impact parameter
            phi = (4 * G * M_BH) / (C ** 2 * b)
            beta = phi - theta * math.pi / 180

            # adjusting the angle


            dx_1, dy_1 = 5, math.tan(theta * math.pi/180) * 5/3  # towards the BH
            dx_2, dy_2 = 5, math.tan(beta) * 5/3  # Away from the BH

            send = True

        # checking if the user aimed right and got to the spaceship; if yes updating the score and
        if abs(x - pos_x_target) < 40 and abs(y - pos_y_target) < 20:
            pos_x_target = min_pos_x_target + random.random() * screen_width / 4
            pos_y_target = min_pos_y_target + random.random() * screen_width / 3
            blackhole_mass = random.randint(1000, 2250)
            M_BH = blackhole_mass * M_SUN
            image_blackhole_resize = pygame.transform.scale(image_blackhole,\
                                    (200 * (1+blackhole_mass/2000), 283 * (1+blackhole_mass/2000)))
            score += 1
            x = x_initial
            y = y_initial
            send = False

        if send:
            if x >= screen_width / 2:  # Movement of the laser after passing BH
                if beta >= 1.396:
                    x = x_initial
                    y = y_initial
                    send = False

                else:
                    x += dx_2
                    y += dy_2

            else:  # Movement of the laser before passing BH
                x += dx_1
                y -= dy_1

            # Draw the object
            pygame.draw.circle(screen, PEACH, (x, y), radius)

            # Draw the object
            pygame.draw.circle(screen, PEACH, (x, y), radius)
            if x > screen_width or y < 0 or y > screen_height:
                x = x_initial
                y = y_initial
                send = False

        # End the game when time runs out
        if remaining_time == 0:
            x = x_initial
            y = y_initial
            send = False
            playing = False

    # ran out of time
    else:
        # Render the restart prompt and add score
        text_surface = font2.render(f' {score}', True, "white")
        text_rect = text_surface.get_rect(center=(screen_width // 1.84, screen_height // 2.249))
        screen.blit(image_gameover, (0,0))
        screen.blit(text_surface, text_rect)
        pygame.display.flip()

        # Wait for player input to restart
        waiting_for_restart = True
        while waiting_for_restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting_for_restart = False

                if pygame.key.get_pressed()[pygame.K_r]:
                    waiting_for_restart = False
                    playing = True
                    start_ticks = pygame.time.get_ticks()

                    # Restarting count down and scores
                    remaining_time = MAX_TIME
                    score = 0

                    # changing the position of the target
                    pos_x_target = min_pos_x_target + random.random() * screen_width / 5
                    pos_y_target = min_pos_y_target + random.random() * screen_width / 3

                    # changing the mass of the black hole
                    blackhole_mass = random.randint(1000, 2250)

                    image_blackhole_resize = pygame.transform.scale(image_blackhole,\
                                            (200 * (1 + blackhole_mass / 2000), 283 * (1 + blackhole_mass / 2000)))


    # flip() the display to put your work on screen
    pygame.display.flip()


    dt = clock.tick(60) / 1000

pygame.quit()




