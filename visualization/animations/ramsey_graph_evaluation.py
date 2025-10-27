from manim import *
import random

class RamseyGraphEvolution(Scene):
    def construct(self):
        title = Text("Evolution of Ramsey Graphs").scale(0.9)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        n = 5
        points = [Dot(2.5 * np.array([np.cos(2*np.pi*i/n), np.sin(2*np.pi*i/n), 0]), color=WHITE) for i in range(n)]
        self.play(*[FadeIn(p) for p in points])

        all_edges = [(i, j) for i in range(n) for j in range(i+1, n)]
        lines = []
        for i, j in all_edges:
            color = random.choice([RED, BLUE])
            line = Line(points[i].get_center(), points[j].get_center(), color=color, stroke_width=3)
            lines.append(line)
            self.play(Create(line), run_time=0.05)

        self.wait(1)
        # Highlight pattern (monochromatic triangle)
        triangle = VGroup(
            *[l for l in lines if {all_edges.index((i, j)) for i,j in [(0,1),(1,2),(0,2)]}]
        )
        highlight = Circle(radius=1.3, color=YELLOW).move_to(points[1].get_center())
        self.play(Create(highlight), run_time=1)
        self.wait(2)
