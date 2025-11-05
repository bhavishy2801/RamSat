from manim import *
import numpy as np

class PigeonholePrinciple(Scene):
    def construct(self):
        # === Title ===
        title = Text("Pigeonhole Principle and Combinatorial Bound", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # === Central vertex ===
        center = Dot(ORIGIN, color=WHITE)

        # === Outer vertices ===
        n = 8
        radius = 2.2
        outer_vertices = [
            Dot(radius * np.array([np.cos(theta), np.sin(theta), 0]), color=WHITE)
            for theta in np.linspace(0, 2 * PI, n, endpoint=False)
        ]

        # Group figure and shift it higher for better text visibility
        figure_group = VGroup(center, *outer_vertices)
        figure_group.shift(UP * 0.5)

        self.play(FadeIn(center))
        self.play(*[FadeIn(v) for v in outer_vertices])
        self.wait(0.5)

        # === Connect edges (5 red, 3 blue deterministic) ===
        colors = [RED] * 5 + [BLUE] * 3
        edges = []
        for i, v in enumerate(outer_vertices):
            color = colors[i % len(colors)]
            edge = Line(center.get_center(), v.get_center(), color=color, stroke_width=4)
            edges.append(edge)

        self.play(*[Create(e) for e in edges])
        self.wait(0.5)

        # === Highlight majority color (red) ===
        majority_edges = [e for e in edges if e.get_color() == RED]
        majority_color = RED

        glow = [edge.copy().set_stroke(width=10, opacity=0.4) for edge in majority_edges]
        self.play(*[edge.animate.set_stroke(width=6) for edge in majority_edges])
        self.play(*[FadeIn(g, shift=IN, scale=1.2) for g in glow], run_time=1.5)
        self.wait(0.5)

        # === Explanatory Text 1 ===
        text1 = MathTex(
            r"\text{At least } \lceil n/2 \rceil \text{ edges share one color}",
            color=YELLOW
        )
        text1.scale(0.9)
        text1.next_to(figure_group, DOWN, buff=0.7)
        self.play(Write(text1))
        self.wait(1)

        # === Subset edges (connect 3 red vertices among majority color) ===
        red_indices = [i for i, e in enumerate(edges) if e.get_color() == RED]
        subset_vertices = [outer_vertices[i] for i in red_indices[:3]]
        subset_edges = []
        for i in range(len(subset_vertices)):
            for j in range(i + 1, len(subset_vertices)):
                subset_edges.append(Line(
                    subset_vertices[i].get_center(),
                    subset_vertices[j].get_center(),
                    color=majority_color,
                    stroke_width=4
                ))

        self.play(*[Create(e) for e in subset_edges])
        self.wait(0.5)

        subset_glow = VGroup(*subset_vertices)
        self.play(subset_glow.animate.set_color(YELLOW).scale(1.2))
        self.wait(1)

        # === Explanatory Text 2 ===
        text2 = MathTex(
            r"\#\text{edges per color} \ge \frac{n}{2} \implies \text{monochromatic subset exists}",
            color=WHITE
        )
        text2.scale(0.8)
        text2.next_to(text1, DOWN)
        self.play(Write(text2))
        self.wait(2)

        # === Fade out ===
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1.5)
