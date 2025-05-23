#!/usr/bin/env python3
"""
Direct launcher for the updated Road Rash style game.
"""

import os
import sys
import pygame
import random
import boto3
from pygame.locals import *

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ROAD_WIDTH = 400
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 100
ENEMY_WIDTH = 50
ENEMY_HEIGHT = 100
OBSTACLE_WIDTH = 30
OBSTACLE_HEIGHT = 30
ROAD_SPEED = 3  # Reduced from 5 to make game longer
ENEMY_SPEED = 2  # Reduced from 3 to make game longer
OBSTACLE_SPEED = 2.5  # Reduced from 4 to make game longer
CLOUD_WIDTH = 80
CLOUD_HEIGHT = 40
GRASS_WIDTH = 40
GRASS_HEIGHT = 30
BOARD_WIDTH = 60
BOARD_HEIGHT = 80

# Colors
SKY_BLUE = (135, 206, 235)
GRAY = (100, 100, 100)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Enemy states
PATROL = "patrol"
CHASE = "chase"
ATTACK = "attack"

class AssetManager:
    """Manages game assets including downloading from S3 when needed"""
    def __init__(self, bucket_name="road-rash-game-assets"):
        self.bucket_name = bucket_name
        self.assets_dir = "assets"
        self.ensure_assets_dir()
        
        # Load assets from files
        self.assets = self.load_assets()
    
    def ensure_assets_dir(self):
        """Create assets directory if it doesn't exist"""
        if not os.path.exists(self.assets_dir):
            os.makedirs(self.assets_dir)
    
    def load_assets(self):
        """Load game assets from files"""
        assets = {}
        
        try:
            assets["player"] = pygame.image.load(os.path.join(self.assets_dir, "player.png"))
            assets["enemy"] = pygame.image.load(os.path.join(self.assets_dir, "enemy.png"))
            assets["obstacle"] = pygame.image.load(os.path.join(self.assets_dir, "obstacle.png"))
            assets["cloud"] = pygame.image.load(os.path.join(self.assets_dir, "cloud.png"))
            assets["grass"] = pygame.image.load(os.path.join(self.assets_dir, "grass.png"))
            assets["highway_board"] = pygame.image.load(os.path.join(self.assets_dir, "highway_board.png"))
            
            # Resize images to match game dimensions
            assets["player"] = pygame.transform.scale(assets["player"], (PLAYER_WIDTH, PLAYER_HEIGHT))
            assets["enemy"] = pygame.transform.scale(assets["enemy"], (ENEMY_WIDTH, ENEMY_HEIGHT))
            assets["obstacle"] = pygame.transform.scale(assets["obstacle"], (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
            assets["cloud"] = pygame.transform.scale(assets["cloud"], (CLOUD_WIDTH, CLOUD_HEIGHT))
            assets["grass"] = pygame.transform.scale(assets["grass"], (GRASS_WIDTH, GRASS_HEIGHT))
            assets["highway_board"] = pygame.transform.scale(assets["highway_board"], (BOARD_WIDTH, BOARD_HEIGHT))
            
            return assets
        except Exception as e:
            print(f"Error loading assets: {e}")
            print("Make sure you've run create_default_assets.py first")
            sys.exit(1)

class Player:
    """Player class representing the user's bike"""
    def __init__(self, x, y, sprite):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.speed = ROAD_SPEED
        self.score = 0
    
    def move(self, dx, dy):
        """Move the player by the given delta x and y"""
        # Constrain player to road boundaries
        road_left = (SCREEN_WIDTH - ROAD_WIDTH) // 2
        road_right = road_left + ROAD_WIDTH
        
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Keep player within road boundaries
        if new_x < road_left:
            new_x = road_left
        elif new_x + PLAYER_WIDTH > road_right:
            new_x = road_right - PLAYER_WIDTH
        
        # Keep player within screen height
        if new_y < 0:
            new_y = 0
        elif new_y + PLAYER_HEIGHT > SCREEN_HEIGHT:
            new_y = SCREEN_HEIGHT - PLAYER_HEIGHT
        
        self.x = new_x
        self.y = new_y
    
    def draw(self, screen):
        """Draw the player on the screen"""
        screen.blit(self.sprite, (self.x, self.y))
    
    def get_rect(self):
        """Get the player's rectangle for collision detection"""
        return pygame.Rect(self.x, self.y, PLAYER_WIDTH, PLAYER_HEIGHT)
    
    def increase_speed(self):
        """Increase player speed"""
        self.speed += 0.05  # Reduced from 0.1 to make game longer
        if self.speed > 12:  # Reduced from 15 to make game longer
            self.speed = 12
    
    def update_score(self, points=1):
        """Update the player's score"""
        self.score += points

class Enemy:
    """Enemy biker class with finite state machine behavior"""
    def __init__(self, sprite):
        self.sprite = sprite
        self.state = PATROL
        self.target = None
        self.reset()
    
    def reset(self):
        """Reset enemy position to top of screen at random x position"""
        road_left = (SCREEN_WIDTH - ROAD_WIDTH) // 2
        self.x = random.randint(road_left, road_left + ROAD_WIDTH - ENEMY_WIDTH)
        self.y = -ENEMY_HEIGHT
        self.patrol_direction = random.choice([-1, 1])  # Left or right
        self.patrol_timer = random.randint(30, 90)  # Frames to patrol in one direction
        self.attack_cooldown = 0
    
    def update(self, player_speed, player=None):
        """Update enemy position based on current state"""
        # Basic movement down the road
        base_speed = ENEMY_SPEED + (player_speed / 4)  # Changed from /3 to /4 to make game longer
        self.y += base_speed
        
        # State machine behavior
        if player:
            # Calculate distance to player
            dx = player.x - self.x
            dy = player.y - self.y
            distance = (dx**2 + dy**2)**0.5
            
            # State transitions
            if self.state == PATROL:
                if distance < 200:  # Detection range
                    self.change_state(CHASE)
                    self.target = player
                else:
                    self.patrol()
            
            elif self.state == CHASE:
                if distance < 50:  # Attack range
                    self.change_state(ATTACK)
                elif distance > 250:  # Lost player
                    self.change_state(PATROL)
                else:
                    self.chase(dx, dy)
            
            elif self.state == ATTACK:
                if distance > 70:  # Out of attack range
                    self.change_state(CHASE)
                else:
                    self.attack(dx, dy)
        else:
            # Default to patrol if no player is provided
            self.patrol()
        
        # If enemy goes off screen, reset position
        if self.y > SCREEN_HEIGHT:
            self.reset()
    
    def change_state(self, new_state):
        """Change the enemy's state"""
        self.state = new_state
    
    def patrol(self):
        """Patrol behavior - move side to side"""
        road_left = (SCREEN_WIDTH - ROAD_WIDTH) // 2
        road_right = road_left + ROAD_WIDTH - ENEMY_WIDTH
        
        # Move in patrol direction
        self.x += self.patrol_direction * 1.5  # Reduced from 2 to make game longer
        
        # Decrease patrol timer
        self.patrol_timer -= 1
        
        # Change direction if hitting boundary or timer expired
        if self.x <= road_left or self.x >= road_right or self.patrol_timer <= 0:
            self.patrol_direction *= -1
            self.patrol_timer = random.randint(30, 90)
        
        # Keep within road boundaries
        self.x = max(road_left, min(self.x, road_right))
    
    def chase(self, dx, dy):
        """Chase behavior - move toward player"""
        # Normalize direction
        distance = max(1, (dx**2 + dy**2)**0.5)
        dx = dx / distance
        dy = dy / distance
        
        # Move toward player, but slower horizontally than vertically
        self.x += dx * 1.5  # Reduced from 2 to make game longer
        
        # Keep within road boundaries
        road_left = (SCREEN_WIDTH - ROAD_WIDTH) // 2
        road_right = road_left + ROAD_WIDTH - ENEMY_WIDTH
        self.x = max(road_left, min(self.x, road_right))
    
    def attack(self, dx, dy):
        """Attack behavior - try to ram the player"""
        if self.attack_cooldown <= 0:
            # Aggressive movement toward player
            distance = max(1, (dx**2 + dy**2)**0.5)
            dx = dx / distance
            dy = dy / distance
            
            # Move faster toward player
            self.x += dx * 2  # Reduced from 3 to make game longer
            
            # Keep within road boundaries
            road_left = (SCREEN_WIDTH - ROAD_WIDTH) // 2
            road_right = road_left + ROAD_WIDTH - ENEMY_WIDTH
            self.x = max(road_left, min(self.x, road_right))
            
            # Set attack cooldown
            self.attack_cooldown = 30  # Increased from 20 to make game longer
        else:
            self.attack_cooldown -= 1
    
    def draw(self, screen):
        """Draw the enemy on the screen"""
        screen.blit(self.sprite, (self.x, self.y))
    
    def get_rect(self):
        """Get the enemy's rectangle for collision detection"""
        return pygame.Rect(self.x, self.y, ENEMY_WIDTH, ENEMY_HEIGHT)

class Obstacle:
    """Road obstacle class"""
    def __init__(self, sprite):
        self.sprite = sprite
        self.reset()
    
    def reset(self):
        """Reset obstacle position to top of screen at random x position"""
        road_left = (SCREEN_WIDTH - ROAD_WIDTH) // 2
        self.x = random.randint(road_left, road_left + ROAD_WIDTH - OBSTACLE_WIDTH)
        self.y = -OBSTACLE_HEIGHT
    
    def update(self, player_speed):
        """Update obstacle position"""
        self.y += OBSTACLE_SPEED + (player_speed / 4)  # Changed from /3 to /4 to make game longer
        
        # If obstacle goes off screen, reset position
        if self.y > SCREEN_HEIGHT:
            self.reset()
    
    def draw(self, screen):
        """Draw the obstacle on the screen"""
        screen.blit(self.sprite, (self.x, self.y))
    
    def get_rect(self):
        """Get the obstacle's rectangle for collision detection"""
        return pygame.Rect(self.x, self.y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)

class Cloud:
    """Cloud class for sky decoration"""
    def __init__(self, sprite):
        self.sprite = sprite
        self.reset()
    
    def reset(self):
        """Reset cloud position"""
        self.x = random.randint(0, SCREEN_WIDTH - CLOUD_WIDTH)
        self.y = random.randint(-CLOUD_HEIGHT, SCREEN_HEIGHT // 2)
        self.speed = random.uniform(0.3, 1.0)  # Reduced from 0.5-1.5 to make game longer
    
    def update(self):
        """Update cloud position"""
        self.x -= self.speed
        
        # If cloud goes off screen, reset position
        if self.x + CLOUD_WIDTH < 0:
            self.x = SCREEN_WIDTH
            self.y = random.randint(-CLOUD_HEIGHT, SCREEN_HEIGHT // 2)
            self.speed = random.uniform(0.3, 1.0)  # Reduced from 0.5-1.5 to make game longer
    
    def draw(self, screen):
        """Draw the cloud on the screen"""
        screen.blit(self.sprite, (self.x, self.y))

class Sky:
    """Sky class for background"""
    def __init__(self, cloud_sprite):
        self.color = SKY_BLUE
        self.clouds = [Cloud(cloud_sprite) for _ in range(5)]
    
    def update(self):
        """Update sky elements"""
        for cloud in self.clouds:
            cloud.update()
    
    def draw(self, screen):
        """Draw the sky and clouds"""
        # Sky is drawn as background in the main game class
        for cloud in self.clouds:
            cloud.draw(screen)

class Grass:
    """Grass class for roadside decoration"""
    def __init__(self, sprite, side="left"):
        self.sprite = sprite
        self.side = side
        self.patches = []
        self.initialize_patches()
    
    def initialize_patches(self):
        """Initialize grass patches along the roadside"""
        road_left = (SCREEN_WIDTH - ROAD_WIDTH) // 2
        road_right = road_left + ROAD_WIDTH
        
        # Create grass patches along the road
        if self.side == "left":
            x_base = road_left - GRASS_WIDTH
            for i in range(10):
                y = random.randint(0, SCREEN_HEIGHT)
                self.patches.append((x_base, y))
        else:  # right side
            x_base = road_right
            for i in range(10):
                y = random.randint(0, SCREEN_HEIGHT)
                self.patches.append((x_base, y))
    
    def update(self, speed):
        """Update grass patch positions"""
        for i in range(len(self.patches)):
            x, y = self.patches[i]
            y += speed
            
            # If patch goes off screen, reset to top
            if y > SCREEN_HEIGHT:
                y = -GRASS_HEIGHT
            
            self.patches[i] = (x, y)
    
    def draw(self, screen):
        """Draw grass patches"""
        for x, y in self.patches:
            screen.blit(self.sprite, (x, y))

class HighwayBoard:
    """Highway board class for roadside signs"""
    def __init__(self, sprite):
        self.sprite = sprite
        self.boards = []
        self.initialize_boards()
    
    def initialize_boards(self):
        """Initialize highway boards along the roadside"""
        road_left = (SCREEN_WIDTH - ROAD_WIDTH) // 2
        road_right = road_left + ROAD_WIDTH
        
        # Create boards on both sides of the road
        positions = [
            (road_left - BOARD_WIDTH - 10, -BOARD_HEIGHT),  # Left side
            (road_right + 10, -BOARD_HEIGHT * 3),           # Right side
            (road_left - BOARD_WIDTH - 10, -BOARD_HEIGHT * 6)  # Left side again
        ]
        
        self.boards = positions
    
    def update(self, speed):
        """Update board positions"""
        for i in range(len(self.boards)):
            x, y = self.boards[i]
            y += speed
            
            # If board goes off screen, reset to top with random offset
            if y > SCREEN_HEIGHT:
                y = -BOARD_HEIGHT - random.randint(0, 300)
                
                # Keep the same side (left or right)
                road_left = (SCREEN_WIDTH - ROAD_WIDTH) // 2
                road_right = road_left + ROAD_WIDTH
                
                if x < SCREEN_WIDTH // 2:  # Left side
                    x = road_left - BOARD_WIDTH - 10
                else:  # Right side
                    x = road_right + 10
            
            self.boards[i] = (x, y)
    
    def draw(self, screen):
        """Draw highway boards"""
        for x, y in self.boards:
            screen.blit(self.sprite, (x, y))

class Road:
    """Road class for handling road animation"""
    def __init__(self):
        self.width = ROAD_WIDTH
        self.x = (SCREEN_WIDTH - self.width) // 2
        self.stripe_height = 50
        self.stripe_width = 10
        self.stripe_gap = 30
        self.stripes = []
        
        # Initialize road stripes
        for y in range(-self.stripe_height, SCREEN_HEIGHT + self.stripe_height, self.stripe_height + self.stripe_gap):
            self.stripes.append(y)
    
    def update(self, speed):
        """Update road stripe positions for scrolling effect"""
        for i in range(len(self.stripes)):
            self.stripes[i] += speed
            
            # If stripe goes off screen, reset to top
            if self.stripes[i] > SCREEN_HEIGHT:
                self.stripes[i] = -self.stripe_height
    
    def draw(self, screen):
        """Draw the road and stripes"""
        # Draw road
        pygame.draw.rect(screen, GRAY, (self.x, 0, self.width, SCREEN_HEIGHT))
        
        # Draw center line stripes
        for y in self.stripes:
            pygame.draw.rect(screen, WHITE, 
                            (self.x + (self.width // 2) - (self.stripe_width // 2), 
                             y, 
                             self.stripe_width, 
                             self.stripe_height))

class Game:
    """Main game class"""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Road Rash Style Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        self.font = pygame.font.SysFont(None, 36)
        
        # Initialize asset manager
        self.asset_manager = AssetManager()
        
        # Initialize game objects
        road_center_x = (SCREEN_WIDTH - ROAD_WIDTH) // 2 + (ROAD_WIDTH // 2) - (PLAYER_WIDTH // 2)
        self.player = Player(road_center_x, SCREEN_HEIGHT - PLAYER_HEIGHT - 20, 
                           self.asset_manager.assets["player"])
        
        self.road = Road()
        self.sky = Sky(self.asset_manager.assets["cloud"])
        
        # Create grass on both sides of the road
        self.left_grass = Grass(self.asset_manager.assets["grass"], "left")
        self.right_grass = Grass(self.asset_manager.assets["grass"], "right")
        
        # Create highway boards
        self.highway_boards = HighwayBoard(self.asset_manager.assets["highway_board"])
        
        # Create enemies and obstacles
        self.enemies = [Enemy(self.asset_manager.assets["enemy"]) for _ in range(3)]
        self.obstacles = [Obstacle(self.asset_manager.assets["obstacle"]) for _ in range(5)]
    
    def handle_events(self):
        """Handle game events like keyboard input"""
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                elif event.key == K_RETURN and self.game_over:
                    self.reset_game()
        
        # Handle continuous key presses for movement
        if not self.game_over:
            keys = pygame.key.get_pressed()
            if keys[K_LEFT]:
                self.player.move(-5, 0)
            if keys[K_RIGHT]:
                self.player.move(5, 0)
            if keys[K_UP]:
                self.player.move(0, -5)
                self.player.increase_speed()
            if keys[K_DOWN]:
                self.player.move(0, 5)
    
    def update(self):
        """Update game state"""
        if self.game_over:
            return
        
        # Update sky
        self.sky.update()
        
        # Update road
        self.road.update(self.player.speed)
        
        # Update grass
        self.left_grass.update(self.player.speed)
        self.right_grass.update(self.player.speed)
        
        # Update highway boards
        self.highway_boards.update(self.player.speed)
        
        # Update enemies
        for enemy in self.enemies:
            enemy.update(self.player.speed, self.player)
            
            # Check for collision with player
            if enemy.get_rect().colliderect(self.player.get_rect()):
                self.game_over = True
        
        # Update obstacles
        for obstacle in self.obstacles:
            obstacle.update(self.player.speed)
            
            # Check for collision with player
            if obstacle.get_rect().colliderect(self.player.get_rect()):
                self.game_over = True
        
        # Update score based on speed
        if not self.game_over:
            self.player.update_score(int(self.player.speed / 10))
    
    def draw(self):
        """Draw game elements on screen"""
        # Fill background with sky blue
        self.screen.fill(SKY_BLUE)
        
        # Draw sky and clouds
        self.sky.draw(self.screen)
        
        # Draw grass
        self.left_grass.draw(self.screen)
        self.right_grass.draw(self.screen)
        
        # Draw highway boards
        self.highway_boards.draw(self.screen)
        
        # Draw road
        self.road.draw(self.screen)
        
        # Draw player
        self.player.draw(self.screen)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        # Draw obstacles
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        
        # Draw score and speed
        score_text = self.font.render(f"Score: {self.player.score}", True, BLACK)
        speed_text = self.font.render(f"Speed: {int(self.player.speed)}", True, BLACK)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(speed_text, (10, 50))
        
        # Draw game over message if game is over
        if self.game_over:
            game_over_text = self.font.render("GAME OVER! Press ENTER to restart", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(game_over_text, text_rect)
        
        # Update display
        pygame.display.flip()
    
    def reset_game(self):
        """Reset the game state"""
        self.game_over = False
        
        # Reset player
        road_center_x = (SCREEN_WIDTH - ROAD_WIDTH) // 2 + (ROAD_WIDTH // 2) - (PLAYER_WIDTH // 2)
        self.player.x = road_center_x
        self.player.y = SCREEN_HEIGHT - PLAYER_HEIGHT - 20
        self.player.speed = ROAD_SPEED
        self.player.score = 0
        
        # Reset enemies and obstacles
        for enemy in self.enemies:
            enemy.reset()
        
        for obstacle in self.obstacles:
            obstacle.reset()
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()

if __name__ == "__main__":
    print("Starting Road Rash Game with updated features...")
    game = Game()
    game.run()