from manim import *
import numpy as np
import random

class Sparse3DGraphRamsey(ThreeDScene):
    def construct(self):
        # -------- Camera setup --------
        self.set_camera_orientation(phi=70 * DEGREES, theta=20 * DEGREES)

        # -------- Title --------
        title = Text(
            "Ramachandran Plots: Ramsey Theory's Use",
            font_size=36, weight=BOLD
        ).to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        self.add(title)

        # -------- Parameters --------
        N = 70
        num_edges = 100       # ↓ fewer edges for faster render
        radius = 3.0
        random.seed(42)
        np.random.seed(42)

        # -------- Node positions (vectorized) --------
        angles = np.linspace(0, 2 * np.pi, N, endpoint=False)
        base_circle = np.column_stack((
            radius * np.cos(angles),
            radius * np.sin(angles),
            np.zeros(N)
        ))
        jitter = np.random.uniform(-0.7, 0.7, (N, 3))
        points = base_circle + jitter

        # -------- Edge generation --------
        edges = set()
        while len(edges) < num_edges:
            i, j = random.sample(range(N), 2)
            if i != j:
                edges.add(tuple(sorted((i, j))))
        edges = list(edges)

        red_levels = [RED_E, RED_C, RED_A]
        green_color = "#00FF88"
        green_edges = {
            e for e in edges if (abs(e[0] - e[1]) % 7 == 0 or abs(e[0] - e[1]) % 11 == 0)
        }

        # -------- Graph construction --------
        # Vectorized loops → single creation pass
        edge_objs = [
            Line(
                points[i], points[j],
                color=(green_color if (i, j) in green_edges else red_levels[k % 3]),
                stroke_width=(1.8 if (i, j) in green_edges else 1.0)
            )
            for k, (i, j) in enumerate(edges)
        ]
        node_objs = [Dot3D(p, radius=0.03, color=WHITE) for p in points]

        ramsey_graph = VGroup(*edge_objs, *node_objs)
        self.add(ramsey_graph)

        # -------- 1. Rotate graph --------
        self.move_camera(theta=60 * DEGREES, run_time=5)

        # -------- 2. Fade to black --------
        black_screen = Rectangle(color=BLACK, fill_opacity=1).scale(10)
        self.play(FadeIn(black_screen, run_time=0.7))
        self.remove(ramsey_graph)

        # -------- 3. Protein-like deterministic structure --------
        t = np.linspace(0, 6 * np.pi, N)
        x = np.sin(t) + 0.3 * np.sin(3 * t)
        y = np.cos(t) + 0.3 * np.cos(2 * t)
        z = 0.5 * np.sin(2 * t)
        protein_points = np.column_stack((x, y, z))

        red_levels = [RED_E, RED_C, RED_A]
        edges2 = [
            Line(protein_points[i], protein_points[i + 1],
                 color=red_levels[i % 3], stroke_width=1.2)
            for i in range(N - 1)
        ]
        nodes2 = [Dot3D(p, radius=0.03, color=WHITE) for p in protein_points]
        protein_graph = VGroup(*edges2, *nodes2).shift(RIGHT * 2.5)

        # Fade in protein
        self.play(
            FadeOut(black_screen, run_time=0.6),
            FadeIn(protein_graph, run_time=0.8)
        )

        # -------- 4. Caption --------
        caption = Text(
            "Ramachandran plots visualize allowed\n"
            "bond angles (phi, psi) in proteins —\n"
            "revealing helices, sheets, and folds.",
            font_size=26
        ).to_edge(RIGHT).shift(DOWN * 0.5)
        self.add_fixed_in_frame_mobjects(caption)
        self.play(FadeIn(caption, shift=LEFT * 0.3, run_time=1.0))

        # -------- 5. Gentle protein rotation --------
        self.move_camera(theta=100 * DEGREES, run_time=5)
        self.wait(0.4)
