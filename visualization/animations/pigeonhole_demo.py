from manim import *

class PigeonholeBound(Scene):
    def construct(self):
        title = Text("Pigeonhole Principle Bound for R(3,3)").scale(0.8)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        eq = MathTex(r"R(3,3) \leq 7").scale(1.5)
        self.play(Write(eq))
        self.wait(2)

        explain = Tex(
            "With 6 vertices, some colorings avoid monochromatic triangles. "
            "But with 7 vertices, it's impossible!"
        ).scale(0.6).next_to(eq, DOWN)
        self.play(FadeIn(explain, shift=UP))
        self.wait(2)
