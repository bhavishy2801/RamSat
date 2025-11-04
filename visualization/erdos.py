from manim import *
import random
import math

class ErdosProbabilisticLowerBound(Scene):
    def construct(self):
        self.camera.background_color = "#0b0b10"
        title = Tex(r"Erdős Probabilistic Method --- Lower Bound", color=YELLOW).scale(0.8).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # === Graph Setup ===
        n_nodes = 10  # More nodes for a denser graph
        radius = 2.3  # Slightly smaller radius for compactness

        # Node positions arranged in a circle
        nodes = [np.array([radius * math.cos(2*PI*i/n_nodes),
                           radius * math.sin(2*PI*i/n_nodes), 0]) for i in range(n_nodes)]

        # Create dots for vertices
        vertices = [Dot(point, radius=0.06, color=WHITE) for point in nodes]
        vertex_group = VGroup(*vertices)
        self.play(FadeIn(vertex_group, lag_ratio=0.1))
        self.wait(0.3)

        # Function to generate random colored edges
        def get_random_edges():
            edges = []
            for i in range(n_nodes):
                for j in range(i+1, n_nodes):
                    color = random.choice([RED, BLUE])
                    edges.append(Line(nodes[i], nodes[j], stroke_width=2, color=color, stroke_opacity=0.65))
            return VGroup(*edges)

        # === Random Flashing Phase ===
        edge_group = get_random_edges()
        self.play(Create(edge_group), run_time=2)
        self.wait(0.3)

        for _ in range(5):  # Flash random recolorings
            new_edges = get_random_edges()
            self.play(Transform(edge_group, new_edges), run_time=0.4)
        self.wait(0.5)

        # === Probability Curve Visualization ===
        self.play(FadeOut(edge_group), FadeOut(vertex_group))

        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 1, 0.2],
            x_length=6,
            y_length=3,
            axis_config={"color": GREY_B, "stroke_width": 2},
        ).to_edge(DOWN).shift(UP*0.5)

        curve = axes.plot(lambda x: math.exp(-((x-2.5)**2)/1.5), color=BLUE, stroke_width=4)
        shaded_region = axes.get_area(curve, x_range=[3.5, 5], color=RED, opacity=0.4)
        self.play(Create(axes), Create(curve))
        self.wait(0.4)
        self.play(FadeIn(shaded_region))
        self.wait(0.3)

        # Threshold Line
        threshold_line = axes.get_vertical_line(axes.c2p(3.5, 0.3), color=YELLOW, stroke_width=3)
        threshold_text = MathTex(r"\text{Threshold: } E[X] < 1", color=YELLOW).next_to(axes, UP)
        self.play(GrowFromCenter(threshold_line), Write(threshold_text))
        self.wait(1)

        # Fade away shaded area = "existence"
        self.play(FadeOut(shaded_region, run_time=1.5))
        self.wait(0.5)

        # === Existential Result ===
        existence_text = Tex(
            r"Existence without construction", color=GREEN
        ).scale(0.9).next_to(axes, DOWN)

        self.play(Write(existence_text))
        self.wait(0.5)

        # === Transition to clean surviving graph ===
        self.play(FadeOut(axes), FadeOut(curve), FadeOut(threshold_line), FadeOut(threshold_text), FadeOut(existence_text))

        final_edges = get_random_edges()
        final_graph = VGroup(final_edges, vertex_group)
        self.play(FadeIn(vertex_group), Create(final_edges, lag_ratio=0.05))
        self.wait(0.3)

        lower_text = Tex("Erdős’ Lower Bound", color=GREEN).scale(0.9).to_edge(DOWN)
        self.play(Write(lower_text))
        self.wait(2)

        # End clean
        self.play(FadeOut(final_graph), FadeOut(lower_text), FadeOut(title))
