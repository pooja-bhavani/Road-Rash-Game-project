import boto3
import sys
import os

def create_bucket(bucket_name="road-rash-game-assets", region="us-east-1"):
    """
    Create an S3 bucket for storing game assets
    """
    try:
        s3_client = boto3.client('s3', region_name=region)
        
        # Create the bucket
        if region == "us-east-1":
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            location = {'LocationConstraint': region}
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration=location
            )
        
        print(f"Successfully created bucket: {bucket_name}")
        return True
    except Exception as e:
        print(f"Error creating bucket: {e}")
        return False

def upload_default_assets(bucket_name="road-rash-game-assets"):
    """
    Create and upload default assets to S3
    """
    try:
        import pygame
        pygame.init()
        
        # Create assets directory if it doesn't exist
        if not os.path.exists("assets"):
            os.makedirs("assets")
        
        # Create default assets
        assets = {
            "player.png": (50, 100, (255, 0, 0)),      # Red player
            "enemy.png": (50, 100, (0, 0, 0)),         # Black enemy
            "obstacle.png": (30, 30, (255, 255, 255))  # White obstacle
        }
        
        s3_client = boto3.client('s3')
        
        for asset_name, (width, height, color) in assets.items():
            # Create surface and save as PNG
            surface = pygame.Surface((width, height))
            surface.fill(color)
            asset_path = os.path.join("assets", asset_name)
            pygame.image.save(surface, asset_path)
            
            # Upload to S3
            s3_client.upload_file(asset_path, bucket_name, asset_name)
            print(f"Uploaded {asset_name} to S3 bucket {bucket_name}")
        
        return True
    except Exception as e:
        print(f"Error uploading assets: {e}")
        return False

if __name__ == "__main__":
    bucket_name = "road-rash-game-assets"
    region = "us-east-1"
    
    # Allow custom bucket name from command line
    if len(sys.argv) > 1:
        bucket_name = sys.argv[1]
    
    # Allow custom region from command line
    if len(sys.argv) > 2:
        region = sys.argv[2]
    
    if create_bucket(bucket_name, region):
        upload_default_assets(bucket_name)
        print(f"\nS3 bucket setup complete. The game will now use assets from: {bucket_name}")
        print("You can customize the assets by uploading your own versions of:")
        print("- player.png")
        print("- enemy.png")
        print("- obstacle.png")
    else:
        print("\nFailed to set up S3 bucket. The game will use default generated assets.")