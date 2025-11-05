from manim import *
import itertools, random, numpy as np

class RamseyInNeuralNets(Scene):
    def construct(self):
        # Title
        title = Text("Discovering Patterns — Ramsey Theory in Neural Nets", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        N = 20
        random.seed(2)

        # Initial random positions
        positions = [np.array([random.uniform(-5, 5), random.uniform(-2, 2), 0]) for _ in range(N)]
        nodes = [Dot(pos, radius=0.12, color=GREY_B) for pos in positions]
        node_group = VGroup(*nodes)

        self.play(FadeIn(node_group))
        self.wait(0.5)

        # Random edges (random weight init)
        edges = []
        for i, j in itertools.combinations(range(N), 2):
            if random.random() < 0.12:
                line = Line(nodes[i].get_center(), nodes[j].get_center(), stroke_opacity=0.5)
                edges.append(line)

        edge_group = VGroup(*edges)
        self.play(LaggedStartMap(Create, edge_group, lag_ratio=0.01), run_time=2)
        self.wait(0.5)

        # Caption 1
        caption1 = Text("Even random graphs contain hidden structure...", font_size=28).next_to(title, DOWN)
        self.play(Write(caption1))
        self.wait(1.5)

        # Highlight a "structured" subgraph (sample)
        sample_nodes = random.sample(range(N), 5)
        highlights = VGroup(*[nodes[i].copy().set_color(YELLOW).scale(1.5) for i in sample_nodes])
        self.play(FadeIn(highlights))
        self.wait(0.8)

        # Ramsey theory claim
        claim = Tex(
            "Ramsey theory: Any large enough graph must contain structured subgraphs.",
            font_size=26
        ).to_edge(DOWN)
        self.play(Write(claim))
        self.wait(1.5)

        # Define neural network layout target positions
        layer_x = [-5, -2, 1, 4]
        new_positions = []
        for idx, node in enumerate(nodes):
            layer = idx % 4
            x = layer_x[layer]
            y = (idx // 4 - 2) * 0.8
            new_positions.append(np.array([x, y, 0]))

        # Instead of MoveToTarget, animate each node to its new location
        self.play(
            *[node.animate.move_to(new_pos) for node, new_pos in zip(nodes, new_positions)],
            run_time=2
        )
        self.wait(0.5)

        # Remove old edges
        self.play(FadeOut(edge_group, shift=DOWN * 0.2))

        # Create edges between layers (feedforward look)
        new_edges = []
        for i in range(N):
            for j in range(N):
                li, lj = i % 4, j % 4
                if lj == li + 1 and random.random() < 0.4:
                    new_edges.append(Line(nodes[i].get_center(), nodes[j].get_center(), stroke_opacity=0.5))
        new_edge_group = VGroup(*new_edges)
        self.play(LaggedStartMap(Create, new_edge_group, lag_ratio=0.02), run_time=2)
        self.wait(0.5)

        # Pulse edges to show “learning”
        pulse_edges = VGroup(*[edge.copy().set_color(BLUE_E).set_stroke(width=3, opacity=0.8) for edge in new_edges])
        self.play(LaggedStartMap(Create, pulse_edges, lag_ratio=0.02), run_time=3)
        self.wait(0.5)

        # Final explanatory text
        final_text = Tex(
            "Neural networks exploit guaranteed structure —\\\\"
            "Ramsey theory ensures it’s always there.",
            font_size=26
        ).next_to(claim, UP)
        self.play(Write(final_text))
        self.wait(2.5)

        self.play(FadeOut(VGroup(title, node_group, new_edge_group, pulse_edges, claim, caption1, final_text)))
        self.wait(0.5)
