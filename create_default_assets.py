import pygame
import os
import random

def create_default_assets():
    """
    Create default game assets in the assets directory
    """
    pygame.init()
    
    # Create assets directory if it doesn't exist
    if not os.path.exists("assets"):
        os.makedirs("assets")
    
    # Create player bike with rider
    create_player_bike()
    
    # Create enemy bike with rider
    create_enemy_bike()
    
    # Create obstacle
    create_obstacle()
    
    # Create cloud
    create_cloud()
    
    # Create grass
    create_grass()
    
    # Create highway board
    create_highway_board()

def create_player_bike():
    """Create a sports bike with rider in sports dress"""
    width, height = 50, 100
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
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
    
    # Rider body - more human-like shape
    body_color = (255, 215, 0)  # Golden shirt
    # Torso
    pygame.draw.rect(surface, body_color, (18, 35, 14, 20))
    # Arms
    pygame.draw.rect(surface, body_color, (14, 40, 4, 15))
    pygame.draw.rect(surface, body_color, (32, 40, 4, 15))
    
    # Rider legs - positioned lower on the bike
    leg_color = (255, 192, 203)  # Pink pants
    pygame.draw.rect(surface, leg_color, (18, 55, 6, 25))
    pygame.draw.rect(surface, leg_color, (26, 55, 6, 25))
    
    # Helmet
    helmet_color = (255, 255, 0)  # Yellow
    pygame.draw.circle(surface, helmet_color, (25, 25), 8)
    # Face area
    face_color = (255, 213, 170)  # Skin tone
    pygame.draw.rect(surface, face_color, (21, 22, 8, 8))
    
    # Save the image
    asset_path = os.path.join("assets", "player.png")
    pygame.image.save(surface, asset_path)
    print(f"Created {asset_path}")

def create_enemy_bike():
    """Create an enemy bike with rider"""
    width, height = 50, 100
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
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
    
    # Rider body - more human-like shape
    body_color = (50, 50, 150)  # Blue shirt
    # Torso
    pygame.draw.rect(surface, body_color, (18, 35, 14, 20))
    # Arms
    pygame.draw.rect(surface, body_color, (14, 40, 4, 15))
    pygame.draw.rect(surface, body_color, (32, 40, 4, 15))
    
    # Rider legs - positioned lower on the bike
    leg_color = (50, 50, 50)  # Dark pants
    pygame.draw.rect(surface, leg_color, (18, 55, 6, 25))
    pygame.draw.rect(surface, leg_color, (26, 55, 6, 25))
    
    # Helmet
    helmet_color = (150, 0, 0)  # Red
    pygame.draw.circle(surface, helmet_color, (25, 25), 8)
    # Face area
    face_color = (255, 213, 170)  # Skin tone
    pygame.draw.rect(surface, face_color, (21, 22, 8, 8))
    
    # Save the image
    asset_path = os.path.join("assets", "enemy.png")
    pygame.image.save(surface, asset_path)
    print(f"Created {asset_path}")

def create_obstacle():
    """Create an obstacle"""
    width, height = 30, 30
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Draw a rock/barrier
    obstacle_color = (100, 100, 100)  # Gray
    pygame.draw.polygon(surface, obstacle_color, 
                       [(5, 25), (10, 5), (20, 5), (25, 25)])
    
    # Add some detail
    detail_color = (70, 70, 70)  # Darker gray
    pygame.draw.line(surface, detail_color, (10, 15), (20, 15), 2)
    
    # Save the image
    asset_path = os.path.join("assets", "obstacle.png")
    pygame.image.save(surface, asset_path)
    print(f"Created {asset_path}")

def create_cloud():
    """Create a cloud"""
    width, height = 80, 40
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Create a cloud shape
    cloud_color = (255, 255, 255)  # White
    pygame.draw.ellipse(surface, cloud_color, (0, 10, 40, 30))
    pygame.draw.ellipse(surface, cloud_color, (20, 0, 50, 25))
    pygame.draw.ellipse(surface, cloud_color, (30, 10, 40, 30))
    
    # Save the image
    asset_path = os.path.join("assets", "cloud.png")
    pygame.image.save(surface, asset_path)
    print(f"Created {asset_path}")

def create_grass():
    """Create grass for roadside"""
    width, height = 40, 30
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Base grass color
    grass_color = (34, 139, 34)  # Forest green
    
    # Draw several blades of grass
    for i in range(15):
        x = random.randint(0, width)
        h = random.randint(10, 25)
        w = random.randint(2, 4)
        pygame.draw.line(surface, grass_color, (x, height), (x, height - h), w)
    
    # Add some variation in color
    light_grass = (85, 170, 85)
    for i in range(5):
        x = random.randint(0, width)
        h = random.randint(8, 20)
        w = random.randint(1, 3)
        pygame.draw.line(surface, light_grass, (x, height), (x, height - h), w)
    
    # Save the image
    asset_path = os.path.join("assets", "grass.png")
    pygame.image.save(surface, asset_path)
    print(f"Created {asset_path}")

def create_highway_board():
    """Create highway board"""
    width, height = 60, 80
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Draw pole
    pole_color = (100, 100, 100)  # Gray
    pygame.draw.rect(surface, pole_color, (width//2 - 3, height//3, 6, 2*height//3))
    
    # Draw sign
    sign_color = (0, 0, 150)  # Blue
    pygame.draw.rect(surface, sign_color, (5, 5, width - 10, height//3))
    
    # Add white border
    border_color = (255, 255, 255)  # White
    pygame.draw.rect(surface, border_color, (5, 5, width - 10, height//3), 2)
    
    # Add some text-like markings
    text_color = (255, 255, 255)  # White
    pygame.draw.line(surface, text_color, (15, 15), (width - 15, 15), 3)
    pygame.draw.line(surface, text_color, (15, 25), (width - 25, 25), 3)
    
    # Save the image
    asset_path = os.path.join("assets", "highway_board.png")
    pygame.image.save(surface, asset_path)
    print(f"Created {asset_path}")

if __name__ == "__main__":
    create_default_assets()
    print("\nDefault assets created successfully.")
    print("You can replace these with custom assets in the assets directory.")