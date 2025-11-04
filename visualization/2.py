from manim import *
import random

class PigeonholePrinciple(Scene):
    def construct(self):
        # === Title ===
        title = Text("Pigeonhole Principle and Combinatorial Bound", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # === Create central vertex ===
        center = Dot(ORIGIN, color=WHITE)
        self.play(FadeIn(center))
        self.wait(0.5)

        # === Create outer vertices ===
        n = 8  # number of outer vertices
        radius = 3
        outer_vertices = [
            Dot(radius * np.array([np.cos(theta), np.sin(theta), 0]), color=WHITE)
            for theta in np.linspace(0, 2 * PI, n, endpoint=False)
        ]

        self.play(*[FadeIn(v) for v in outer_vertices])
        self.wait(0.5)

        # === Connect edges (randomly colored red/blue) ===
        colors = [RED, BLUE]
        edges = []
        for v in outer_vertices:
            color = random.choice(colors)
            edge = Line(center.get_center(), v.get_center(), color=color, stroke_width=4)
            edges.append(edge)

        self.play(*[Create(e) for e in edges])
        self.wait(0.5)

        # === Highlight Pigeonhole group (majority color) ===
        # Count colors
        red_edges = [e for e in edges if e.get_color() == RED]
        blue_edges = [e for e in edges if e.get_color() == BLUE]

        majority_edges = red_edges if len(red_edges) >= len(blue_edges) else blue_edges
        majority_color = majority_edges[0].get_color()

        # Emphasize that color group
        glow = [edge.copy().set_stroke(width=10, opacity=0.4) for edge in majority_edges]
        self.play(*[edge.animate.set_stroke(width=6) for edge in majority_edges])
        self.play(*[FadeIn(g, shift=IN, scale=1.2) for g in glow], run_time=1.5)
        self.wait(0.5)

        # === Add explanatory text ===
        text = MathTex(r"\text{At least } \lceil n/2 \rceil \text{ edges share one color}", color=YELLOW)
        text.next_to(title, DOWN)
        self.play(Write(text))
        self.wait(1)

        # === Show the "subset" forming (connect endpoints of same color) ===
        subset_edges = []
        subset_vertices = [outer_vertices[edges.index(e)] for e in majority_edges[:3]]  # pick first 3
        for i in range(len(subset_vertices)):
            for j in range(i + 1, len(subset_vertices)):
                subset_edges.append(Line(subset_vertices[i].get_center(),
                                         subset_vertices[j].get_center(),
                                         color=majority_color, stroke_width=4))

        # Highlight subset
        self.play(*[Create(e) for e in subset_edges])
        self.wait(0.5)

        subset_glow = VGroup(*subset_vertices)
        self.play(subset_glow.animate.set_color(YELLOW).scale(1.2))
        self.wait(1)

        # === Show formula overlay ===
        bound = MathTex(r"\#\text{edges per color} \ge \frac{n}{2} \implies \text{monochromatic subset exists}", color=WHITE)
        bound.scale(0.7)
        bound.to_edge(DOWN)
        self.play(Write(bound))
        self.wait(2)

        # === Fade out to next topic ===
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=1.5
        )

