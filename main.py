# main.py
import os

if args.mode == "animate":
    os.system(f"manim -pqh visualization/animations/{args.scene}.py {args.scene}")