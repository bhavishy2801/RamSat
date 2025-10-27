from manim import *
import itertools

class RamseyIntro(Scene):
    def construct(self):
        title = Text("Ramsey’s Theorem: Order in Chaos").scale(0.8)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        # Create 6 points in a circle
        points = [Dot(point=3*RIGHT*np.cos(theta) + 3*UP*np.sin(theta)) 
                  for theta in np.linspace(0, 2*np.pi, 6, endpoint=False)]
        group = VGroup(*points)
        self.play(LaggedStartMap(FadeIn, group))
        self.wait(1)

        # Random red/blue edges
        edges = []
        for i, j in itertools.combinations(range(6), 2):
            color = RED if (i + j) % 2 == 0 else BLUE
            edge = Line(points[i].get_center(), points[j].get_center(), color=color)
            edges.append(edge)
        self.play(LaggedStart(*[Create(e) for e in edges], lag_ratio=0.1))
        self.wait(1)

        # Highlight a red triangle (K_3)
        tri = Polygon(points[0].get_center(), points[2].get_center(), points[4].get_center(), color=YELLOW)
        self.play(Create(tri))
        label = Text("Monochromatic Triangle Found!", color=YELLOW).scale(0.6).next_to(tri, DOWN)
        self.play(Write(label))
        self.wait(2)