from manim import *
import random as rand

class RamseyTheory(Scene):
    def construct(self):
        # Seed for reproducibility - fixed "random" dataset
        rand.seed(42)
        
        # Create many vertices scattered chaotically
        n_vertices = 25
        vertices = VGroup()
        positions = []
        
        # Generate scattered, asymmetric positions
        rand.seed(42)
        for i in range(n_vertices):
            x = rand.uniform(-5, 5)
            y = rand.uniform(-2.5, 2.5)
            pos = np.array([x, y, 0])
            positions.append(pos)
            vertex = Dot(pos, radius=0.08, color=WHITE, fill_opacity=1, z_index=2)
            vertices.add(vertex)
        
        # Create chaotic web of random connections
        edges = VGroup()
        edge_data = []
        
        # Create random connections (not complete graph)
        rand.seed(42)
        for i in range(n_vertices):
            # Each vertex connects to 3-6 random other vertices
            n_connections = rand.randint(3, 6)
            possible_targets = [j for j in range(n_vertices) if j != i and j > i]
            if possible_targets:
                targets = rand.sample(possible_targets, min(n_connections, len(possible_targets)))
                for j in targets:
                    edge = Line(positions[i], positions[j], stroke_width=1.5)
                    color = RED if rand.random() > 0.5 else BLUE
                    edge.set_stroke(color=color, opacity=0.6)
                    edges.add(edge)
                    edge_data.append((i, j, color, edge))
        
        # Find multiple triangles in our "random" data (we'll engineer them)
        # Red triangles
        red_triangle_1 = [3, 7, 12]
        red_triangle_2 = [5, 15, 20]
        
        # Blue triangles
        blue_triangle_1 = [2, 8, 18]
        blue_triangle_2 = [10, 14, 22]
        
        all_triangles = [
            (red_triangle_1, RED),
            (red_triangle_2, RED),
            (blue_triangle_1, BLUE),
            (blue_triangle_2, BLUE)
        ]
        
        # Store triangle data
        triangle_data = {}
        
        for triangle_verts, color in all_triangles:
            pairs = [
                (triangle_verts[0], triangle_verts[1]),
                (triangle_verts[0], triangle_verts[2]),
                (triangle_verts[1], triangle_verts[2])
            ]
            triangle_data[tuple(triangle_verts)] = (pairs, color)
            
            # Force these specific edges to have the right color
            for i, j, edge_color, edge in edge_data:
                if (i, j) in pairs or (j, i) in pairs:
                    edge.set_color(color)
            
            # Add triangle edges if they don't exist
            existing_pairs = [(i, j) for i, j, _, _ in edge_data]
            for pair in pairs:
                if pair not in existing_pairs and (pair[1], pair[0]) not in existing_pairs:
                    edge = Line(positions[pair[0]], positions[pair[1]], stroke_width=1.5)
                    edge.set_stroke(color=color, opacity=0.6)
                    edges.add(edge)
                    edge_data.append((pair[0], pair[1], color, edge))
        
        # Title
        title = Text("Ramsey Theory", font_size=40, weight=BOLD)
        title.to_edge(UP).set_z_index(10)
        
        # Phase 1: Show the chaotic web (0-6 seconds)
        subtitle1 = Text("A chaotic web of connections...", font_size=28, color=GRAY)
        subtitle1.next_to(title, DOWN, buff=0.3).set_z_index(10)
        
        self.play(FadeIn(title), run_time=0.8)
        self.play(Write(subtitle1), run_time=1)
        
        # Show vertices appearing randomly
        vertex_indices = list(range(len(vertices)))
        rand.shuffle(vertex_indices)
        
        vertex_animations = [FadeIn(vertices[i]) for i in vertex_indices]
        self.play(AnimationGroup(*vertex_animations, lag_ratio=0.03), run_time=2)
        
        # Show edges appearing chaotically
        edge_indices = list(range(len(edges)))
        rand.shuffle(edge_indices)
        
        edge_animations = [Create(edges[i]) for i in edge_indices]
        self.play(AnimationGroup(*edge_animations, lag_ratio=0.02), run_time=2.5)
        
        self.wait(0.7)
        
        # Phase 2: The revelation - reveal triangles one by one (6-16 seconds)
        self.play(FadeOut(subtitle1), run_time=0.5)
        
        subtitle2 = Text("But patterns are inevitable...", font_size=28, color=YELLOW)
        subtitle2.next_to(title, DOWN, buff=0.3).set_z_index(10)
        self.play(Write(subtitle2), run_time=1)
        
        # Collect all triangle edges and vertices
        all_triangle_edges = []
        all_triangle_vertices = set()
        
        for triangle_verts, color in all_triangles:
            pairs, _ = triangle_data[tuple(triangle_verts)]
            for i, j, edge_color, edge in edge_data:
                if (i, j) in pairs or (j, i) in pairs:
                    all_triangle_edges.append(edge)
            all_triangle_vertices.update(triangle_verts)
        
        # Fade everything except triangles
        non_triangle_edges = [edge for edge in edges if edge not in all_triangle_edges]
        non_triangle_vertices = [vertices[i] for i in range(n_vertices) if i not in all_triangle_vertices]
        
        self.play(
            *[edge.animate.set_opacity(0.06) for edge in non_triangle_edges],
            *[v.animate.set_opacity(0.15).scale(0.6) for v in non_triangle_vertices],
            run_time=2
        )
        
        # Reveal each triangle one by one
        for idx, (triangle_verts, color) in enumerate(all_triangles):
            pairs, _ = triangle_data[tuple(triangle_verts)]
            
            # Get edges for this triangle
            triangle_edges = []
            for i, j, edge_color, edge in edge_data:
                if (i, j) in pairs or (j, i) in pairs:
                    triangle_edges.append(edge)
            
            # Get vertices for this triangle
            triangle_vertex_dots = [vertices[i] for i in triangle_verts]
            
            # Highlight this triangle
            self.play(
                *[edge.animate.set_stroke(width=5, opacity=1) for edge in triangle_edges],
                *[v.animate.set_color(color).scale(2.5) for v in triangle_vertex_dots],
                run_time=1.2
            )
            
            # Add glow
            for edge in triangle_edges:
                glow = edge.copy().set_stroke(width=10, opacity=0.25)
                self.add(glow)
            
            self.wait(0.4)
        
        self.wait(0.8)
        
        # Phase 3: The message (16-20 seconds)
        self.play(FadeOut(subtitle2), run_time=0.5)
        
        conclusion = VGroup(
            Text("Multiple ordered patterns", font_size=26, weight=BOLD, color=YELLOW),
            Text("emerge from chaos", font_size=26)
        ).arrange(DOWN, buff=0.25)
        conclusion.to_edge(DOWN, buff=1).set_z_index(10)
        
        self.play(FadeIn(conclusion, shift=UP), run_time=1.5)
        
        # Pulse all triangles together
        all_triangle_vertex_dots = [vertices[i] for i in all_triangle_vertices]
        self.play(
            *[v.animate.scale(1.15) for v in all_triangle_vertex_dots],
            rate_func=there_and_back,
            run_time=1
        )
        
        self.wait(1)
        
        # Fade everything
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)