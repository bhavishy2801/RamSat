from manim import *
import numpy as np

class RamseyGraphEvolutionAdvanced(Scene):
    def construct(self):
        # Title
        title = Text("Advanced: Ramsey Number Growth", font_size=40, color=TEAL)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP).scale(0.8))
        
        # Show growth of known Ramsey numbers
        table_title = Text("Known Ramsey Numbers", font_size=32, color=YELLOW).next_to(title, DOWN)
        self.play(Write(table_title))
        
        # Create table
        ramsey_data = [
            ["r,s", "R(r,s)", "Status"],
            ["2,2", "2", "Trivial"],
            ["2,3", "3", "Trivial"],
            ["3,3", "6", "Known"],
            ["3,4", "9", "Known"],
            ["4,4", "18", "Known"],
            ["3,5", "14", "Known"],
            ["5,5", "43-48", "Bounds only!"]
        ]
        
        table = Table(
            ramsey_data[1:],
            row_labels=[Text(row[0], font_size=20) for row in ramsey_data[1:]],
            col_labels=[Text(col, font_size=22) for col in ramsey_data[0]],
            include_outer_lines=True,
            line_config={"stroke_width": 2}
        ).scale(0.6).shift(DOWN*0.3)
        
        self.play(Create(table))
        self.wait(2)
        
        # Highlight uncertainty
        unknown_box = SurroundingRectangle(table.get_rows()[7], color=RED, buff=0.1)
        unknown_label = Text("Unknown exact value!", font_size=24, color=RED).next_to(unknown_box, RIGHT)
        
        self.play(Create(unknown_box), Write(unknown_label))
        self.wait(2)
        
        self.play(FadeOut(table), FadeOut(table_title), FadeOut(unknown_box), FadeOut(unknown_label))
        
        # Complexity visualization
        complexity_title = Text("Computational Complexity", font_size=34, color=PURPLE).next_to(title, DOWN)
        self.play(Write(complexity_title))
        
        # Show exponential growth
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 100, 20],
            x_length=7,
            y_length=4,
            axis_config={"include_tip": True},
            x_axis_config={"numbers_to_include": range(0, 11, 2)},
            y_axis_config={"numbers_to_include": range(0, 101, 20)}
        ).shift(DOWN*0.8)
        
        x_label = axes.get_x_axis_label("n", edge=RIGHT, direction=RIGHT)
        y_label = axes.get_y_axis_label("R(n,n)", edge=UP, direction=UP)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        
        # Lower bound curve
        lower_bound = axes.plot(lambda x: 2**(x/2), x_range=[1, 9], color=BLUE)
        lower_label = MathTex(r"2^{n/2}", font_size=28, color=BLUE).next_to(lower_bound, LEFT)
        
        # Upper bound curve
        upper_bound = axes.plot(lambda x: 4**x / (x**0.5), x_range=[1, 6], color=RED)
        upper_label = MathTex(r"\frac{4^n}{\sqrt{n}}", font_size=28, color=RED).next_to(upper_bound, RIGHT, buff=0.5)
        
        self.play(Create(lower_bound), Write(lower_label))
        self.wait(1)
        self.play(Create(upper_bound), Write(upper_label))
        self.wait(1)
        
        gap_text = Text("Huge gap between bounds!", font_size=26, color=YELLOW).to_edge(DOWN)
        self.play(Write(gap_text))
        self.wait(2)
        
        self.play(
            FadeOut(axes),
            FadeOut(x_label),
            FadeOut(y_label),
            FadeOut(lower_bound),
            FadeOut(upper_bound),
            FadeOut(lower_label),
            FadeOut(upper_label),
            FadeOut(gap_text),
            FadeOut(complexity_title)
        )
        
        # Computational challenge
        challenge_title = Text("The Computational Challenge", font_size=36, color=ORANGE).next_to(title, DOWN)
        self.play(Write(challenge_title))
        
        challenges = VGroup(
            Text("• SAT formulas grow exponentially", font_size=26),
            Text("• Random simulations need many trials", font_size=26),
            Text("• Exact values only known for small n", font_size=26),
            Text("• R(5,5) unknown after 80+ years!", font_size=26, color=RED)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(DOWN*0.5)
        
        for challenge in challenges:
            self.play(FadeIn(challenge, shift=RIGHT))
            self.wait(0.8)
        
        self.wait(2)
        
        # RamSat contribution
        self.play(FadeOut(challenges), FadeOut(challenge_title))
        
        contribution_title = Text("RamSat's Contribution", font_size=36, color=GREEN).next_to(title, DOWN)
        self.play(Write(contribution_title))
        
        contributions = VGroup(
            Text("✓ Hybrid computational approach", font_size=28, color=BLUE),
            Text("✓ Probabilistic bound estimation", font_size=28, color=BLUE),
            Text("✓ SAT-based verification for small cases", font_size=28, color=BLUE),
            Text("✓ Educational visualization", font_size=28, color=BLUE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(DOWN*0.3)
        
        for contribution in contributions:
            self.play(FadeIn(contribution, shift=UP))
            self.wait(0.6)
        
        self.wait(3)
