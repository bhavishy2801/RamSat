import os
import subprocess
import sys

class RamSatAnimationRenderer:
    def __init__(self):
        self.animation_dir = "visualization/animations"
        self.output_dir = "visualization/output"
        self.quality = "high"  # Options: low, medium, high, production
        
        self.animations = {
            "intro": "ramsey_overview_intro.py",
            "pigeonhole": "pigeonhole_demo_anim.py",
            "erdos": "erdos_probabilistic_anim.py",
            "sat": "sat_verification_anim.py",
            "evolution": "ramsey_graph_evolution.py",
            "advanced": "ramsey_graph_evolution_advanced.py"
        }
    
    def render_animation(self, name, quality=None):
        """Render a specific animation by name"""
        if name not in self.animations:
            print(f"Error: Animation '{name}' not found!")
            print(f"Available animations: {', '.join(self.animations.keys())}")
            return False
        
        filename = self.animations[name]
        filepath = os.path.join(self.animation_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"Error: File '{filepath}' not found!")
            return False
        
        quality_flag = quality if quality else self.quality
        quality_map = {
            "low": "-ql",
            "medium": "-qm",
            "high": "-qh",
            "production": "-qk"
        }
        
        q_flag = quality_map.get(quality_flag, "-qh")
        
        print(f"\n{'='*60}")
        print(f"Rendering: {filename}")
        print(f"Quality: {quality_flag}")
        print(f"{'='*60}\n")
        
        cmd = [
            "manim",
            filepath,
            q_flag,
            "-o", f"{name}.mp4"
        ]
        
        try:
            subprocess.run(cmd, check=True)
            print(f"\n✓ Successfully rendered {name}!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"\n✗ Error rendering {name}: {e}")
            return False
    
    def render_all(self, quality=None):
        """Render all animations"""
        print(f"\n{'='*60}")
        print("RENDERING ALL RAMSAT ANIMATIONS")
        print(f"{'='*60}\n")
        
        results = {}
        for name in self.animations.keys():
            results[name] = self.render_animation(name, quality)
        
        print(f"\n{'='*60}")
        print("RENDERING SUMMARY")
        print(f"{'='*60}")
        for name, success in results.items():
            status = "✓ SUCCESS" if success else "✗ FAILED"
            print(f"{name:20s}: {status}")
        
        success_count = sum(results.values())
        total_count = len(results)
        print(f"\nTotal: {success_count}/{total_count} animations rendered successfully")
    
    def preview_animation(self, name):
        """Render and preview a specific animation"""
        if name not in self.animations:
            print(f"Error: Animation '{name}' not found!")
            return
        
        filename = self.animations[name]
        filepath = os.path.join(self.animation_dir, filename)
        
        print(f"\n{'='*60}")
        print(f"Previewing: {filename}")
        print(f"{'='*60}\n")
        
        cmd = ["manim", filepath, "-pql"]
        
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"\n✗ Error previewing {name}: {e}")
    
    def list_animations(self):
        """List all available animations"""
        print(f"\n{'='*60}")
        print("AVAILABLE RAMSAT ANIMATIONS")
        print(f"{'='*60}\n")
        
        for i, (name, filename) in enumerate(self.animations.items(), 1):
            print(f"{i}. {name:15s} -> {filename}")
        print()

def main():
    renderer = RamSatAnimationRenderer()
    
    if len(sys.argv) < 2:
        print("\nRamSat Animation Renderer")
        print("=" * 60)
        print("\nUsage:")
        print("  python main.py list                    - List all animations")
        print("  python main.py render <name> [quality] - Render specific animation")
        print("  python main.py render-all [quality]    - Render all animations")
        print("  python main.py preview <name>          - Preview animation (low quality)")
        print("\nQuality options: low, medium, high, production")
        print("\nExamples:")
        print("  python main.py list")
        print("  python main.py render intro")
        print("  python main.py render erdos high")
        print("  python main.py render-all medium")
        print("  python main.py preview sat")
        renderer.list_animations()
        return
    
    command = sys.argv[1].lower()
    
    if command == "list":
        renderer.list_animations()
    
    elif command == "render":
        if len(sys.argv) < 3:
            print("Error: Please specify animation name")
            renderer.list_animations()
            return
        
        name = sys.argv[2]
        quality = sys.argv[3] if len(sys.argv) > 3 else None
        renderer.render_animation(name, quality)
    
    elif command == "render-all":
        quality = sys.argv[2] if len(sys.argv) > 2 else None
        renderer.render_all(quality)
    
    elif command == "preview":
        if len(sys.argv) < 3:
            print("Error: Please specify animation name")
            renderer.list_animations()
            return
        
        name = sys.argv[2]
        renderer.preview_animation(name)
    
    else:
        print(f"Unknown command: {command}")
        print("Use 'python main.py' for help")

if __name__ == "__main__":
    main()