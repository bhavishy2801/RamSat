from manim import *
import numpy as np
import random

class RamseyGraphEvolutionAdvanced(Scene):
    def construct(self):
        title = Text("Evolution of Ramsey Graphs", font="Helvetica", weight=BOLD).scale(0.9)
        subtitle = Text("Visualizing Random Edge Colorings and Emergent Patterns", font="Helvetica").scale(0.5)
        subtitle.next_to(title, DOWN)
        self.play(Write(title), FadeIn(subtitle))
        self.wait(1)
        self.play(title.animate.to_edge(UP), FadeOut(subtitle))
        
        n = 6
        radius = 3
        points = [
            Dot(radius * np.array([np.cos(2 * np.pi * i / n), np.sin(2 * np.pi * i / n), 0]), color=WHITE)
            for i in range(n)
        ]
        point_labels = [
            Text(str(i + 1), font="Consolas").scale(0.4).next_to(points[i], np.sign(points[i].get_center()))
            for i in range(n)
        ]

        # Show initial graph structure
        self.play(LaggedStart(*[FadeIn(p) for p in points], lag_ratio=0.15))
        self.play(LaggedStart(*[FadeIn(l) for l in point_labels], lag_ratio=0.1))
        self.wait(0.5)

        all_edges = [(i, j) for i in range(n) for j in range(i + 1, n)]

        # Create an initial neutral (grey) graph
        lines = {}
        for i, j in all_edges:
            line = Line(points[i].get_center(), points[j].get_center(), color=GREY, stroke_width=2.5)
            lines[(i, j)] = line
        self.play(LaggedStart(*[Create(line) for line in lines.values()], lag_ratio=0.05))
        self.wait(0.5)

        # Animate random coloring evolution
        color_text = Text("Random Edge Coloring", font="Helvetica", color=YELLOW).scale(0.5)
        color_text.to_edge(DOWN)
        self.play(FadeIn(color_text))
        for step in range(3):
            animations = []
            for (i, j), line in lines.items():
                new_color = random.choice([RED, BLUE])
                animations.append(line.animate.set_color(new_color))
            self.play(*animations, run_time=1)
            self.wait(0.7)

        self.play(FadeOut(color_text))

        # Highlight a monochromatic triangle pattern
        highlight_text = Text("Detecting Monochromatic Triangles", color=GREEN).scale(0.5)
        highlight_text.to_edge(DOWN)
        self.play(FadeIn(highlight_text))

        # Choose triangle (0, 2, 4) for demo
        tri_nodes = [0, 2, 4]
        tri_edges = [(0, 2), (2, 4), (0, 4)]
        tri_color = lines[tri_edges[0]].get_color()

        triangle_lines = VGroup(*[lines[e] for e in tri_edges])
        circle = Circle(radius=1.5, color=YELLOW, stroke_width=3).move_to(
            sum([points[i].get_center() for i in tri_nodes]) / 3
        )
        self.play(
            Flash(points[0], color=YELLOW, flash_radius=0.6),
            Flash(points[2], color=YELLOW, flash_radius=0.6),
            Flash(points[4], color=YELLOW, flash_radius=0.6),
        )
        self.play(Create(circle), run_time=1)
        self.wait(1.5)

        # Add zoom-out with graph rearrangement
        self.play(FadeOut(highlight_text))
        self.play(
            *[p.animate.move_to(1.5 * p.get_center()) for p in points],
            FadeOut(circle),
            *[l.animate.set_stroke(width=1.5, opacity=0.7) for l in lines.values()],
            title.animate.scale(0.7).to_corner(UL),
            run_time=2
        )
        self.wait(0.5)

        # Animated color oscillations — edges "flip" color
        flip_text = Text("Color Evolution Simulation", color=BLUE).scale(0.5)
        flip_text.to_edge(DOWN)
        self.play(FadeIn(flip_text))

        for frame in range(5):
            flip_anims = []
            for (i, j), line in lines.items():
                current = line.get_color()
                next_color = BLUE if current == RED else RED
                flip_anims.append(line.animate.set_color(next_color))
            self.play(*flip_anims, run_time=0.5)
        self.wait(1)
        self.play(FadeOut(flip_text))

        # Show final stabilization
        final_text = Text("Emergent Stable Pattern (Ramsey Structure)", font="Helvetica", color=YELLOW).scale(0.55)
        final_text.to_edge(DOWN)
        self.play(FadeIn(final_text))

        self.wait(2)
        self.play(FadeOut(final_text), FadeOut(title), *[FadeOut(mobj) for mobj in points + point_labels + list(lines.values())])
        self.wait(0.5)
