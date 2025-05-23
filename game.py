import pygame
import random
import os
import sys
import boto3
from pygame.locals import *

# Initialize pygame
pygame.init()

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
ROAD_SPEED = 5
ENEMY_SPEED = 3
OBSTACLE_SPEED = 4
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
    """
    Manages game assets including downloading from S3 when needed
    """
    def __init__(self, bucket_name="road-rash-game-assets"):
        self.bucket_name = bucket_name
        self.assets_dir = "assets"
        self.ensure_assets_dir()
        
        # Default assets if S3 download fails
        self.default_assets = {
            "player": self.create_default_player(),
            "enemy": self.create_default_enemy(),
            "obstacle": self.create_default_obstacle(),
            "cloud": self.create_default_cloud(),
            "grass": self.create_default_grass(),
            "highway_board": self.create_default_highway_board()
        }
        
        # Try to download assets from S3
        self.assets = self.load_assets()
    
    def ensure_assets_dir(self):
        """Create assets directory if it doesn't exist"""
        if not os.path.exists(self.assets_dir):
            os.makedirs(self.assets_dir)
    
    def create_default_player(self):
        """Create a default player sprite if asset download fails"""
        surface = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT), pygame.SRCALPHA)
        
        # Bike body (pink) - facing upward
        bike_color = (255, 105, 180)  # Pink
        pygame.draw.polygon(surface, bike_color, [(15, 60), (35, 60), (25, 40)])
        pygame.draw.rect(surface, bike_color, (20, 60, 10, 30))
        
        # Wheels - vertically aligned
        wheel_color = (30, 30, 30)  # Dark gray
        pygame.draw.circle(surface, wheel_color, (25, 70), 6)  # Middle wheel
        pygame.draw.circle(surface, wheel_color, (25, 90), 6)  # Back wheel
        
        # Headlight (red) - at the front (top) of the bike
        headlight_color = (255, 0, 0)  # Red
        pygame.draw.circle(surface, headlight_color, (25, 40), 4)
        
        # Rider body
        body_color = (255, 215, 0)  # Golden shirt
        pygame.draw.ellipse(surface, body_color, (15, 50, 20, 25))
        
        # Rider legs
        leg_color = (255, 192, 203)  # Pink pants
        pygame.draw.rect(surface, leg_color, (18, 70, 6, 20))
        pygame.draw.rect(surface, leg_color, (26, 70, 6, 20))
        
        # Helmet
        helmet_color = (255, 255, 0)  # Yellow
        pygame.draw.circle(surface, helmet_color, (25, 30), 10)
        
        return surface
    
    def create_default_enemy(self):
        """Create a default enemy sprite if asset download fails"""
        surface = pygame.Surface((ENEMY_WIDTH, ENEMY_HEIGHT), pygame.SRCALPHA)
        
        # Bike body (green) - facing upward
        bike_color = (0, 128, 0)  # Green
        pygame.draw.polygon(surface, bike_color, [(15, 60), (35, 60), (25, 40)])
        pygame.draw.rect(surface, bike_color, (20, 60, 10, 30))
        
        # Wheels - vertically aligned
        wheel_color = (30, 30, 30)  # Dark gray
        pygame.draw.circle(surface, wheel_color, (25, 70), 6)  # Middle wheel
        pygame.draw.circle(surface, wheel_color, (25, 90), 6)  # Back wheel
        
        # Headlight (red) - at the front (top) of the bike
        headlight_color = (255, 0, 0)  # Red
        pygame.draw.circle(surface, headlight_color, (25, 40), 4)
        
        # Rider body
        body_color = (50, 50, 150)  # Blue shirt
        pygame.draw.ellipse(surface, body_color, (15, 50, 20, 25))
        
        # Rider legs
        leg_color = (50, 50, 50)  # Dark pants
        pygame.draw.rect(surface, leg_color, (18, 70, 6, 20))
        pygame.draw.rect(surface, leg_color, (26, 70, 6, 20))
        
        # Helmet
        helmet_color = (150, 0, 0)  # Red
        pygame.draw.circle(surface, helmet_color, (25, 30), 10)
        
        return surface
    
    def create_default_obstacle(self):
        """Create a default obstacle sprite if asset download fails"""
        surface = pygame.Surface((OBSTACLE_WIDTH, OBSTACLE_HEIGHT), pygame.SRCALPHA)
        
        # Draw a rock/barrier
        obstacle_color = (100, 100, 100)  # Gray
        pygame.draw.polygon(surface, obstacle_color, 
                           [(5, 25), (10, 5), (20, 5), (25, 25)])
        
        # Add some detail
        detail_color = (70, 70, 70)  # Darker gray
        pygame.draw.line(surface, detail_color, (10, 15), (20, 15), 2)
        
        return surface
    
    def create_default_cloud(self):
        """Create a default cloud sprite if asset download fails"""
        surface = pygame.Surface((CLOUD_WIDTH, CLOUD_HEIGHT), pygame.SRCALPHA)
        
        # Create a cloud shape
        cloud_color = (255, 255, 255)  # White
        pygame.draw.ellipse(surface, cloud_color, (0, 10, 40, 30))
        pygame.draw.ellipse(surface, cloud_color, (20, 0, 50, 25))
        pygame.draw.ellipse(surface, cloud_color, (30, 10, 40, 30))
        
        return surface
    
    def create_default_grass(self):
        """Create default grass sprite if asset download fails"""
        surface = pygame.Surface((GRASS_WIDTH, GRASS_HEIGHT), pygame.SRCALPHA)
        
        # Base grass color
        grass_color = (34, 139, 34)  # Forest green
        
        # Draw several blades of grass
        for i in range(15):
            x = random.randint(0, GRASS_WIDTH)
            h = random.randint(10, 25)
            w = random.randint(2, 4)
            pygame.draw.line(surface, grass_color, (x, GRASS_HEIGHT), (x, GRASS_HEIGHT - h), w)
        
        # Add some variation in color
        light_grass = (85, 170, 85)
        for i in range(5):
            x = random.randint(0, GRASS_WIDTH)
            h = random.randint(8, 20)
            w = random.randint(1, 3)
            pygame.draw.line(surface, light_grass, (x, GRASS_HEIGHT), (x, GRASS_HEIGHT - h), w)
        
        return surface
    
    def create_default_highway_board(self):
        """Create default highway board sprite if asset download fails"""
        surface = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT), pygame.SRCALPHA)
        
        # Draw pole
        pole_color = (100, 100, 100)  # Gray
        pygame.draw.rect(surface, pole_color, (BOARD_WIDTH//2 - 3, BOARD_HEIGHT//3, 6, 2*BOARD_HEIGHT//3))
        
        # Draw sign
        sign_color = (0, 0, 150)  # Blue
        pygame.draw.rect(surface, sign_color, (5, 5, BOARD_WIDTH - 10, BOARD_HEIGHT//3))
        
        # Add white border
        border_color = (255, 255, 255)  # White
        pygame.draw.rect(surface, border_color, (5, 5, BOARD_WIDTH - 10, BOARD_HEIGHT//3), 2)
        
        # Add some text-like markings
        text_color = (255, 255, 255)  # White
        pygame.draw.line(surface, text_color, (15, 15), (BOARD_WIDTH - 15, 15), 3)
        pygame.draw.line(surface, text_color, (15, 25), (BOARD_WIDTH - 25, 25), 3)
        
        return surface
    
    def download_from_s3(self):
        """
        Download assets from S3 bucket
        Returns True if successful, False otherwise
        """
        try:
            s3 = boto3.client('s3')
            
            # List of assets to download
            assets = ["player.png", "enemy.png", "obstacle.png", "cloud.png", 
                     "grass.png", "highway_board.png"]
            
            for asset in assets:
                s3.download_file(
                    self.bucket_name,
                    asset,
                    os.path.join(self.assets_dir, asset)
                )
            return True
        except Exception as e:
            print(f"Failed to download assets from S3: {e}")
            return False
    
    def load_assets(self):
        """Load game assets, first trying S3 then falling back to defaults"""
        assets = {}
        
        # Try to download from S3
        s3_success = self.download_from_s3()
        
        if s3_success:
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
        
        # Fall back to default assets
        return self.default_assets