class Game:
    """Main game class"""
    def __init__(self):
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