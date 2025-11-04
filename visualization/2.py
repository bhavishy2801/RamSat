from manim import *
import random

class PigeonholePrinciple(Scene):
    def construct(self):
        # === Title ===
        title = Text("Pigeonhole Principle and Combinatorial Bound", font_size=36, color=YELLOW)
        title.to_edge(UP)
        self.play(FadeIn(title, shift=UP), run_time=1.2)
        self.wait(0.3)

        # === Center vertex ===
        center = Dot(ORIGIN, color=WHITE)
        center_label = MathTex("v_0", color=WHITE).scale(0.7).next_to(center, DOWN)
        self.play(FadeIn(center), Write(center_label))
        self.wait(0.3)

        # === Outer vertices setup ===
        n = 8
        radius = 3
        outer_vertices = [
            Dot(radius * np.array([np.cos(theta), np.sin(theta), 0]), color=WHITE)
            for theta in np.linspace(0, 2 * PI, n, endpoint=False)
        ]

        outer_labels = [
            MathTex(f"v_{{{i+1}}}", color=WHITE).scale(0.6).next_to(outer_vertices[i], 
            radius * 0.05 * np.array([np.cos(np.linspace(0, 2 * PI, n, endpoint=False)[i]),
                                      np.sin(np.linspace(0, 2 * PI, n, endpoint=False)[i]), 0]))
            for i in range(n)
        ]

        self.play(
            LaggedStart(*[FadeIn(v) for v in outer_vertices], lag_ratio=0.1),
            run_time=1.2
        )
        self.play(LaggedStart(*[Write(lbl) for lbl in outer_labels], lag_ratio=0.1), run_time=1)
        self.wait(0.5)

        # === Colored edges ===
        colors = [RED, BLUE]
        edges = []
        for v in outer_vertices:
            color = random.choice(colors)
            edge = Line(center.get_center(), v.get_center(), color=color, stroke_width=4)
            edges.append(edge)

        self.play(LaggedStart(*[Create(e) for e in edges], lag_ratio=0.1), run_time=2)
        self.wait(0.5)

        # === Highlight majority color ===
        red_edges = [e for e in edges if e.get_color() == RED]
        blue_edges = [e for e in edges if e.get_color() == BLUE]
        majority_edges = red_edges if len(red_edges) >= len(blue_edges) else blue_edges
        majority_color = majority_edges[0].get_color()

        # Highlight with glow effect
        self.play(
            *[edge.animate.set_stroke(width=6).set_z_index(2) for edge in majority_edges],
            run_time=1
        )
        self.play(
            *[edge.animate.set_opacity(0.8) for edge in majority_edges],
            run_time=0.6
        )

        highlight_text = MathTex(
            r"\text{At least } \lceil n/2 \rceil \text{ edges share one color}",
            color=YELLOW
        ).scale(0.9)
        highlight_text.next_to(title, DOWN, buff=0.6)
        self.play(Write(highlight_text), run_time=1.5)
        self.wait(1)

        # === Form subset (monochromatic triangle) ===
        subset_vertices = [outer_vertices[edges.index(e)] for e in majority_edges[:3]]
        subset_edges = [
            Line(subset_vertices[i].get_center(), subset_vertices[j].get_center(),
                 color=majority_color, stroke_width=5)
            for i in range(len(subset_vertices)) for j in range(i + 1, len(subset_vertices))
        ]

        subset_glow = VGroup(*subset_vertices)
        self.play(
            AnimationGroup(
                *[Create(e) for e in subset_edges],
                subset_glow.animate.set_color(YELLOW).scale(1.2),
                lag_ratio=0.2,
            ),
            run_time=1.5
        )

        subset_text = Text("Monochromatic Subset Found!", color=GREEN, font_size=28)
        subset_text.next_to(highlight_text, DOWN, buff=0.7)
        self.play(FadeIn(subset_text, shift=UP), run_time=1)
        self.wait(1.5)

        # === Mathematical conclusion ===
        bound_eq = MathTex(
            r"\#\text{edges per color} \ge \frac{n}{2} \Rightarrow \text{monochromatic subset exists}",
            color=WHITE
        ).scale(0.8)
        bound_eq.to_edge(DOWN)
        self.play(Write(bound_eq), run_time=1.5)
        self.wait(2)

        # === Cinematic outro ===
        self.play(
            FadeOut(VGroup(*self.mobjects), shift=DOWN),
            run_time=1.5
        )
        self.wait(0.5)
