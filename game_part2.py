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