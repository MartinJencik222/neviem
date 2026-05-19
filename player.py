import pygame
from config import *

class Player:
    def __init__(self, x, y, player_id=1):
        self.x = x
        self.y = y
        self.player_id = player_id
        self.width = TILE_SIZE - 4
        self.height = TILE_SIZE - 4
        self.color = COLOR_PLAYER_1 if player_id == 1 else COLOR_PLAYER_2
        
        # Physics
        self.velocity_y = 0
        self.velocity_x = 0
        self.is_jumping = False
        self.is_falling = False
        self.on_ground = True
        
        # Controls
        if player_id == 1:
            self.up_key = pygame.K_UP
            self.down_key = pygame.K_DOWN
            self.left_key = pygame.K_LEFT
            self.right_key = pygame.K_RIGHT
            self.jump_key = pygame.K_SPACE
        else:
            self.up_key = pygame.K_w
            self.down_key = pygame.K_s
            self.left_key = pygame.K_a
            self.right_key = pygame.K_d
            self.jump_key = pygame.K_SPACE
        
        self.score = 0
        self.alive = True
        
    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        # Horizontal movement
        if keys[self.left_key]:
            self.x = max(0, self.x - PLAYER_SPEED)
        if keys[self.right_key]:
            self.x = min(SCREEN_WIDTH - self.width, self.x + PLAYER_SPEED)
        
        # Jump
        if keys[self.jump_key] and self.on_ground:
            self.velocity_y = -JUMP_HEIGHT
            self.is_jumping = True
            self.on_ground = False
    
    def update(self, terrain):
        # Apply gravity
        if not self.on_ground:
            self.velocity_y += GRAVITY
            self.y += self.velocity_y
            self.is_falling = self.velocity_y > 0
        
        # Check collision with terrain
        grid_x = self.x // GRID_SIZE
        grid_y = self.y // GRID_SIZE
        
        # Check if player is on valid ground
        self.on_ground = False
        
        if grid_y < len(terrain):
            current_tile = terrain[grid_y][int(grid_x)] if 0 <= int(grid_x) < len(terrain[grid_y]) else None
            
            if current_tile in ['grass', 'water_platform']:
                self.on_ground = True
                self.velocity_y = 0
                self.y = grid_y * GRID_SIZE
            elif current_tile == 'road':
                self.on_ground = True
                self.velocity_y = 0
                self.y = grid_y * GRID_SIZE
        
        # Check death conditions
        if grid_y >= len(terrain) or self.y > SCREEN_HEIGHT:
            self.alive = False
        
        if grid_x < 0 or grid_x >= SCREEN_WIDTH // GRID_SIZE:
            self.alive = False
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        # Draw eyes
        eye_offset_x = 4
        eye_offset_y = 4
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x + eye_offset_x), int(self.y + eye_offset_y)), 2)
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x + self.width - eye_offset_x), int(self.y + eye_offset_y)), 2)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def add_score(self, points):
        self.score += points
    
    def reset_position(self, x, y):
        self.x = x
        self.y = y
        self.velocity_y = 0
        self.velocity_x = 0
        self.is_jumping = False
        self.is_falling = False
        self.on_ground = True
