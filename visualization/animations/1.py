from manim import *
import itertools

class RamseyBeauty(Scene):
    def construct(self):

        title = Text("Beauty Hidden in Chaos", font_size=52)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # ---------- Big Grid on Left ----------
        rows, cols = 18, 26
        cell = 0.33
        gap = 0.01

        left_shift = LEFT * 4.2 + DOWN * 0.3
        
        def pos(r, c):
            return left_shift + np.array([
                (c - cols/2) * (cell + gap),
                -(r - rows/2) * (cell + gap),
                0
            ])

        # Base "chaotic" color generator with many colors
        color_palette = [
            RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE, TEAL, PINK, GOLD, MAROON
        ]
        def noisy_color(r, c):
            return color_palette[(r * 41 + c * 97 + (r ^ c)) % len(color_palette)]

        tiles = VGroup()
        for r in range(rows):
            for c in range(cols):
                sq = Square(cell, stroke_width=0.5, fill_opacity=1)
                sq.move_to(pos(r, c))
                sq.set_fill(noisy_color(r,c))
                tiles.add(sq)

        self.play(FadeIn(tiles), run_time=1.2)

        # Intro text right
        def show_text(texts, color=WHITE):
            g = VGroup(*[Text(t, font_size=34, color=color) for t in texts])
            g.arrange(DOWN, aligned_edge=LEFT)
            g.set_width(5)
            g.to_edge(UR).shift(LEFT * 0.5 + DOWN * 0.8)
            self.play(FadeIn(g, shift=DOWN * 0.1), run_time=0.6)
            return g

        intro = show_text([
            "A colorful chaotic mosaic.",
            "No obvious design. No order."
        ])
        self.wait(1.2)

        self.play(FadeOut(intro, shift=UP*0.2))

        expl = show_text([
            "But look closer...",
            "Chaos doesn't stay chaotic for long."
        ])
        self.wait(1.4)

        # ---------- Hidden Gorgeous Pattern ----------
        # Coordinates for brilliant rainbow diamond
        center = (rows//2, cols//2)
        diamond = []
        size = 6
        for r in range(rows):
            for c in range(cols):
                if abs(r-center[0]) + abs(c-center[1]) <= size:
                    diamond.append((r,c))

        rainbow = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, PINK]
        def rainbow_for(r,c):
            d = abs(r-center[0]) + abs(c-center[1])
            return rainbow[d % len(rainbow)]

        self.play(FadeOut(expl))

        # Dim background
        self.play(*[tile.animate.set_opacity(0.15) for tile in tiles], run_time=0.7)

        highlight_tiles = []
        for (r,c) in diamond:
            idx = r*cols + c
            tile = tiles[idx]
            highlight_tiles.append(tile)

        self.play(
            *[
                highlight_tiles[i].animate.set_fill(rainbow_for(*diamond[i])).set_opacity(1.0)
                for i in range(len(highlight_tiles))
            ],
            run_time=1.4
        )

        diamond_group = VGroup(*highlight_tiles)
        border = SurroundingRectangle(diamond_group, color=WHITE, stroke_width=5)
        glow = border.copy().set_stroke(YELLOW, width=15, opacity=0.4)
        self.play(Create(border), FadeIn(glow), run_time=0.9)

        result = show_text([
            "Hidden structure emerges.",
            "A rainbow diamond inside randomness.",
            "Ramsey-style beauty from chaos.",
        ], color=YELLOW)

        self.wait(2.5)
