from manim import *
import numpy as np

# Run:
# manim -pql inevitable_islands_sparse_centered.py InevitableIslandsNeuralSparse_Centered
# (≈90–110 s render on pql, ~30 s runtime)

class InevitableIslandsNeuralSparse_Centered(ThreeDScene):
    def construct(self):
        np.random.seed(42)

        LAYERS, N_PER_LAYER = 6, 16
        LAYER_SPACING, NODE_SPREAD = 1.2, 2.2
        TOTAL_NODES = LAYERS * N_PER_LAYER

        # --- Node layout (lifted upward) ---
        pts = []
        for l in range(LAYERS):
            xs = np.linspace(-NODE_SPREAD, NODE_SPREAD, N_PER_LAYER)
            for x in xs:
                pts.append([x, (l - LAYERS/2) * LAYER_SPACING, 0])
        pts = np.array(pts)
        pts[:, 0] += 2.0      # move to the right
        pts[:, 1] += 1.5      # move up more to center better

        # --- Neurons ---
        dots = VGroup(*[Dot(pts[i], radius=0.07, color=GRAY) for i in range(TOTAL_NODES)])
        for d in dots:
            d.set_opacity(0.8)
        self.add(dots)

        # --- Sparse deterministic edges ---
        lines = VGroup()
        desired_edges = 350
        edge_pairs = set()
        while len(edge_pairs) < desired_edges:
            i, j = np.random.randint(0, TOTAL_NODES, 2)
            if i != j and abs(i - j) > 4:
                edge_pairs.add((i, j))
        for (i, j) in edge_pairs:
            src, tgt = pts[i], pts[j]
            base = np.random.choice([BLUE_D, RED_D, GREEN_D])
            grad = interpolate_color(base, WHITE, 0.5)
            line = Line(src, tgt, stroke_width=0.8)
            line.set_color_by_gradient(base, grad)
            line.set_opacity(0.18)
            lines.add(line)
        self.add(lines)

        # --- Camera ---
        self.set_camera_orientation(phi=65*DEGREES, theta=35*DEGREES)

        # --- Text overlays ---
        caption = VGroup(
            Text("In complex systems,", color=WHITE, font_size=32),
            Text("any node can link to any other — but sparsely.", color=TEAL_A, font_size=32)
        ).arrange(DOWN, aligned_edge=ORIGIN).to_edge(UP, buff=0.8)

        self.add_fixed_in_frame_mobjects(caption)



        title = Text("Inevitable Islands — Sparse Structured Chaos", color=YELLOW_E).scale(0.5)
        title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)

        # --- Intro ---
        self.play(FadeIn(dots, scale=1.05), FadeIn(lines), run_time=2)
        self.wait(0.8)
        self.move_camera(phi=60*DEGREES, theta=25*DEGREES, run_time=3)

        # --- Define deterministic "islands" ---
        red_idxs = [l * N_PER_LAYER + (N_PER_LAYER//2 - 4 + l) for l in range(LAYERS)]
        center_layer = LAYERS // 2
        base = center_layer * N_PER_LAYER + (N_PER_LAYER//2 - 1)
        green_idxs = [base + dx + dy*N_PER_LAYER for dy in [-1,0,1] for dx in [-1,0,1]]
        blue_idxs = []
        for l in [2,3]:
            base = l * N_PER_LAYER + (N_PER_LAYER - 5)
            blue_idxs.extend(range(base, base + 5))
        clusters = [(red_idxs, RED), (green_idxs, GREEN), (blue_idxs, BLUE)]

        # --- Highlight islands sequentially ---
        for idxs, color in clusters:
            glow_nodes = VGroup(*[
                Circle(radius=0.17, color=color)
                .set_stroke(width=3)
                .set_opacity(0.35)
                .move_to(pts[i])
                for i in idxs
            ])
            glow_edges = VGroup()
            for line in lines:
                p1, p2 = line.get_start_and_end()
                i1 = np.argmin(np.linalg.norm(pts - p1, axis=1))
                i2 = np.argmin(np.linalg.norm(pts - p2, axis=1))
                if i1 in idxs and i2 in idxs:
                    glow_edges.add(line.copy().set_color(color).set_opacity(0.5).set_stroke(width=1.5))
            self.add(glow_edges)
            self.play(*[dots[i].animate.set_color(color) for i in idxs], run_time=0.6)
            self.play(FadeIn(glow_nodes, scale=1.1), run_time=0.8)
            self.wait(2.3)
            self.play(FadeOut(glow_nodes, scale=1.05), run_time=0.8)
            self.wait(0.4)

        # --- Final composite glow ---
        final_glow = VGroup()
        for idxs, color in clusters:
            for i in idxs:
                g = Circle(radius=0.17, color=color).set_opacity(0.25).move_to(pts[i])
                final_glow.add(g)
        self.play(FadeIn(final_glow, scale=1.05), run_time=1.2)
        self.wait(2.5)

        outro = Text("Ramsey inevitability — structure emerges from sparse chaos",
                     color=TEAL_A).scale(0.43).to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(outro)
        self.wait(2.5)
