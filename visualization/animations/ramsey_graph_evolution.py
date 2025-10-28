from manim import *
import numpy as np

class RamseyGraphEvolution(Scene):
    def construct(self):
        # Title
        title = Text("Graph Evolution: Finding R(3,3)", font_size=40, color=PURPLE)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))
        
        # Start with K5 (n=5)
        n5_label = Text("K₅: Can we avoid monochromatic triangles?", font_size=28, color=YELLOW).next_to(title, DOWN)
        self.play(Write(n5_label))
        
        vertices_5 = list(range(1, 6))
        edges_5 = [(i, j) for i in vertices_5 for j in vertices_5 if i < j]
        
        graph_5 = Graph(
            vertices_5,
            edges_5,
            layout="circular",
            vertex_config={"radius": 0.2, "color": WHITE, "fill_opacity": 1},
            edge_config={"stroke_width": 3}
        ).scale(1.8).shift(DOWN*0.5)
        
        self.play(Create(graph_5))
        self.wait(1)
        
        # Color edges to avoid triangles
        valid_coloring = {
            (1, 2): RED, (2, 3): RED, (3, 4): RED, (4, 5): RED, (5, 1): RED,
            (1, 3): BLUE, (2, 4): BLUE, (3, 5): BLUE, (4, 1): BLUE, (5, 2): BLUE
        }
        
        animations = []
        for edge_tuple, color in valid_coloring.items():
            edge = graph_5.edges[edge_tuple]
            animations.append(edge.animate.set_color(color))
        
        self.play(*animations, run_time=2)
        
        success_text = Text("✓ Valid coloring found!", font_size=28, color=GREEN).to_edge(DOWN)
        self.play(Write(success_text))
        self.wait(2)
        
        # Transition to K6
        self.play(
            FadeOut(graph_5),
            FadeOut(n5_label),
            FadeOut(success_text)
        )
        
        n6_label = Text("K₆: Now it becomes impossible!", font_size=28, color=YELLOW).next_to(title, DOWN)
        self.play(Write(n6_label))
        
        vertices_6 = list(range(1, 7))
        edges_6 = [(i, j) for i in vertices_6 for j in vertices_6 if i < j]
        
        graph_6 = Graph(
            vertices_6,
            edges_6,
            layout="circular",
            vertex_config={"radius": 0.2, "color": WHITE, "fill_opacity": 1},
            edge_config={"stroke_width": 3}
        ).scale(1.8).shift(DOWN*0.5)
        
        self.play(Create(graph_6))
        self.wait(1)
        
        # Try to color but highlight inevitable triangle
        attempt_text = Text("Attempting to color...", font_size=24, color=ORANGE).to_edge(DOWN)
        self.play(Write(attempt_text))
        
        # Color some edges
        partial_coloring = {}
        for i, edge_tuple in enumerate(edges_6[:10]):
            color = RED if i % 2 == 0 else BLUE
            partial_coloring[edge_tuple] = color
            self.play(graph_6.edges[edge_tuple].animate.set_color(color), run_time=0.3)
        
        self.wait(1)
        
        # Highlight a monochromatic triangle
        triangle_vertices = [1, 2, 3]
        triangle_edges = [(1, 2), (2, 3), (1, 3)]
        
        # Make these edges red
        for edge in triangle_edges:
            self.play(graph_6.edges[edge].animate.set_color(RED).set_stroke(width=6), run_time=0.5)
        
        # Highlight the triangle
        triangle_highlight = Polygon(
            *[graph_6.vertices[v].get_center() for v in triangle_vertices],
            color=YELLOW,
            fill_opacity=0.3,
            stroke_width=4
        )
        
        self.play(Create(triangle_highlight))
        
        fail_text = Text("✗ Monochromatic triangle found!", font_size=28, color=RED)
        fail_text.next_to(attempt_text, UP)
        self.play(Write(fail_text))
        self.wait(2)
        
        # Conclusion
        self.play(
            FadeOut(graph_6),
            FadeOut(triangle_highlight),
            FadeOut(n6_label),
            FadeOut(attempt_text),
            FadeOut(fail_text)
        )
        
        conclusion = VGroup(
            Text("Conclusion:", font_size=36, color=GOLD),
            MathTex(r"R(3,3) = 6", font_size=52, color=GREEN),
            Text("6 is the minimum number where", font_size=24),
            Text("monochromatic triangles are unavoidable", font_size=24)
        ).arrange(DOWN, buff=0.4)
        
        self.play(FadeIn(conclusion, shift=UP))
        self.wait(3)
