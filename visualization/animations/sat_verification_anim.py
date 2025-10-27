import random
from manim import *

class SATVerifier(Scene):
    def construct(self):
        title = Text("SAT-Based Edge Coloring Verification").scale(0.9)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # Formula visualization
        formula = MathTex(r"(\neg x_{12} \lor x_{23} \lor \neg x_{13}) \land (\neg x_{12} \lor x_{24}) \land \cdots").scale(0.8)
        self.play(Write(formula))
        self.wait(1)

        # Represent variables as edges in K4
        vertices = [Dot(2 * np.array([np.cos(2*np.pi*i/4), np.sin(2*np.pi*i/4), 0]), color=WHITE) for i in range(4)]
        for v in vertices: self.add(v)

        edges = []
        for i in range(4):
            for j in range(i+1, 4):
                line = Line(vertices[i].get_center(), vertices[j].get_center(), color=GRAY, stroke_width=3)
                edges.append(line)
                self.add(line)

        self.wait(0.5)

        # Highlight satisfying assignment
        satisfying = random.sample(edges, 3)
        self.play(*[edge.animate.set_color(RED) for edge in satisfying])
        self.wait(1)
        self.play(*[edge.animate.set_color(BLUE) for edge in edges if edge not in satisfying])
        self.wait(1)

        result = Text("SAT solved → Valid 2-coloring found!").next_to(formula, DOWN).scale(0.7)
        self.play(Write(result))
        self.wait(2)
