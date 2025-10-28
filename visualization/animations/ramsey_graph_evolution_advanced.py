from manim import *
import numpy as np
import random
import itertools

class RamseyGraphEvolutionAdvanced(Scene):
    def construct(self):
        # --- TITLE ---
        title = Text("Evolution of Ramsey Graphs", font="Helvetica", weight=BOLD).scale(0.9)
        subtitle = Text("Random Edge Colorings and Ramsey Probability", font="Helvetica").scale(0.5)
        subtitle.next_to(title, DOWN)
        self.play(Write(title), FadeIn(subtitle))
        self.wait(1)
        self.play(title.animate.to_edge(UP), FadeOut(subtitle))

        # --- CREATE GRAPH NODES ---
        n = 6
        radius = 3
        points = [
            Dot(radius * np.array([np.cos(2 * np.pi * i / n), np.sin(2 * np.pi * i / n), 0]), color=WHITE)
            for i in range(n)
        ]
        labels = [
            Text(str(i + 1), font="Consolas").scale(0.4).next_to(points[i], np.sign(points[i].get_center()))
            for i in range(n)
        ]
        self.play(LaggedStart(*[FadeIn(p) for p in points], lag_ratio=0.1))
        self.play(LaggedStart(*[FadeIn(l) for l in labels], lag_ratio=0.05))

        # --- DRAW ALL EDGES ---
        all_edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
        lines = {e: Line(points[e[0]].get_center(), points[e[1]].get_center(), color=GREY, stroke_width=2.5)
                 for e in all_edges}
        self.play(LaggedStart(*[Create(line) for line in lines.values()], lag_ratio=0.03))
        self.wait(0.5)

        # --- EXPERIMENT TITLE ---
        exp_title = Text("Ramsey Probability Experiment", color=ORANGE).scale(0.55)
        exp_title.to_edge(DOWN)
        self.play(FadeIn(exp_title))

        # --- COUNTERS ---
        trial_count = Integer(0, color=WHITE).scale(0.5)
        success_count = Integer(0, color=YELLOW).scale(0.5)
        total_label = Text("Trials:", font="Consolas").scale(0.4).next_to(trial_count, LEFT)
        success_label = Text("With Monochromatic Triangle:", font="Consolas").scale(0.4).next_to(success_count, LEFT)

        counter_group = VGroup(total_label, trial_count, success_label, success_count).arrange(DOWN, aligned_edge=LEFT)
        counter_group.to_corner(DR)
        self.play(FadeIn(counter_group))

        # --- RUN SIMULATION ---
        trials = 10
        successes = 0
        probs = []  # store success probabilities for the bar chart

        for t in range(1, trials + 1):
            # Random edge coloring
            for (i, j), line in lines.items():
                new_color = random.choice([RED, BLUE])
                line.set_color(new_color)
            self.wait(0.3)

            # Check triangles for monochromatic triplets
            found = False
            for (a, b, c) in itertools.combinations(range(n), 3):
                colors = [lines[tuple(sorted(e))].get_color() for e in [(a, b), (b, c), (a, c)]]
                if colors[0] == colors[1] == colors[2]:
                    found = True
                    center = sum([points[x].get_center() for x in (a, b, c)]) / 3
                    highlight = Circle(radius=1.2, color=YELLOW, stroke_width=3).move_to(center)
                    self.play(Create(highlight), run_time=0.3)
                    self.wait(0.3)
                    self.play(FadeOut(highlight))
                    break

            # Update counters
            if found:
                successes += 1
                self.play(success_count.animate.set_value(successes), run_time=0.2)
            self.play(trial_count.animate.set_value(t), run_time=0.2)
            probs.append(successes / t)
            self.wait(0.1)

        # --- DISPLAY FINAL PROBABILITY ---
        prob = successes / trials
        prob_text = Text(f"Empirical Probability ≈ {prob:.2f}", color=GREEN).scale(0.6)
        prob_text.next_to(exp_title, UP)
        self.play(FadeIn(prob_text))
        self.wait(1.5)

        # --- CLEAN UP GRAPH FOR STATISTICS VISUALIZATION ---
        self.play(*[FadeOut(mobj) for mobj in points + labels + list(lines.values()) + [counter_group, exp_title]])
        self.wait(0.5)

        # --- DISPLAY EMPIRICAL FORMULA ---
        formula = MathTex(
            r"P_{empirical} = \frac{\text{Number of successes}}{\text{Total trials}}",
            color=YELLOW
        ).scale(0.8)
        self.play(Write(formula))
        self.wait(2)
        self.play(formula.animate.to_edge(UP))

        # --- CREATE BAR CHART OF PROBABILITIES ---
        x_labels = [str(i) for i in range(1, trials + 1)]
        bar_chart = BarChart(
            values=probs,
            bar_names=x_labels,
            y_range=[0, 1.1, 0.2],
            y_length=4,
            x_length=8,
            bar_width=0.3,
            color=BLUE,
        )
        bar_chart.next_to(formula, DOWN)
        self.play(Create(bar_chart))
        self.wait(1)

        # --- LABELS ---
        label_x = Text("Trial Number", font="Helvetica").scale(0.5).next_to(bar_chart, DOWN)
        label_y = Text("Empirical Probability", font="Helvetica").scale(0.5).next_to(bar_chart, LEFT)
        self.play(FadeIn(label_x), FadeIn(label_y))
        self.wait(1)

        # --- FINAL MESSAGE ---
        final_msg = Text(
            "As trials increase, the empirical probability approaches 1.\n"
            "Ramsey’s theorem guarantees this order in any large enough graph.",
            font="Helvetica",
            color=YELLOW
        ).scale(0.5)
        final_msg.next_to(bar_chart, DOWN)
        self.play(FadeIn(final_msg))
        self.wait(3)

        self.play(FadeOut(bar_chart), FadeOut(formula), FadeOut(label_x), FadeOut(label_y), FadeOut(final_msg), FadeOut(title))
        self.wait(0.5)
