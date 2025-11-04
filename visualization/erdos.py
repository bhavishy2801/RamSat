from manim import *
import random, math

class ErdosProbabilisticLowerBound(ThreeDScene):
    def construct(self):
        # --- Setup ---
        self.camera.background_color = "#0b0b10"
        title = Tex(r"Erdős Probabilistic Method --- Lower Bound", color=YELLOW).scale(0.8).to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        self.wait(0.5)

        # --- Graph parameters ---
        n_nodes = 10
        radius = 2.3
        stroke_opacity = 0.45
        node_radius = 0.06

        # Distribute nodes on a 3D sphere (golden spiral pattern)
        nodes = []
        for i in range(n_nodes):
            theta = math.acos(1 - 2 * (i + 0.5) / n_nodes)
            phi = math.pi * (1 + 5**0.5) * i
            x = radius * math.cos(phi) * math.sin(theta)
            y = radius * math.sin(phi) * math.sin(theta)
            z = radius * math.cos(theta)
            nodes.append(np.array([x, y, z]))

        # Create node spheres
        vertices = [Sphere(center=p, radius=node_radius, color=WHITE) for p in nodes]
        vertex_group = VGroup(*vertices)
        self.play(FadeIn(vertex_group, lag_ratio=0.1, run_time=2))
        self.wait(0.5)

        # Function to generate random colored edges
        def get_random_edges():
            edges = []
            for i in range(n_nodes):
                for j in range(i + 1, n_nodes):
                    color = random.choice([RED, BLUE])
                    edge = Line3D(nodes[i], nodes[j], thickness=0.015, color=color).set_opacity(stroke_opacity)
                    edges.append(edge)
            return VGroup(*edges)

        # --- Create edges and rotate the scene ---
        edge_group = get_random_edges()
        self.play(Create(edge_group), run_time=3)
        self.wait(0.5)

        # Enable gentle camera rotation
        self.move_camera(phi=70 * DEGREES, theta=-60 * DEGREES, run_time=2)
        self.begin_ambient_camera_rotation(rate=0.2)  # slow and smooth rotation

        # --- Slow probabilistic recolor transitions ---
        for _ in range(6):
            new_edges = get_random_edges()
            self.play(Transform(edge_group, new_edges), run_time=2.5)
        self.wait(1)

        # --- Fade to "expected value" curve in 2D frame ---
        self.stop_ambient_camera_rotation()
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, run_time=2)
        self.play(FadeOut(edge_group, vertex_group))

        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 1, 0.2],
            x_length=6,
            y_length=3,
            axis_config={"color": GREY_B, "stroke_width": 2},
        ).to_edge(DOWN).shift(UP * 0.5)

        curve = axes.plot(lambda x: math.exp(-((x - 2.5) ** 2) / 1.5), color=BLUE, stroke_width=4)
        shaded = axes.get_area(curve, x_range=[3.5, 5], color=RED).set_opacity(0.4)
        threshold_line = axes.get_vertical_line(axes.c2p(3.5, 0.3), color=YELLOW, stroke_width=3)
        threshold_text = MathTex(r"E[X] < 1", color=YELLOW).next_to(axes, UP)

        self.play(Create(axes), Create(curve), FadeIn(shaded), GrowFromCenter(threshold_line), Write(threshold_text))
        self.wait(1.5)
        self.play(FadeOut(shaded, run_time=1.5))
        self.wait(0.5)

        existence_text = Tex("Existence without construction", color=GREEN).scale(0.9).next_to(axes, DOWN)
        self.play(Write(existence_text))
        self.wait(1)

        # --- Return to 3D: “Erdős’ Lower Bound” scene ---
        self.play(FadeOut(axes), FadeOut(curve), FadeOut(threshold_line), FadeOut(threshold_text), FadeOut(existence_text))
        final_edges = get_random_edges()
        self.play(FadeIn(vertex_group), Create(final_edges, lag_ratio=0.05, run_time=3))
        self.wait(0.5)
        self.begin_ambient_camera_rotation(rate=0.15)

        lower_text = Tex("Erdős’ Lower Bound", color=GREEN).scale(0.9).to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(lower_text)
        self.play(Write(lower_text))
        self.wait(3)

        # --- Clean exit ---
        self.stop_ambient_camera_rotation()
        self.play(FadeOut(final_edges), FadeOut(vertex_group), FadeOut(lower_text), FadeOut(title))