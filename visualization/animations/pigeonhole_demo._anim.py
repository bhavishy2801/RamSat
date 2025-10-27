import random
from manim import *

class PigeonholeDemo(Scene):
    def construct(self):
        title = Text("Pigeonhole Principle in Ramsey Bounds").scale(0.8)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        boxes = VGroup(*[Square(side_length=1, color=BLUE) for _ in range(4)]).arrange(RIGHT, buff=0.8)
        self.play(LaggedStart(*[Create(b) for b in boxes], lag_ratio=0.3))

        pigeons = VGroup(*[Circle(radius=0.2, color=YELLOW, fill_opacity=1) for _ in range(5)])
        for i, p in enumerate(pigeons):
            p.move_to(UP * random.uniform(-1, 1) + LEFT * random.uniform(0, 3))
        self.play(LaggedStart(*[FadeIn(p) for p in pigeons], lag_ratio=0.2))

        self.wait(0.5)
        self.play(*[p.animate.move_to(boxes[i % 4].get_center()) for i, p in enumerate(pigeons)])
        self.wait(1)

        txt = MathTex(r"5 > 4 \Rightarrow \text{ at least one box has } \ge 2 \text{ pigeons.}")
        txt.next_to(boxes, DOWN)
        self.play(Write(txt))
        self.wait(2)

        formula = MathTex(r"R(3,3) \le 6").scale(1.2).next_to(txt, DOWN)
        self.play(Write(formula))
        self.wait(2)
