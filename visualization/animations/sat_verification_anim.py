from manim import *
import numpy as np

class SATVerificationAnimation(Scene):
    def construct(self):
        # Title
        title = Text("SAT-Based Verification", font_size=42, color=BLUE)
        subtitle = Text("Encoding graph coloring as Boolean satisfiability", font_size=26).next_to(title, DOWN)
        
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))
        
        # SAT Problem Overview
        overview_title = Text("What is SAT?", font_size=38, color=YELLOW).to_edge(UP)
        self.play(Write(overview_title))
        
        sat_def = Text(
            "Boolean Satisfiability Problem:\n"
            "Given a Boolean formula, find an assignment\n"
            "of TRUE/FALSE to variables that satisfies it",
            font_size=26,
            line_spacing=1.2
        ).shift(UP*0.8)
        
        self.play(FadeIn(sat_def, shift=UP))
        self.wait(2)
        
        example_formula = MathTex(
            r"(x_1 \lor \neg x_2) \land (\neg x_1 \lor x_3) \land (x_2 \lor \neg x_3)",
            font_size=36,
            color=GREEN
        ).shift(DOWN*0.5)
        
        self.play(Write(example_formula))
        
        solution = MathTex(
            r"x_1 = \text{TRUE}, \; x_2 = \text{FALSE}, \; x_3 = \text{TRUE}",
            font_size=32,
            color=GOLD
        ).shift(DOWN*1.8)
        
        self.play(Write(solution))
        self.wait(2)
        self.play(FadeOut(sat_def), FadeOut(example_formula), FadeOut(solution))
        
        # Graph Coloring Encoding
        encoding_title = Text("Encoding Graph Coloring", font_size=32, color=PURPLE).next_to(overview_title, DOWN, buff=0.5)
        self.play(Write(encoding_title))
        
        # Small graph for demonstration
        vertices = [1, 2, 3, 4]
        edges = [(1, 2), (2, 3), (3, 4), (4, 1), (1, 3)]
        
        graph = Graph(
            vertices,
            edges,
            layout="circular",
            vertex_config={"radius": 0.25, "color": WHITE, "fill_opacity": 1},
            edge_config={"stroke_width": 4},
            labels=True
        ).scale(1.2).shift(LEFT*3.5 + UP*0.3)
        
        self.play(Create(graph))
        
        # Variable encoding
        var_title = Text("Variables:", font_size=28, color=BLUE).shift(RIGHT*2.5 + UP*1.5)
        variables = VGroup(
            MathTex(r"r_{ij} = \text{edge } (i,j) \text{ is RED}", font_size=22),
            MathTex(r"\neg r_{ij} \text{ means edge is BLUE}", font_size=22)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(var_title, DOWN, aligned_edge=LEFT)
        
        self.play(Write(var_title))
        self.play(Write(variables))
        self.wait(2)
        
        # Constraints
        constraint_title = Text("Constraints:", font_size=28, color=RED).shift(RIGHT*2.5 + DOWN*0.3)
        constraints = VGroup(
            Text("No red triangle:", font_size=22, color=YELLOW),
            MathTex(r"\neg(r_{12} \land r_{23} \land r_{13})", font_size=20),
            Text("No blue triangle:", font_size=22, color=YELLOW),
            MathTex(r"\neg(\neg r_{12} \land \neg r_{23} \land \neg r_{13})", font_size=20)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(constraint_title, DOWN, aligned_edge=LEFT)
        
        self.play(Write(constraint_title))
        for constraint in constraints:
            self.play(Write(constraint), run_time=0.8)
        
        self.wait(3)
        self.play(
            FadeOut(graph),
            FadeOut(var_title),
            FadeOut(variables),
            FadeOut(constraint_title),
            FadeOut(constraints),
            FadeOut(overview_title),
            FadeOut(encoding_title)
        )
        
        # SAT Solver Process
        solver_title = Text("SAT Solver in Action", font_size=38, color=GREEN).to_edge(UP)
        self.play(Write(solver_title))
        
        steps = VGroup(
            Text("1. Encode graph as CNF formula", font_size=26),
            Text("2. Feed to SAT solver (PySAT/Z3)", font_size=26),
            Text("3. Solver searches for satisfying assignment", font_size=26),
            Text("4. If SAT: valid coloring exists", font_size=26, color=GREEN),
            Text("   If UNSAT: no valid coloring possible", font_size=26, color=RED)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(LEFT*1.5)
        
        for step in steps:
            self.play(FadeIn(step, shift=RIGHT), run_time=0.8)
            self.wait(0.8)
        
        self.wait(2)
        
        # Show verification progress
        self.play(FadeOut(steps))
        
        progress_text = Text("Verifying R(3,3)...", font_size=32, color=YELLOW).shift(UP*1)
        self.play(Write(progress_text))
        
        verification_results = VGroup(
            Text("n = 5: SAT ✓ (valid coloring exists)", font_size=26, color=GREEN),
            Text("n = 6: UNSAT ✗ (no valid coloring)", font_size=26, color=RED),
            MathTex(r"\therefore \; R(3,3) = 6", font_size=40, color=GOLD)
        ).arrange(DOWN, buff=0.5).shift(DOWN*0.5)
        
        for result in verification_results:
            self.play(FadeIn(result, shift=UP))
            self.wait(1.2)
        
        self.wait(3)
