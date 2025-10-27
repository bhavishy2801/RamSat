from manim import *

class RamseyOverviewIntro(Scene):
    def construct(self):
        title = Text("RamSat: A Ramsey Theory Calculator", gradient=(BLUE, PURPLE)).scale(1.1)
        subtitle = Text("Exploring Order in Randomness", color=YELLOW).next_to(title, DOWN)
        self.play(Write(title), run_time=2)
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(1)

        bg_circle = Circle(radius=3, color=BLUE, stroke_width=2)
        self.play(Create(bg_circle), run_time=1.5)
        dots = VGroup(*[Dot(radius=0.1, color=WHITE).move_to(bg_circle.point_at_angle(a)) for a in np.linspace(0, TAU, 10)])
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.1))

        edges = [Line(dots[i].get_center(), dots[j].get_center(), color=interpolate_color(RED, BLUE, j/len(dots)))
                 for i in range(len(dots)) for j in range(i+1, len(dots))]
        self.play(LaggedStart(*[Create(e) for e in edges], lag_ratio=0.002, run_time=3))

        self.play(FadeOut(VGroup(bg_circle, *edges, *dots)), run_time=1)
        tagline = Text("Bridging Theoretical Math with Computation", color=WHITE).scale(0.7)
        self.play(Write(tagline))
        self.wait(2)
