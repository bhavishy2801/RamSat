from manim import *
import itertools
import random
import math
import numpy as np

# 3D Social Media Clusters visualization (Ramsey-inspired)
# Smaller scale, limited rotation (~60 degrees), deterministic random layout of nodes and edges.
# Highlights detected monochromatic (Ramsey-style) triangles and dense micro-clusters in green/yellow.

class Ramsey3D(ThreeDScene):
    def construct(self):
        title = Title("Social Media Clusters -- Ramsey Theory")
        self.add(title)

        N = 200
        EDGE_COUNT = 200
        SEED = 42
        POINT_SCALE = 0.05  # smaller
        R = 2.0  # smaller spatial cube radius

        random.seed(SEED)

        # Generate deterministic random 3D points within a cube
        points = [np.array([random.uniform(-R, R), random.uniform(-R, R), random.uniform(-R, R)]) for _ in range(N)]
        dots = VGroup(*[Dot(point=pt, radius=POINT_SCALE) for pt in points])

        # A few labels for first 8 nodes only
        labels = VGroup(*[MathTex(str(i + 1)).scale(0.4).next_to(points[i], UP * 0.15) for i in range(min(8, N))])

        # Deterministically choose edges
        all_pairs = list(itertools.combinations(range(N), 2))
        random.shuffle(all_pairs)
        chosen_pairs = all_pairs[:EDGE_COUNT]

        # Assign deterministic red/blue coloring
        color_map = {}
        edges = {}
        edge_group = VGroup()
        for (i, j) in chosen_pairs:
            col = BLUE if random.random() < 0.5 else RED
            color_map[(i, j)] = col
            line = Line(points[i], points[j], stroke_width=1.3, color=col)
            edges[(i, j)] = line
            edge_group.add(line)

        graph_group = VGroup(edge_group, dots, labels).center()

        # Add 3D bounding cube for spatial reference
        wireframe = VGroup()
        cube_points = [np.array([sx * R, sy * R, sz * R]) for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)]
        for a, b in itertools.combinations(cube_points, 2):
            if np.count_nonzero((a > 0) != (b > 0)) == 1:
                line = Line(a, b, stroke_width=0.5, color=GREY_A)
                wireframe.add(line)

        self.add(wireframe)
        self.play(LaggedStartMap(FadeIn, dots, lag_ratio=0.005), run_time=2.0)
        self.play(Create(edge_group), run_time=2.0)
        self.play(*[Write(l) for l in labels], run_time=0.5)

        total_rotation = PI / 3  # about 60 degrees total rotation
        steps = 40
        rot_per_step = total_rotation / steps

        # Detect monochromatic triangles (Ramsey) and local clusters (dense mini-groups)
        def find_mono_triangle(cmap):
            adj = {BLUE: {}, RED: {}}
            for (a, b), c in cmap.items():
                adj[c].setdefault(a, set()).add(b)
                adj[c].setdefault(b, set()).add(a)
            for color in (BLUE, RED):
                for a in adj[color]:
                    for b in adj[color][a]:
                        common = adj[color][a].intersection(adj[color].get(b, set()))
                        for c in common:
                            if a < b < c:
                                return (a, b, c), color
            return None, None

        def find_micro_clusters(edges_dict, threshold=4):
            node_degree = {}
            for (a, b) in edges_dict.keys():
                node_degree[a] = node_degree.get(a, 0) + 1
                node_degree[b] = node_degree.get(b, 0) + 1
            high_degree_nodes = [k for k, v in node_degree.items() if v >= threshold]
            if len(high_degree_nodes) < 3:
                return []
            clusters = []
            for i in range(0, len(high_degree_nodes) - 3, 3):
                clusters.append(high_degree_nodes[i:i + 3])
            return clusters

        tri, tri_col = find_mono_triangle(color_map)
        clusters = find_micro_clusters(edges)

        # Animate rotation and highlight structures
        for k in range(steps):
            self.play(Rotate(graph_group, angle=rot_per_step, axis=UP), run_time=0.15)
            if k == steps // 3 and tri is not None:
                a, b, c = tri
                tri_face = Polygon(points[a], points[b], points[c])
                tri_face.set_fill(tri_col, opacity=0.25)
                tri_face.set_stroke(width=0)
                self.play(Create(tri_face), run_time=0.8)
            if k == steps // 2 and clusters:
                cluster_faces = []
                for cluster in clusters[:5]:
                    if len(cluster) >= 3:
                        pts = [points[i] for i in cluster[:3]]
                        col = GREEN if random.random() < 0.5 else YELLOW
                        face = Polygon(*pts)
                        face.set_fill(col, opacity=0.25)
                        face.set_stroke(width=0)
                        cluster_faces.append(face)
                self.play(*[Create(f) for f in cluster_faces], run_time=1.2)

        end_note = Tex(r"Highlighted real clusters (green/yellow) \& Ramsey triangles (red/blue)")
        end_note.scale(0.6)
        end_note.to_edge(DOWN)
        self.play(Write(end_note))
        self.wait(2)