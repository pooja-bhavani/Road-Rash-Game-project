# Road Rash Style Game

A simple 2D Road Rash-style bike racing game built with Python and Pygame.
![image](https://github.com/user-attachments/assets/1e252ce6-5253-49f7-9c36-6ba3d08d3a44)
![image](https://github.com/user-attachments/assets/37b353db-b866-4db3-8e74-9a4487b2a946)

<img width="1470" alt="Screenshot 2025-05-22 at 6 55 32 PM" src="https://github.com/user-attachments/assets/8d7188b3-fc9b-43ae-b4dc-1622b1a4b54d" />


## Features

- Control a bike with keyboard arrow keys
- Avoid enemy bikers and obstacles
- Track score and speed
- Game over condition on collision
- Sky-blue background with scrolling road animation
- Integration with Amazon S3 for game assets

## Requirements

- Python 3.6+
- Pygame
- Boto3 (for AWS S3 integration)

## How to Play

1. Make sure you have Python 3 installed
2. Run the game using the provided script:
   ```
   chmod +x run_game.sh
   ./run_game.sh
   ```

3. Use arrow keys to control your bike:
   - Up: Accelerate
   - Down: Decelerate
   - Left/Right: Move sideways

4. Avoid collisions with enemy bikers and obstacles
5. Your score increases as you maintain higher speeds

## AWS S3 Integration

The game attempts to download assets from an S3 bucket. If the download fails, it will use default generated assets.

To use your own S3 bucket:
1. Create an S3 bucket and upload the following assets:
   - player.png
   - enemy.png
   - obstacle.png
2. Configure AWS credentials using AWS CLI or environment variables
3. Update the bucket name in the AssetManager class if needed

## Architecture

The game follows a simple object-oriented architecture:
- `Game`: Main game loop and state management
- `Player`: Player bike control and scoring
- `Enemy`: Enemy bikers that move down the road
- `Obstacle`: Road obstacles to avoid
- `Road`: Handles road rendering and scrolling animation
- `AssetManager`: Manages game assets and S3 integration
