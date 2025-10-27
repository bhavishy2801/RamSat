from manim import *

class ErdosProb(Scene):
    def construct(self):
        title = Text("Erdős Probabilistic Method").scale(0.8)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        graph = Axes(
            x_range=[3, 10],
            y_range=[0, 1],
            axis_config={"include_numbers": True}
        )
        labels = graph.get_axis_labels("n", "P(Avoid Mono Triangles)")
        self.play(Create(graph), Write(labels))

        curve = graph.plot(lambda x: np.exp(-0.5*(x-3)), color=RED)
        self.play(Create(curve))
        self.wait(1)

        label = Tex("Probability → 0 as n increases").next_to(graph, DOWN)
        self.play(Write(label))
        self.wait(2)
