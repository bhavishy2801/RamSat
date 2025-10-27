from manim import *
import random

class ErdosProbabilistic(Scene):
    def construct(self):
        title = Text("Erdős Probabilistic Method").scale(0.9)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # Create points for K6
        n = 6
        points = [Dot(3 * np.array([np.cos(2 * np.pi * i / n),
                                    np.sin(2 * np.pi * i / n), 0]),
                                    color=WHITE) for i in range(n)]
        self.play(*[FadeIn(p) for p in points])

        edges = []
        for i in range(n):
            for j in range(i+1, n):
                color = random.choice([RED, BLUE])
                line = Line(points[i].get_center(), points[j].get_center(),
                            color=color, stroke_width=3)
                edges.append(line)
                self.add(line)
                self.wait(0.05)

        self.wait(1)
        self.play(LaggedStart(*[line.animate.set_opacity(0.2) for line in edges],
                              lag_ratio=0.05))
        txt = Text("Expected count of colorings avoiding monochromatic K₃ ↓").scale(0.6).to_edge(DOWN)
        self.play(Write(txt))
        self.wait(2)

        # Probability curve
        axes = Axes(x_range=[0, 6, 1], y_range=[0, 1, 0.2],
                    x_length=5, y_length=3,
                    axis_config={"include_numbers": True}).to_edge(DOWN)
        label_x = axes.get_x_axis_label("n")
        label_y = axes.get_y_axis_label("P(no mono-K₃)")
        graph = axes.plot(lambda x: np.exp(-0.4*x), color=YELLOW)
        self.play(Create(axes), Write(label_x), Write(label_y))
        self.play(Create(graph))
        self.wait(2)
