#!/usr/bin/env python3
"""
Direct launcher for the Road Rash style game.
This script runs the game directly without requiring the shell script.
"""

import sys
import os
import subprocess

def main():
    """Run the game directly"""
    print("Starting Road Rash Game...")
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Change to the script directory
    os.chdir(script_dir)
    
    # Run the game
    try:
        import game
        game_instance = game.Game()
        game_instance.run()
    except ImportError as e:
        print(f"Error importing game module: {e}")
        print("Make sure pygame and boto3 are installed.")
        print("Try running: pip install pygame boto3")
        sys.exit(1)
    except Exception as e:
        print(f"Error running game: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()