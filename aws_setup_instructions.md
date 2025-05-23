# AWS S3 Setup Instructions

To fully utilize the S3 integration in the Road Rash game, follow these steps:

## 1. Create an AWS Account

If you don't already have an AWS account:
1. Go to [AWS Console](https://aws.amazon.com/)
2. Click "Create an AWS Account" and follow the instructions

## 2. Set Up AWS CLI

1. Install AWS CLI:
   - For macOS: `brew install awscli` or `pip install awscli`
   - For Windows: Download and run the installer from AWS website
   - For Linux: `pip install awscli` or use your package manager

2. Configure AWS CLI:
   ```
   aws configure
   ```
   
   You'll be prompted to enter:
   - AWS Access Key ID
   - AWS Secret Access Key
   - Default region name (e.g., us-east-1)
   - Default output format (json)

## 3. Create S3 Bucket

You can create the S3 bucket using either:

### Option 1: Using the provided script

```
python create_s3_bucket.py
```

This will:
- Create a bucket named "road-rash-game-assets"
- Generate and upload default assets

### Option 2: Using AWS CLI

```
aws s3 mb s3://road-rash-game-assets
```

## 4. Upload Custom Assets

To use custom assets:

1. Create your own images:
   - player.png (50x100 pixels)
   - enemy.png (50x100 pixels)
   - obstacle.png (30x30 pixels)

2. Upload to S3:
   ```
   aws s3 cp assets/player.png s3://road-rash-game-assets/
   aws s3 cp assets/enemy.png s3://road-rash-game-assets/
   aws s3 cp assets/obstacle.png s3://road-rash-game-assets/
   ```

## 5. Verify Setup

Check that your assets are in the bucket:
```
aws s3 ls s3://road-rash-game-assets/
```

## Note

If you don't set up S3, the game will use locally generated default assets.