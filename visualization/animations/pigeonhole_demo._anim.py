from manim import *
import numpy as np

class PigeonholeDemo(Scene):
    def construct(self):
        # Title
        title = Text("Pigeonhole Principle Bounds", font_size=44, color=RED)
        subtitle = Tex(r"Computing bounds for $R(r, s)$", font_size=32).next_to(title, DOWN)
        
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))
        
        # Classical Pigeonhole Visualization
        pigeonhole_title = Text("The Pigeonhole Principle", font_size=36, color=YELLOW).to_edge(UP)
        self.play(Write(pigeonhole_title))
        
        # Pigeons and holes
        holes = VGroup(*[
            Rectangle(height=0.8, width=0.6, color=BLUE, fill_opacity=0.2)
            for _ in range(5)
        ]).arrange(RIGHT, buff=0.3).shift(UP*1)
        
        hole_labels = VGroup(*[
            Text(f"Hole {i+1}", font_size=18).next_to(holes[i], DOWN, buff=0.1)
            for i in range(5)
        ])
        
        self.play(Create(holes), Write(hole_labels))
        
        # Pigeons
        pigeons = VGroup(*[
            Dot(radius=0.15, color=RED, fill_opacity=1).move_to(UP*3 + LEFT*4 + RIGHT*i*0.8)
            for i in range(7)
        ])
        
        pigeon_label = Text("7 Pigeons", font_size=24, color=RED).next_to(pigeons, UP)
        self.play(FadeIn(pigeons), Write(pigeon_label))
        self.wait(1)
        
        # Place pigeons in holes
        for i, pigeon in enumerate(pigeons):
            target_hole = i % 5
            self.play(
                pigeon.animate.move_to(holes[target_hole].get_center()),
                run_time=0.5
            )
        
        conclusion = Text(
            "At least one hole contains 2+ pigeons!",
            font_size=28,
            color=GREEN
        ).shift(DOWN*2)
        self.play(Write(conclusion))
        self.wait(2)
        
        self.play(
            FadeOut(pigeonhole_title),
            FadeOut(holes),
            FadeOut(hole_labels),
            FadeOut(pigeons),
            FadeOut(pigeon_label),
            FadeOut(conclusion)
        )
        
        # Ramsey Number Bound Formula
        formula_title = Text("Upper Bound Formula", font_size=38, color=BLUE).to_edge(UP)
        self.play(Write(formula_title))
        
        bound_formula = MathTex(
            r"R(r, s) \leq R(r-1, s) + R(r, s-1)",
            font_size=48
        ).shift(UP*1)
        
        self.play(Write(bound_formula))
        self.wait(2)
        
        # Example: R(3,3)
        example = Text("Example: Computing R(3,3)", font_size=32, color=YELLOW).shift(DOWN*0.5)
        self.play(FadeIn(example))
        
        calculation = VGroup(
            MathTex(r"R(3,3) \leq R(2,3) + R(3,2)", font_size=36),
            MathTex(r"R(2,n) = n \text{ and } R(n,2) = n", font_size=32, color=GRAY),
            MathTex(r"R(3,3) \leq 3 + 3 = 6", font_size=40, color=GREEN)
        ).arrange(DOWN, buff=0.4).shift(DOWN*2)
        
        for line in calculation:
            self.play(Write(line))
            self.wait(1.5)
        
        self.wait(2)
        
        # Show general recursive pattern
        self.play(
            FadeOut(formula_title),
            FadeOut(bound_formula),
            FadeOut(example),
            FadeOut(calculation)
        )
        
        tree_title = Text("Recursive Bound Tree", font_size=36, color=PURPLE).to_edge(UP)
        self.play(Write(tree_title))
        
        # Simple tree visualization
        root = Circle(radius=0.4, color=BLUE, fill_opacity=0.3).shift(UP*2)
        root_label = MathTex("R(3,3)", font_size=28).move_to(root.get_center())
        
        left_child = Circle(radius=0.35, color=RED, fill_opacity=0.2).shift(UP*0.5 + LEFT*2)
        left_label = MathTex("R(2,3)", font_size=24).move_to(left_child.get_center())
        
        right_child = Circle(radius=0.35, color=RED, fill_opacity=0.2).shift(UP*0.5 + RIGHT*2)
        right_label = MathTex("R(3,2)", font_size=24).move_to(right_child.get_center())
        
        arrow_left = Arrow(root.get_bottom(), left_child.get_top(), buff=0.1, color=WHITE)
        arrow_right = Arrow(root.get_bottom(), right_child.get_top(), buff=0.1, color=WHITE)
        
        self.play(Create(root), Write(root_label))
        self.play(
            Create(arrow_left), Create(arrow_right),
            Create(left_child), Write(left_label),
            Create(right_child), Write(right_label)
        )
        
        result = Text("Both base cases = 3, so R(3,3) ≤ 6", font_size=30, color=GREEN).shift(DOWN*1.5)
        self.play(Write(result))
        
        self.wait(3)
