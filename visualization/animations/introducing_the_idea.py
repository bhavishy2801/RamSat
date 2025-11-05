from manim import *
import itertools

class RamseyIntro(Scene):
    def construct(self):
        title = Text("Ramsey Numbers: R(s, t)", font_size=48)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # Shift graph left for text space
        shift_left = LEFT * 1.3
        coords = [
            (-3, 2, 0) + shift_left, (-1, 1.1, 0) + shift_left,
            (-4, 0.4, 0) + shift_left, (-2.3, -0.8, 0) + shift_left,
            (-3.7, -2.0, 0) + shift_left, (-1.4, -2.4, 0) + shift_left,
            (-0.1, -0.6, 0) + shift_left, (-4.6, -1.0, 0) + shift_left
        ]

        points = [Dot(coord, radius=.12) for coord in coords]
        labels = [Text(str(i+1), font_size=26).next_to(points[i], DOWN * 0.2)
                  for i in range(len(points))]
        self.play(*[FadeIn(p) for p in points], *[FadeIn(l) for l in labels])

        RED_CLIQUE = [(0,1),(1,2),(0,2)]
        BLUE_CLIQUE = [(3,4),(4,5),(3,5)]
        edges = VGroup()

        for i, j in itertools.combinations(range(len(points)), 2):
            if (i, j) in RED_CLIQUE or (j, i) in RED_CLIQUE:
                col = RED
            elif (i, j) in BLUE_CLIQUE or (j, i) in BLUE_CLIQUE:
                col = BLUE
            else:
                col = RED if (i+j) % 2 == 0 else BLUE
            edges.add(Line(points[i].get_center(),
                           points[j].get_center(),
                           color=col, stroke_width=2))
        self.play(*[Create(e) for e in edges])

        # Helper for safe text placement
        def show_text(lines):
            text_group = VGroup(*[
                Text(line, font_size=36)
                for line in lines
            ])
            text_group.arrange(DOWN, aligned_edge=LEFT)
            text_group.set_width(5)  # wrapping to avoid overlap
            text_group.to_edge(UR).shift(LEFT * 0.4 + DOWN * 0.9)
            self.play(FadeIn(text_group))
            return text_group

        # INITIAL TEXT
        intro_text = show_text([
            "Each vertex = a person",
            "Each edge = a relationship",
            "Red = friends | Blue = strangers"
        ])
        self.wait(1)

        # ✅ RED TRIANGLE
        self.play(*[e.animate.set_opacity(0.15) for e in edges])
        red_hl = [Line(points[i].get_center(), points[j].get_center(),
                       color=RED, stroke_width=6) for i, j in RED_CLIQUE]
        self.play(*[Create(h) for h in red_hl])

        self.play(FadeOut(intro_text, shift=UP * 0.3))

        red_text = show_text([
            "A triangle of mutual friends",
            "always appears in a large group.",
            "Ramsey numbers guarantee this."
        ])
        self.wait(2)

        self.play(*[FadeOut(h) for h in red_hl],
                  FadeOut(red_text),
                  *[e.animate.set_opacity(1) for e in edges])

        # ✅ BLUE TRIANGLE
        self.play(*[e.animate.set_opacity(0.15) for e in edges])
        blue_hl = [Line(points[i].get_center(), points[j].get_center(),
                        color=BLUE, stroke_width=6) for i, j in BLUE_CLIQUE]
        self.play(*[Create(h) for h in blue_hl])

        blue_text = show_text([
            "Even a group of complete strangers",
            "cannot avoid forming a triangle!",
            "Order emerges from randomness."
        ])
        self.wait(2)

        self.play(*[FadeOut(h) for h in blue_hl],
                  FadeOut(blue_text),
                  *[e.animate.set_opacity(1) for e in edges])

        # ✅ FINAL MESSAGE
        final_text = show_text([
            "Ramsey Numbers give the minimum",
            "group size where such patterns",
            "become unavoidable."
        ])
        self.wait(3)
