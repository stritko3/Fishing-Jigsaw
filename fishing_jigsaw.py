import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (173, 216, 230)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)

# Shape colors
SHAPE_COLORS = {
    "L": GREEN,               # Green
    "Reversed L": YELLOW,     # Yellow
    "Square": LIGHT_BLUE,     # Light Blue
    "I": BLUE,                # Blue
    "Z": RED,                 # Red
    "Single": ORANGE,         # Orange
}

# Grid dimensions
GRID_COLS = 6
GRID_ROWS = 4
TILE_SIZE = 50

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fishing Jigsaw")

# Font for text
font = pygame.font.Font(None, 36)

# Center the grid
GRID_X = (SCREEN_WIDTH - GRID_COLS * TILE_SIZE) // 2
GRID_Y = 50

# Button dimensions
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50
BUTTON_X = (SCREEN_WIDTH - BUTTON_WIDTH) // 2
BUTTON_Y = SCREEN_HEIGHT - 100

# Shapes
SHAPES = {
    "L": [(0, 0), (0, -1), (1, 0)],             # Green
    "Reversed L": [(0, 0), (0, 1), (-1, 0)],   # Yellow
    "Square": [(0, 0), (1, 0), (0, 1), (1, 1)], # Light Blue
    "I": [(0, 0), (0, 1), (0, 2)],             # Blue
    "Z": [(0, 0), (1, 0), (1, 1), (2, 1)],     # Red
    "Single": [(0, 0)],                        # Orange
}

# Generate random shape
current_shape = None
def generate_shape():
    shape_name = random.choice(list(SHAPES.keys()))
    shape_coords = SHAPES[shape_name]
    return shape_name, shape_coords

# Draw grid
def draw_grid():
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            rect = pygame.Rect(GRID_X + col * TILE_SIZE, GRID_Y + row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 1)

# Draw shape
def draw_shape(coords, x_offset, y_offset, shape_name):
    color = SHAPE_COLORS.get(shape_name, GREEN)  # Default to green if shape not found
    for x, y in coords:
        rect = pygame.Rect(GRID_X + (x + x_offset) * TILE_SIZE, GRID_Y + (y + y_offset) * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)

# Check if shape can be placed
def can_place(coords, x_offset, y_offset, placed_tiles):
    for x, y in coords:
        grid_x = x + x_offset
        grid_y = y + y_offset
        if grid_x < 0 or grid_x >= GRID_COLS or grid_y < 0 or grid_y >= GRID_ROWS:
            return False
        if (grid_x, grid_y) in placed_tiles:
            return False
    return True

# Place shape on grid
def place_shape(coords, x_offset, y_offset, placed_tiles):
    for x, y in coords:
        grid_x = x + x_offset
        grid_y = y + y_offset
        placed_tiles.add((grid_x, grid_y))

# Draw button
def draw_button():
    button_rect = pygame.Rect(BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(screen, GRAY, button_rect)
    pygame.draw.rect(screen, DARK_GRAY, button_rect, 2)
    text = font.render("Open", True, BLACK)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)
    return button_rect

# Function to reset the game when grid is filled
def reset_game():
    return set(), 0  # Empty placed tiles set and reset pieces used counter

# Main loop
placed_tiles = set()
pieces_used = 0  # Combined counter for placed and discarded pieces
s_chest = 0
m_chest = 0
l_chest = 0
running = True
holding_shape = False
hover_coords = None

while running:
    screen.fill(WHITE)

    # Draw grid and placed tiles
    draw_grid()
    for x, y in placed_tiles:
        rect = pygame.Rect(GRID_X + x * TILE_SIZE, GRID_Y + y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, BLUE, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)

    # Draw current shape
    if holding_shape and hover_coords:
        draw_shape(current_shape[1], *hover_coords, current_shape[0])

    # Display piece count
    text = font.render(f"Pieces Used: {pieces_used}", True, BLACK)
    screen.blit(text, (10, 10))

    # Display chest counters
    text_s = font.render(f"S Chests: {s_chest}", True, BLACK)
    screen.blit(text_s, (10, 50))

    text_m = font.render(f"M Chests: {m_chest}", True, BLACK)
    screen.blit(text_m, (10, 90))

    text_l = font.render(f"L Chests: {l_chest}", True, BLACK)
    screen.blit(text_l, (10, 130))

    # Draw the button
    button_rect = draw_button()

    # Check if the grid is filled and reset the game if it is
    if len(placed_tiles) == GRID_COLS * GRID_ROWS:
        # Update chest counters based on pieces used
        if pieces_used >= 25:
            s_chest += 1
        elif 11 <= pieces_used <= 24:
            m_chest += 1
        elif pieces_used <= 10:
            l_chest += 1

        # Now reset the game
        placed_tiles, pieces_used = reset_game()

    pygame.display.flip()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            if event.button == 1:  # Left click
                if holding_shape:  # Place shape
                    if can_place(current_shape[1], *hover_coords, placed_tiles):
                        place_shape(current_shape[1], *hover_coords, placed_tiles)
                        pieces_used += 1  # Increment pieces used for placed shape
                        holding_shape = False
                        hover_coords = None
                elif button_rect.collidepoint(mouse_x, mouse_y) and not holding_shape:  # Open button
                    current_shape = generate_shape()
                    holding_shape = True

            elif event.button == 3 and holding_shape:  # Right click to discard
                pieces_used += 1  # Increment pieces used for discarded shape
                holding_shape = False
                hover_coords = None

    # Update hover position
    if holding_shape:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        grid_x = (mouse_x - GRID_X) // TILE_SIZE
        grid_y = (mouse_y - GRID_Y) // TILE_SIZE
        hover_coords = (grid_x, grid_y)

pygame.quit()
