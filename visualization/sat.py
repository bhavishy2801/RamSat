from manim import *
import itertools
import math
import random



# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------



def circular_layout(n, radius=3.0, start_angle=PI/2):
    """Return n points on a circle (for K_n)."""
    return [
        radius * np.array([
            math.cos(start_angle + 2 * math.pi * i / n),
            math.sin(start_angle + 2 * math.pi * i / n),
            0,
        ])
        for i in range(n)
    ]



def complete_graph_edges(vertices):
    """All undirected edges (i<j) from list of Dot mobjects."""
    idx_pairs = list(itertools.combinations(range(len(vertices)), 2))
    return idx_pairs



def edge_key(i, j):
    return (i, j) if i < j else (j, i)



def clique_indices(n, k):
    """All k-cliques by index (combinations of k distinct vertices)."""
    return list(itertools.combinations(range(n), k))



# ------------------------------------------------------------
# Main Scene
# ------------------------------------------------------------



class SATRamseyVerification(Scene):
    def construct(self):
        self.camera.background_color = "#0b0b10"


        title = Tex(r"SAT-Based Computational Verification of Ramsey Numbers", color=YELLOW).scale(0.7)
        subtitle = Tex(r"Edges $\leftrightarrow$ Boolean variables \quad Constraints forbid monochromatic cliques", color=GRAY_B).scale(0.45)
        title.to_edge(UP, buff=0.2)
        subtitle.next_to(title, DOWN, buff=0.15)


        self.play(FadeIn(title, shift=UP), Write(subtitle))
        self.wait(0.5)


        # --------------------------------------------------------
        # Layout: Left = K_n visual; Right = "SAT Solver" window
        # --------------------------------------------------------
        left_panel = Rectangle(width=6.0, height=5.2, stroke_color=GRAY_B, fill_color=BLACK, fill_opacity=0.15)
        right_panel = Rectangle(width=5.5, height=5.2, stroke_color=GRAY_B, fill_color=BLACK, fill_opacity=0.15)
        
        panels = VGroup(left_panel, right_panel).arrange(RIGHT, buff=0.3).shift(0.4*DOWN)


        left_header = Tex(r"Graph View: $K_n$", color=BLUE_A).scale(0.5).next_to(left_panel.get_top(), DOWN, buff=0.15)
        right_header = Tex(r"SAT Solver", color=BLUE_A).scale(0.55).next_to(right_panel.get_top(), DOWN, buff=0.15)


        self.play(FadeIn(left_panel, shift=DOWN), FadeIn(right_panel, shift=DOWN))
        self.play(Write(left_header), Write(right_header))


        # --------------------------------------------------------
        # Build K_n with n=6
        # --------------------------------------------------------
        n = 6
        vertex_positions = circular_layout(n, radius=1.8)
        vertices = VGroup(*[Dot(pos, radius=0.07, color=WHITE) for pos in vertex_positions])
        labels = VGroup(*[
            Tex(str(i+1)).scale(0.45).next_to(vertices[i], 0.35*OUT + 0.35*RIGHT if vertex_positions[i][0] >= 0 else 0.35*OUT + 0.35*LEFT)
            for i in range(n)
        ])
        graph_group = VGroup(vertices, labels).move_to(left_panel.get_center()).shift(0.2*DOWN)


        self.play(FadeIn(vertices, scale=0.9), FadeIn(labels, shift=0.1*UP))
        self.wait(0.25)


        # Edges
        idx_pairs = complete_graph_edges(vertices)
        edges = {}
        edge_lines = VGroup()
        for (i, j) in idx_pairs:
            line = Line(vertices[i].get_center(), vertices[j].get_center(), stroke_width=2.0, color=GRAY_D, z_index=-1)
            edges[edge_key(i, j)] = line
            edge_lines.add(line)
        self.play(LaggedStart(*[Create(line) for line in edge_lines], lag_ratio=0.02))
        self.wait(0.25)


        # --------------------------------------------------------
        # SAT Variables and Clauses
        # --------------------------------------------------------
        var_expl = Tex(
            r"Variables: $x_{ij}\in\{0,1\}$ per edge \\",
            r"$x_{ij}=1\Rightarrow \text{red}$, $x_{ij}=0\Rightarrow \text{blue}$",
            tex_environment="flushleft"
        ).scale(0.48)
        var_expl.set_color(GRAY_B)
        var_expl.next_to(right_header, DOWN, buff=0.25, aligned_edge=LEFT)
        var_expl.align_to(right_panel.get_left(), LEFT).shift(0.2*RIGHT)


        self.play(Write(var_expl))


        # Clause templates
        clause_title = Tex(r"Constraints (no mono $K_3$):", color=GRAY_B).scale(0.48)
        clause_title.next_to(var_expl, DOWN, buff=0.25, aligned_edge=LEFT)


        self.play(Write(clause_title))


        clause_examples = VGroup(
            Tex(r"No red $\triangle$: $(\lnot x_{ab}) \lor (\lnot x_{bc}) \lor (\lnot x_{ac})$").scale(0.4),
            Tex(r"No blue $\triangle$: $x_{ab} \lor x_{bc} \lor x_{ac}$").scale(0.4),
        )
        clause_examples.arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(clause_title, DOWN, aligned_edge=LEFT, buff=0.15)


        self.play(LaggedStart(*[Write(t) for t in clause_examples], lag_ratio=0.15))
        self.wait(0.4)


        # FIXED: Console properly positioned inside right panel
        console = Rectangle(width=4.4, height=2.0, stroke_color=GRAY_D, fill_color=BLACK, fill_opacity=0.4)
        console.next_to(clause_examples, DOWN, buff=0.25, aligned_edge=LEFT)
        
        self.play(FadeIn(console, shift=DOWN))


        # FIXED: Console lines properly formatted and positioned
        console_lines_text = [
            "encode(K_6) -> 40 vars",
            "propagate() -> search",
            "branch() -> x_12=1",
            "conflict() -> back",
            "propagate() -> fail",
            "UNSAT"
        ]
        console_lines = VGroup(*[Text(t, font_size=13, color=GRAY_B, font="Monospace") for t in console_lines_text])
        
        # Arrange console lines vertically
        console_lines.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        console_lines.move_to(console.get_center())
        console_lines.align_to(console.get_left(), LEFT).shift(0.2*RIGHT)


        for line in console_lines[:-1]:
            self.play(FadeIn(line, target_position=line.get_center()+0.03*UP), run_time=0.2)
        
        unsat_line = console_lines[-1]
        unsat_line.set_color(RED)
        self.play(FadeIn(unsat_line, scale=1.05), Flash(unsat_line, color=RED, flash_radius=0.5))
        self.wait(0.3)


        # --------------------------------------------------------
        # Visual link: edge coloring
        # --------------------------------------------------------
        random.seed(7)
        assignment = {}
        for (i, j) in idx_pairs:
            assignment[edge_key(i, j)] = random.choice([0, 1])


        anims = []
        for (i, j) in idx_pairs:
            color = RED if assignment[edge_key(i, j)] == 1 else BLUE
            anims.append(edges[edge_key(i, j)].animate.set_color(color))
        self.play(LaggedStart(*anims, lag_ratio=0.01), run_time=0.8)


        tri_cliques = clique_indices(n, 3)
        tri_found = None
        for (a, b, c) in tri_cliques:
            colors = [
                RED if assignment[edge_key(a, b)] else BLUE,
                RED if assignment[edge_key(b, c)] else BLUE,
                RED if assignment[edge_key(a, c)] else BLUE,
            ]
            if colors[0] == colors[1] == colors[2]:
                tri_found = (a, b, c, colors[0])
                break


        if tri_found is not None:
            a, b, c, mono_color = tri_found
            tri_edges = VGroup(
                edges[edge_key(a, b)],
                edges[edge_key(b, c)],
                edges[edge_key(a, c)],
            )
            halo = SurroundingRectangle(tri_edges, color=mono_color, buff=0.15, corner_radius=0.1)
            self.play(Create(halo), Indicate(tri_edges, color=mono_color))
            
            # FIXED: Position text BELOW left panel to avoid overlap
            forbid_text = Tex(
                r"Forbidden mono $K_3$ found",
                color=mono_color
            ).scale(0.5)
            forbid_text.next_to(left_panel, DOWN, buff=0.2)
            
            self.play(Write(forbid_text))
            self.wait(0.3)
            self.play(FadeOut(halo), FadeOut(forbid_text))


        # FIXED: SAT/UNSAT interpretation positioned BELOW right panel
        sat_text = Tex(r"\textbf{SAT} $\Rightarrow R(s,t) > n$", color=GREEN).scale(0.5)
        unsat_text = Tex(r"\textbf{UNSAT} $\Rightarrow R(s,t) \le n$", color=RED).scale(0.5)
        
        interp_group = VGroup(sat_text, unsat_text).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        interp_group.next_to(right_panel, DOWN, buff=0.2, aligned_edge=LEFT)


        self.play(FadeIn(sat_text, shift=UP), FadeIn(unsat_text, shift=UP))
        self.wait(0.5)


        # --------------------------------------------------------
        # FIXED: Demonstrate R(3,3) = 6 - properly positioned below panels with reduced sizes
        # --------------------------------------------------------
        r33 = Tex(r"$R(3,3)=6$", color=YELLOW).scale(0.52)
        r33.next_to(left_panel, DOWN, buff=0.15)
        self.play(Write(r33))
        self.wait(0.2)


        n5_note = Tex(r"$n=5$: SAT", color=GREEN).scale(0.42)
        n5_note.next_to(r33, DOWN, buff=0.1)
        self.play(Write(n5_note))


        # Temporarily show K5
        self.play(FadeOut(edge_lines), FadeOut(vertices), FadeOut(labels))
        n5 = 5
        pos5 = circular_layout(n5, radius=1.8)
        vertices5 = VGroup(*[Dot(pos, radius=0.07, color=WHITE) for pos in pos5])
        labels5 = VGroup(*[
            Tex(str(i+1)).scale(0.45).next_to(vertices5[i], 0.35*OUT + 0.35*RIGHT if pos5[i][0] >= 0 else 0.35*OUT + 0.35*LEFT)
            for i in range(n5)
        ])
        vg5 = VGroup(vertices5, labels5).move_to(left_panel.get_center()).shift(0.2*DOWN)
        self.play(FadeIn(vertices5, labels5, shift=0.2*UP))


        idx5 = list(itertools.combinations(range(n5), 2))
        edges5 = {}
        lines5 = VGroup()
        for (i, j) in idx5:
            line = Line(vertices5[i].get_center(), vertices5[j].get_center(), stroke_width=2.0, color=GRAY_D, z_index=-1)
            edges5[edge_key(i, j)] = line
            lines5.add(line)
        self.play(LaggedStart(*[Create(line) for line in lines5], lag_ratio=0.02))


        cycle = [(0,1),(1,2),(2,3),(3,4),(4,0)]
        for (i, j) in idx5:
            if edge_key(i, j) in [edge_key(*p) for p in cycle]:
                edges5[edge_key(i, j)].set_color(RED)
            else:
                edges5[edge_key(i, j)].set_color(BLUE)
        self.play(*[edges5[e].animate.set_stroke(width=2.8) for e in edges5])
        self.wait(0.5)


        # FIXED: Position n=6 note properly below n=5 note with reduced size
        n6_note = Tex(r"$n=6$: UNSAT", color=RED).scale(0.42)
        n6_note.next_to(n5_note, DOWN, buff=0.1)
        
        self.play(Write(n6_note))
        self.wait(0.2)


        # Return to K6
        self.play(FadeOut(lines5), FadeOut(vertices5), FadeOut(labels5))


        vertices = VGroup(*[Dot(pos, radius=0.07, color=WHITE) for pos in vertex_positions])
        labels = VGroup(*[
            Tex(str(i+1)).scale(0.45).next_to(vertices[i], 0.35*OUT + 0.35*RIGHT if vertex_positions[i][0] >= 0 else 0.35*OUT + 0.35*LEFT)
            for i in range(n)
        ])
        VGroup(vertices, labels).move_to(left_panel.get_center()).shift(0.2*DOWN)
        self.play(FadeIn(vertices, labels, shift=0.1*UP))


        edges = {}
        edge_lines = VGroup()
        for (i, j) in idx_pairs:
            line = Line(vertices[i].get_center(), vertices[j].get_center(), stroke_width=2.0, color=GRAY_D, z_index=-1)
            edges[edge_key(i, j)] = line
            edge_lines.add(line)
        self.play(LaggedStart(*[Create(l) for l in edge_lines], lag_ratio=0.02))


        attempts = 2
        for attempt_num in range(attempts):
            assignment = {}
            for (i, j) in idx_pairs:
                assignment[edge_key(i, j)] = random.choice([0, 1])
            self.play(*[
                edges[edge_key(i, j)].animate.set_color(RED if assignment[edge_key(i, j)] else BLUE)
                for (i, j) in idx_pairs
            ], run_time=0.6)


            tri_found = None
            for (a, b, c) in tri_cliques:
                colors = [
                    RED if assignment[edge_key(a, b)] else BLUE,
                    RED if assignment[edge_key(b, c)] else BLUE,
                    RED if assignment[edge_key(a, c)] else BLUE,
                ]
                if colors[0] == colors[1] == colors[2]:
                    tri_found = (a, b, c, colors[0])
                    break


            if tri_found is not None:
                a, b, c, mono_color = tri_found
                tri_edges = VGroup(
                    edges[edge_key(a, b)],
                    edges[edge_key(b, c)],
                    edges[edge_key(a, c)],
                )
                self.play(Indicate(tri_edges, color=mono_color), Flash(tri_edges[0], color=mono_color, flash_radius=0.3))
                self.wait(0.15)


        # Final statement
        self.play(FadeOut(n5_note), FadeOut(n6_note))
        
        final_text = Tex(
            r"In any 6 people: 3 friends \\",
            r"\emph{or} 3 strangers",
            color=YELLOW
        ).scale(0.48)
        final_text.next_to(left_panel, DOWN, buff=0.15)


        self.play(Transform(r33, final_text))
        self.wait(1.0)


        # Graceful outro
        to_fade = [
            subtitle, left_panel, right_panel, left_header, right_header,
            vertices, labels, edge_lines, var_expl, clause_title, clause_examples,
            console, console_lines, sat_text, unsat_text, r33, interp_group
        ]
        
        self.play(
            *[FadeOut(mob) for mob in to_fade],
            title.animate.move_to(ORIGIN),
            run_time=0.8
        )
        
        thanks = Tex(r"Logic $\cdot$ Probability $\cdot$ Computation", color=GRAY_B).scale(0.65)
        thanks.next_to(title, DOWN, buff=0.3)
        self.play(Write(thanks))
        self.wait(1.0)
        self.play(FadeOut(title), FadeOut(thanks))
