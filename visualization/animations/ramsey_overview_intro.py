from manim import *
import numpy as np

class RamseyOverviewIntro(Scene):
    def construct(self):
        # Title
        title = Text("RamSat: A Ramsey Theory Calculator", font_size=48, color=BLUE)
        subtitle = Text(
            "Computing Order from Chaos",
            font_size=32,
            color=YELLOW
        ).next_to(title, DOWN)
        
        self.play(Write(title), run_time=2)
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))
        
        # Ramsey's Theorem Statement
        theorem_title = Text("Ramsey's Theorem", font_size=42, color=GREEN).to_edge(UP)
        theorem_text = Tex(
            r"For any $r, s \geq 2$, there exists $R(r,s)$ such that\\",
            r"every red-blue coloring of $K_{R(r,s)}$ contains\\",
            r"either a red $K_r$ or a blue $K_s$",
            font_size=36
        ).next_to(theorem_title, DOWN, buff=0.5)
        
        self.play(Write(theorem_title))
        self.play(FadeIn(theorem_text, shift=UP), run_time=2)
        self.wait(3)
        self.play(FadeOut(theorem_title), FadeOut(theorem_text))
        
        # Methods Overview
        methods_title = Text("Three Computational Approaches", font_size=40, color=PURPLE).to_edge(UP)
        self.play(Write(methods_title))
        
        methods = VGroup(
            VGroup(
                Circle(radius=0.3, color=RED, fill_opacity=0.3),
                Text("Pigeonhole\nPrinciple", font_size=24)
            ).arrange(DOWN),
            VGroup(
                Circle(radius=0.3, color=ORANGE, fill_opacity=0.3),
                Text("Erdős\nProbabilistic", font_size=24)
            ).arrange(DOWN),
            VGroup(
                Circle(radius=0.3, color=BLUE, fill_opacity=0.3),
                Text("SAT-Based\nVerification", font_size=24)
            ).arrange(DOWN)
        ).arrange(RIGHT, buff=1.5).shift(DOWN*0.5)
        
        for method in methods:
            self.play(
                GrowFromCenter(method[0]),
                FadeIn(method[1], shift=UP),
                run_time=0.8
            )
        
        self.wait(2)
        
        # Connection arrows
        arrows = VGroup(
            Arrow(methods[0].get_right(), methods[1].get_left(), buff=0.2, color=WHITE),
            Arrow(methods[1].get_right(), methods[2].get_left(), buff=0.2, color=WHITE)
        )
        self.play(Create(arrows))
        
        integration_text = Text(
            "Unified Computational Framework",
            font_size=28,
            color=YELLOW
        ).to_edge(DOWN)
        self.play(Write(integration_text))
        self.wait(3)
        
        # Transition to example
        self.play(
            FadeOut(methods_title),
            FadeOut(methods),
            FadeOut(arrows),
            FadeOut(integration_text)
        )
        
        example_title = Text("Example: R(3,3) = 6", font_size=48, color=GOLD)
        example_desc = Text(
            "The minimum number of people at a party where\n"
            "3 are mutual friends OR 3 are mutual strangers",
            font_size=28
        ).next_to(example_title, DOWN, buff=0.5)
        
        self.play(Write(example_title))
        self.play(FadeIn(example_desc, shift=UP))
        self.wait(3)
        self.play(FadeOut(example_title), FadeOut(example_desc))
