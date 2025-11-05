from manim import *
import itertools
import numpy as np

# ============================================================
# Ramsey Number R(3,3)=6 Video Animation
# Detailed Explanations | One Sentence per Screen | Fade Transitions
# Labels Dominant | Pigeonhole Highlight Verified Monochromatic
# Run: manim -pqh 1.py R33_FullVideo
# ============================================================

VERT_POS_ANGLES = [0, 1.2, 2.4, 3.65, 4.7, 5.5]

def fixed_edge_coloring():
    REDS = {
        (0,1),(0,3),(0,5),
        (1,2),(1,4),
        (2,3),
        (3,5),
        (4,5)
    }
    all_edges = {tuple(sorted(e)) for e in itertools.combinations(range(6),2)}
    return {e:(RED if e in REDS else BLUE) for e in all_edges}


class TwoPaneScene(Scene):

    def setup_panes(self,right_ratio=0.34,gap=0.3):
        W,H=config.frame_width,config.frame_height
        rw=W*right_ratio
        lw=W-rw-gap
        left=Rectangle(width=lw,height=H-0.5).set_stroke(opacity=0).to_edge(LEFT)
        right=Rectangle(width=rw,height=H-0.5).set_stroke(opacity=0).to_edge(RIGHT)
        sep=Line(left.get_right(),right.get_left(),stroke_opacity=0.15)
        self.add(sep)
        return left,right


    def make_k6(self,left_rect):
        center = left_rect.get_center()
        r = min(left_rect.width,left_rect.height)*0.4

        layout = {
            i:center+r*np.array([np.cos(a),np.sin(a),0])
            for i,a in enumerate(VERT_POS_ANGLES)
        }

        edges = list(itertools.combinations(range(6),2))
        g = Graph(
            vertices=list(range(6)),
            edges=edges,
            layout=layout,
            vertex_config={"radius":0.14, "fill_color":WHITE},
            edge_config={"stroke_width":3},
        )

        # ✅ Stronger visible labels
        for i in range(6):
            label = Text(str(i), font_size=32, weight=BOLD)
            label.set_stroke(BLACK, width=3, opacity=1.0)
            label.move_to(layout[i] + 0.22*UP)
            g[i].label = label

        return g

    def add_vertex_labels(self,g):
        for i in g.vertices:
            self.add(g[i].label)

    def apply_coloring(self,g,col):
        for e,c in col.items():
            g.edges[e].set_color(c)


    # ✅ Show each sentence separately, fade out before next
    def show_sentence(self, lines, right_rect, font_size=28,
                      wait_line=0.4, wait_sentence=5.0):

        group = VGroup(*[
            Text(l, font_size=font_size)
            .set_stroke(BLACK, width=1)
            .align_to(right_rect, LEFT)
            for l in lines
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)

        max_w = right_rect.width - 0.18
        if group.width > max_w:
            group.set_width(max_w)

        group.move_to(right_rect.get_left() + 0.1*RIGHT, LEFT)

        for m in group:
            self.add(m)
            self.play(FadeIn(m, shift=RIGHT), run_time=0.3)
            self.wait(wait_line)

        self.wait(wait_sentence)
        self.play(FadeOut(group, shift=LEFT), run_time=0.4)


    def mono_triangles(self,col):
        out=[]
        for a,b,c in itertools.combinations(range(6),3):
            e1 = (min(a,b),max(a,b))
            e2 = (min(a,c),max(a,c))
            e3 = (min(b,c),max(b,c))
            if col[e1]==col[e2]==col[e3]:
                out.append((a,b,c))
        return out


    def glow_tri(self,g,tri,color=YELLOW):
        a,b,c = tri
        glows = VGroup()
        for x,y in [(a,b),(a,c),(b,c)]:
            e = (min(x,y),max(x,y))
            seg = g.edges[e].copy().set_z_index(10)
            seg.set_stroke(color, width=10, opacity=0.95)
            glows.add(seg)
        return glows




class R33_FullVideo(TwoPaneScene):

    def construct(self):
        self.part_prob()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)
        self.part_pigeonhole()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)
        self.part_sat()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)
        self.part_conclusion()


    def part_prob(self):
        left,right = self.setup_panes()
        self.play(FadeIn(Text("Probabilistic Method", weight=BOLD).to_edge(UP)), run_time=0.6)

        g = self.make_k6(left)
        col = fixed_edge_coloring()
        self.play(Create(g), run_time=1.4)
        self.add_vertex_labels(g)
        self.apply_coloring(g,col)

        sentences = [
            ["In K6 every edge is colored", "either Red or Blue."],
            ["There are 20 triangles", "because 6 choose 3 equals 20."],
            ["Probability of a triangle", "being monochromatic is 1/4."],
            ["Expected number of mono triangles", "is 5 in every coloring."],
            ["Thus a monochromatic triangle", "must exist in every coloring."]
        ]
        for s in sentences:
            self.show_sentence(s, right)

        for tri in self.mono_triangles(col)[:2]:
            glow = self.glow_tri(g, tri)
            self.play(Create(glow), run_time=0.6)
            self.wait(0.6)
            self.play(FadeOut(glow), run_time=0.3)


    def part_pigeonhole(self):
        left,right = self.setup_panes()
        self.play(FadeIn(Text("Pigeonhole Principle", weight=BOLD).to_edge(UP)), run_time=0.6)

        g=self.make_k6(left)
        col=fixed_edge_coloring()
        self.apply_coloring(g,col)
        self.play(Create(g),run_time=1.2)
        self.add_vertex_labels(g)

        v = 0
        neigh = [1,2,3,4,5]
        redN = neigh[:3]
        blueN = neigh[3:]

        sentences = [
            ["Pick any vertex v.","It has 5 edges incident to it."],
            ["By pigeonhole principle,","at least 3 of these edges share a color."],
            ["Let those neighbors be a, b, c.","Consider the triangle among them."],
            ["Either that triangle is same color as edges to v","OR it is the other color"],
            ["Either way we get","a monochromatic triangle."]
        ]
        for s in sentences:
            self.show_sentence(s,right)

        # ✅ Choose a triangle that is TRULY monochromatic
        monos = self.mono_triangles(col)
        if monos:
            tri = monos[0]
            tri_color = col[(min(tri[0], tri[1]), max(tri[0], tri[1]))]
        else:
            tri = (0,1,2)
            tri_color = YELLOW

        glow=self.glow_tri(g,tri,color=tri_color)
        self.play(Create(glow),run_time=0.6)
        self.wait(0.6)
        self.play(FadeOut(glow),run_time=0.3)


    def part_sat(self):
        left,right = self.setup_panes()
        self.play(FadeIn(Text("SAT Verification", weight=BOLD).to_edge(UP)), run_time=0.6)

        g = self.make_k6(left)
        col=fixed_edge_coloring()
        self.apply_coloring(g,col)
        self.play(Create(g),run_time=1.2)
        self.add_vertex_labels(g)

        sentences = [
            ["Encode each edge","as a boolean variable."],
            ["Add clauses to forbid","all-red or all-blue triangles."],
            ["The CNF formula becomes UNSAT.", "No valid assignment exists."],
            ["SAT confirms combinatorics:", "a monochromatic triangle is inevitable."]
        ]
        for s in sentences:
            self.show_sentence(s,right)

        stamp=Text("UNSAT",color=RED,weight=BOLD).scale(1.3)
        rect=SurroundingRectangle(g,color=RED,buff=0.2)
        self.play(Create(rect),Write(stamp.move_to(g.get_center())),run_time=1.0)
        self.wait(0.4)


    def part_conclusion(self):
        left,right = self.setup_panes()
        self.play(FadeIn(Text("Conclusion", weight=BOLD).to_edge(UP)), run_time=0.6)

        g=self.make_k6(left)
        col=fixed_edge_coloring()
        self.apply_coloring(g,col)
        self.play(Create(g),run_time=1.3)
        self.add_vertex_labels(g)

        sentences = [
            ["Expected value argument shows","many mono triangles appear."],
            ["Pigeonhole principle forces one", "in every 2-coloring."],
            ["SAT solver verifies there is", "no coloring without mono triangle."],
            ["Thus the Ramsey number", "R(3,3) = 6 ✅"]
        ]
        for s in sentences:
            self.show_sentence(s,right)

        badge=Text("R(3,3)=6 ✅",weight=BOLD,color=YELLOW).scale(1.2)
        badge.next_to(g,DOWN)
        self.play(Write(badge),run_time=1.0)
        self.wait(0.5)
