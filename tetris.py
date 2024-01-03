import pygame
import random

# Constants
WIDTH, HEIGHT = 300, 600
GRID_SIZE = 30
GRID_WIDTH, GRID_HEIGHT = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE
FPS = 7

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1, 1], [1]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 1], [0, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1]],
]

# Tetromino colors
COLORS = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
    (128, 0, 128),
]

# Initialize Pygame
pygame.init()

# Initialize game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

# Define functions
def draw_grid():
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, (255, 255, 255), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, (255, 255, 255), (0, y), (WIDTH, y))

def draw_tetromino(tetromino, position, color):
    for y, row in enumerate(tetromino):
        for x, value in enumerate(row):
            if value:
                pygame.draw.rect(
                    screen,
                    color,
                    (position[0] * GRID_SIZE + x * GRID_SIZE, position[1] * GRID_SIZE + y * GRID_SIZE, GRID_SIZE, GRID_SIZE),
                )
                pygame.draw.rect(
                    screen,
                    (0, 0, 0),
                    (position[0] * GRID_SIZE + x * GRID_SIZE, position[1] * GRID_SIZE + y * GRID_SIZE, GRID_SIZE, GRID_SIZE),
                    2,
                )

def check_collision(tetromino, position, grid):
    for y, row in enumerate(tetromino):
        for x, value in enumerate(row):
            if value:
                if (
                    position[0] + x < 0
                    or position[0] + x >= GRID_WIDTH
                    or position[1] + y >= GRID_HEIGHT
                    or grid[position[1] + y][position[0] + x] != 0
                ):
                    return True
    return False

def merge_tetromino(tetromino, position, grid):
    for y, row in enumerate(tetromino):
        for x, value in enumerate(row):
            if value:
                grid[position[1] + y][position[0] + x] = 1

def remove_completed_rows(grid):
    completed_rows = [i for i, row in enumerate(grid) if all(row)]
    for row in completed_rows:
        del grid[row]
        grid.insert(0, [0] * GRID_WIDTH)

def draw_score(score):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

# Game loop
clock = pygame.time.Clock()
game_over = False
grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
current_tetromino = random.choice(SHAPES)
current_tetromino_position = [GRID_WIDTH // 2 - len(current_tetromino[0]) // 2, 0]
score = 0

# Additional variables for button states
left_button_pressed = False
right_button_pressed = False
down_button_pressed = False
rotate_button_pressed = False
hold_button_pressed = False

# Additional game features
hold_tetromino = None  # Hold a tetromino for later use
next_tetromino = random.choice(SHAPES)  # Display the next tetromino
can_hold = True  # Allow holding only once per tetromino

# Set key repeat settings
pygame.key.set_repeat(200, 50)  # Delays: 200ms, Intervals: 50ms

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        # Handle keyboard events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                left_button_pressed = True
            elif event.key == pygame.K_RIGHT:
                right_button_pressed = True
            elif event.key == pygame.K_DOWN:
                down_button_pressed = True
            elif event.key == pygame.K_SPACE:
                rotate_button_pressed = True
            elif event.key == pygame.K_c and can_hold:
                hold_button_pressed = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left_button_pressed = False
            elif event.key == pygame.K_RIGHT:
                right_button_pressed = False
            elif event.key == pygame.K_DOWN:
                down_button_pressed = False
            elif event.key == pygame.K_SPACE:
                rotate_button_pressed = False
            elif event.key == pygame.K_c:
                hold_button_pressed = False

    # Move the tetromino left
    if left_button_pressed:
        new_position = [current_tetromino_position[0] - 1]
        new_position = [current_tetromino_position[0] - 1, current_tetromino_position[1]]
        if not check_collision(current_tetromino, new_position, grid):
            current_tetromino_position = new_position
        left_button_pressed = False

    # Move the tetromino right
    if right_button_pressed:
        new_position = [current_tetromino_position[0] + 1, current_tetromino_position[1]]
        if not check_collision(current_tetromino, new_position, grid):
            current_tetromino_position = new_position
        right_button_pressed = False

    # Move the tetromino down
    if down_button_pressed:
        new_position = [current_tetromino_position[0], current_tetromino_position[1] + 1]
        if not check_collision(current_tetromino, new_position, grid):
            current_tetromino_position = new_position
        down_button_pressed = False

    # Rotate the tetromino
    if rotate_button_pressed:
        rotated_tetromino = list(zip(*reversed(current_tetromino)))
        if not check_collision(rotated_tetromino, current_tetromino_position, grid):
            current_tetromino = rotated_tetromino
        rotate_button_pressed = False

    # Hold the tetromino
    if hold_button_pressed:
        if can_hold:
            if hold_tetromino is None:
                hold_tetromino = current_tetromino
                current_tetromino = next_tetromino
                next_tetromino = random.choice(SHAPES)
                current_tetromino_position = [GRID_WIDTH // 2 - len(current_tetromino[0]) // 2, 0]
            else:
                temp = hold_tetromino
                hold_tetromino = current_tetromino
                current_tetromino = temp
                current_tetromino_position = [GRID_WIDTH // 2 - len(current_tetromino[0]) // 2, 0]
            can_hold = False
        hold_button_pressed = False

    # Move the tetromino down automatically
    new_position = [current_tetromino_position[0], current_tetromino_position[1] + 1]
    if not check_collision(current_tetromino, new_position, grid):
        current_tetromino_position = new_position
    else:
        merge_tetromino(current_tetromino, current_tetromino_position, grid)
        remove_completed_rows(grid)

        # Spawn a new tetromino
        current_tetromino = next_tetromino
        next_tetromino = random.choice(SHAPES)
        current_tetromino_position = [GRID_WIDTH // 2 - len(current_tetromino[0]) // 2, 0]

        # Check for game over
        if check_collision(current_tetromino, current_tetromino_position, grid):
            game_over = True

        can_hold = True

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the grid
    draw_grid()

    # Draw the current tetromino
    draw_tetromino(current_tetromino, current_tetromino_position, COLORS[SHAPES.index(current_tetromino)])

    # Draw the hold tetromino
    if hold_tetromino is not None:
        draw_tetromino(hold_tetromino, [0, 0], COLORS[SHAPES.index(hold_tetromino)])

    # Draw the next tetromino
    draw_tetromino(next_tetromino, [GRID_WIDTH + 2, 2], COLORS[SHAPES.index(next_tetromino)])

    for y, row in enumerate(grid):
        for x, value in enumerate(row):
            if value:
                pygame.draw.rect(screen, (255, 255, 255), (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, (0, 0, 0), (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 2)

    # Draw the score
    draw_score(score)

    # Update the display
    pygame.display.flip()

    # Control the game speed
    clock.tick(FPS)

# Quit the game
pygame.quit()