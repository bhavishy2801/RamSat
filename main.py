# main.py
import os
import argparse

# Create the parser
parser = argparse.ArgumentParser(description="Run Manim animations")
parser.add_argument("--mode", type=str, required=True, help="Mode of execution (e.g., 'animate')")
parser.add_argument("--scene", type=str, required=True, help="Scene name (without .py)")

# Parse the command-line arguments
args = parser.parse_args()

# Run animation if mode is animate
if args.mode == "animate":
    os.system(f"manim -pqh visualization/animations/{args.scene}.py {args.scene}")
