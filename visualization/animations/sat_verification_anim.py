from manim import *

class SATVerifier(Scene):
    def construct(self):
        title = Text("SAT-Based Ramsey Verification").scale(0.8)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        formula = Tex(r"(\neg x_{12} \lor x_{23} \lor \neg x_{13}) \land \cdots").scale(0.8)
        self.play(Write(formula))
        self.wait(1)

        solving = Text("Solving with PySAT / Z3...").scale(0.7).next_to(formula, DOWN)
        self.play(Write(solving))
        self.wait(1)

        result = Text("Result: R(3,3) = 6 ✅", color=GREEN).scale(0.9).next_to(solving, DOWN)
        self.play(Transform(solving, result))
        self.wait(2)
