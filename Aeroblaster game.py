import pygame
import sys
import random

pygame.init()

# Set up the game window
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aeroblaster")

# Load images
background_img = pygame.image.load("background.png").convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
player_img = pygame.image.load("player1.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (60, 60))
asteroid_img = pygame.image.load("asteroid1.png").convert_alpha()
asteroid_img = pygame.transform.scale(asteroid_img, (50, 50))

# Define game variables
player_size = 60  # Increase player size
player_speed = 10  # Increase player speed
projectile_speed = 300
projectile_cooldown = 30
projectile_timer = 0
player_x, player_y = WIDTH // 2, HEIGHT // 2  # Initialize player position in the center
asteroid_size = 50  # Increase asteroid size
cores = [(random.randint(WIDTH, WIDTH * 2), random.randint(0, HEIGHT - 50)) for _ in range(3)]
projectiles = []
game_over = False  # Flag to indicate if the game is over
score = 0  # Initialize score variable
timer = 0  # Initialize timer variable
font = pygame.font.SysFont(None, 36) 

# Define menu variables
menu_font = pygame.font.SysFont(None, 36)
menu_color = (255, 255, 255)
menu_text_start = menu_font.render("Start", True, menu_color)
menu_text_stop = menu_font.render("Stop", True, menu_color)
menu_rect = menu_text_start.get_rect()
menu_rect.topleft = (10, 10)
game_running = False

# Define game over text variables
game_over_font = pygame.font.SysFont(None, 72)
game_over_color = (255, 0, 0)
game_over_text = game_over_font.render("GAME OVER", True, game_over_color)
game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# Main game loop
clock = pygame.time.Clock()  
while True:
    win.blit(background_img, (0, 0))  

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if menu_rect.collidepoint(mouse_pos):
                game_running = not game_running
                if not game_running:
                    pygame.quit()
                    sys.exit()

    # Draw menu
    if game_running:
        win.blit(menu_text_stop, menu_rect)
    else:
        win.blit(menu_text_start, menu_rect)

    if not game_running:
        pygame.display.flip()
        continue

    # Move player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < HEIGHT - player_size:
        player_y += player_speed
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
        player_x += player_speed
    if keys[pygame.K_SPACE] and projectile_timer <= 0:
        projectiles.append((player_x + player_size, player_y + player_size // 2))
        projectile_timer = projectile_cooldown

    # Loop player horizontally
    if player_x > WIDTH:
        player_x = 0
    elif player_x < 0:
        player_x = WIDTH

    # Loop projectiles horizontally
    for i in range(len(projectiles)):
        projectiles[i] = (projectiles[i][0] + projectile_speed, projectiles[i][1])
        if projectiles[i][0] > WIDTH:
            del projectiles[i]
            break

    # Loop cores horizontally and check collision with player
    for i in range(len(cores)):
        cores[i] = (cores[i][0] - player_speed, cores[i][1])
        if cores[i][0] < 0:
            cores[i] = (random.randint(WIDTH, WIDTH * 2), random.randint(0, HEIGHT - 50))

        core_rect = pygame.Rect(cores[i][0], cores[i][1], asteroid_size, asteroid_size)
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        if core_rect.colliderect(player_rect):
            game_over = True
            break

    if game_over:
        win.blit(game_over_text, game_over_rect)
        pygame.display.flip()
        continue

    win.blit(player_img, (player_x, player_y))

    for projectile in projectiles:
        pygame.draw.circle(win, (0, 0, 255), projectile, 5)

    for core in cores:
        win.blit(asteroid_img, core)

    pygame.display.flip()

    timer += 1

    score = timer // 20  

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    win.blit(score_text, (10, 10))

    if projectile_timer > 0:
        projectile_timer -= 1

    clock.tick(60)  
