from manim import *
import numpy as np

class ErdosProbabilisticMethod(Scene):
    def construct(self):
        # Title
        title = Text("Erdős Probabilistic Method", font_size=42, color=ORANGE)
        subtitle = Text("Proving existence through probability", font_size=28).next_to(title, DOWN)
        
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))
        
        # Key Idea
        idea_title = Text("Key Insight", font_size=38, color=YELLOW).to_edge(UP)
        self.play(Write(idea_title))
        
        idea_text = Text(
            "If the probability of a random coloring\n"
            "avoiding both monochromatic structures is > 0,\n"
            "then such a coloring must exist!",
            font_size=26,
            line_spacing=1.2
        ).shift(UP*0.5)
        
        self.play(FadeIn(idea_text, shift=UP), run_time=2)
        self.wait(3)
        self.play(FadeOut(idea_text))
        
        # Probability calculation
        calc_title = Text("Probability Calculation", font_size=32, color=GREEN).next_to(idea_title, DOWN, buff=0.5)
        self.play(Write(calc_title))
        
        formulas = VGroup(
            MathTex(r"P(\text{red } K_r) = 2^{-\binom{r}{2}}", font_size=36),
            MathTex(r"\text{Number of } K_r \text{ subgraphs} = \binom{n}{r}", font_size=32),
            MathTex(
                r"P(\text{exists red } K_r) \leq \binom{n}{r} \cdot 2^{-\binom{r}{2}}",
                font_size=36,
                color=BLUE
            ),
            MathTex(
                r"P(\text{no monochromatic } K_r) > 0 \text{ when } n \text{ small}",
                font_size=32,
                color=YELLOW
            )
        ).arrange(DOWN, buff=0.5).shift(DOWN*0.5)
        
        for formula in formulas:
            self.play(Write(formula))
            self.wait(1.5)
        
        self.wait(2)
        self.play(FadeOut(idea_title), FadeOut(calc_title), FadeOut(formulas))
        
        # Simulation visualization
        sim_title = Text("Random Coloring Simulation", font_size=38, color=PURPLE).to_edge(UP)
        self.play(Write(sim_title))
        
        # Create a small graph
        vertices = list(range(1, 7))
        edges = [(i, j) for i in vertices for j in vertices if i < j]
        
        graph = Graph(
            vertices,
            edges,
            layout="circular",
            vertex_config={"radius": 0.2, "color": WHITE, "fill_opacity": 1},
            edge_config={"stroke_width": 3}
        ).scale(1.5)
        
        self.play(Create(graph))
        self.wait(1)
        
        # Random coloring animation
        num_trials = 5
        success_text = Text("Searching for valid colorings...", font_size=28, color=YELLOW).to_edge(DOWN)
        self.play(Write(success_text))
        
        for trial in range(num_trials):
            # Random edge colors
            edge_colors = {}
            for edge in graph.edges.values():
                color = RED if np.random.random() < 0.5 else BLUE
                edge_colors[edge] = color
            
            animations = []
            for edge, color in edge_colors.items():
                animations.append(edge.animate.set_color(color))
            
            self.play(*animations, run_time=0.8)
            self.wait(0.5)
        
        final_text = Text(
            "As n increases, probability of valid coloring decreases",
            font_size=26,
            color=GREEN
        ).next_to(success_text, UP)
        self.play(Write(final_text))
        
        self.wait(2)
        self.play(FadeOut(graph), FadeOut(sim_title), FadeOut(success_text), FadeOut(final_text))
        
        # Lower bound conclusion
        conclusion_title = Text("Lower Bound Result", font_size=38, color=GREEN).to_edge(UP)
        self.play(Write(conclusion_title))
        
        bound_formula = MathTex(
            r"R(r, r) \geq 2^{r/2}",
            font_size=52,
            color=GOLD
        ).shift(UP*0.5)
        
        self.play(Write(bound_formula))
        
        explanation = Text(
            "Erdős proved this exponential lower bound\n"
            "using the probabilistic method in 1947",
            font_size=26,
            line_spacing=1.2
        ).shift(DOWN*1.5)
        
        self.play(FadeIn(explanation))
        self.wait(3)
