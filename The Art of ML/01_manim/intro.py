from manim import *
import os
from get_tech_logos import get_tech_logos

class Intro(Scene):
    def construct(self):
        self.camera.background_color = "#020b1a"

        # Scene 1 - Channel Name
        channel_name = Text("The Art of Machine Learning", font_size=52, weight=BOLD, color="#fffcd6")

        underline = Line(LEFT, RIGHT, color="#78716c", stroke_width=3)
        underline.match_width(channel_name)
        underline.next_to(channel_name, DOWN, buff=0.25)

        intro_group = VGroup(channel_name, underline).move_to(ORIGIN)

        self.play(Write(channel_name), run_time=1.8)
        self.play(Create(underline), run_time=0.6)
        self.wait(2.5)

        self.play(FadeOut(intro_group, shift=UP * 0.4), run_time=0.8)
        self.wait(0.3)


        # Scene 2 - Topic and Agenda
        topic_title = Text("How neural network learns linear function", font_size=40, weight=BOLD, color="#fffcd6")
        topic_title.to_edge(UP, buff=0.8)

        divider = Line(start=ORIGIN, end=RIGHT*11.2, color="#78716c", stroke_width=2)
        divider.next_to(topic_title, DOWN, buff=0.25, aligned_edge=LEFT)

        agenda_items = [
            "1. Short introduction to linear functions",
            "2. Creating, splitting and analysing the data",
            "3. Building and training the model",
            "4. Analysing model output",
            "5. Saving the model"
        ]

        agenda_group = VGroup()
        for item in agenda_items:
            text = Text(item, font_size=26, color="#d3e7fa")
            agenda_group.add(text)

        agenda_group.arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        agenda_group.next_to(divider, DOWN, buff=0.6, aligned_edge=LEFT)

        logos = get_tech_logos()

        logos_box = VGroup(
            Text("Using: ", font_size=20, color="#94a3b8"),
            logos
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)

        logos_box.to_corner(DR, buff=1.0)
        logos_box.shift(UP*0.5)

        self.play(
            Write(topic_title),
            Create(divider),
            run_time=1.0
        )

        for item in agenda_group:
            self.play(FadeIn(item, shift=RIGHT*0.3), run_time=0.35)

        self.play(FadeIn(logos_box, shift=UP*0.3), run_time=0.8)

        self.wait(3)

        self.play(FadeOut(topic_title, agenda_group, logos_box, divider))


        # Scene 3 - Linear Function

        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 5, 1],
            x_length=8,
            y_length=6,
            axis_config={"include_numbers": True},
            ).to_edge(LEFT, buff=0.5)

        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")

        a_tracker = ValueTracker(1)
        b_tracker = ValueTracker(0)

        graph = always_redraw(
            lambda: axes.plot(
                lambda x: a_tracker.get_value() * x + b_tracker.get_value(),
                x_range=[-3, 3],
                color=BLUE,
            )
        )

        formula = always_redraw(
            lambda: MathTex(f"y = {a_tracker.get_value():.1f}x + {b_tracker.get_value():.1f}"
        ).scale(1.2).to_edge(RIGHT, buff=1.0).shift(UP*2))

        info_text = Text("a - slop\nb - bias", font_size=24).next_to(formula, DOWN, buff=1.0)

        self.play(Create(axes), Write(axes_labels))
        self.play(Write(formula), FadeIn(info_text))
        self.play(Create(graph))
        self.wait(1)


        self.play(a_tracker.animate.set_value(2.5), run_time=2)
        self.wait(0.5)
        self.play(a_tracker.animate.set_value(-1.5), run_time=2)
        self.wait(0.5)
        self.play(a_tracker.animate.set_value(1.0), run_time=1)  
        self.wait(0.5)


        self.play(b_tracker.animate.set_value(3.0), run_time=2)
        self.wait(0.5)
        self.play(b_tracker.animate.set_value(-2.0), run_time=2)
        self.wait(0.5)
        self.play(b_tracker.animate.set_value(0.0), run_time=1)  
        self.wait(1)


        self.play(
            a_tracker.animate.set_value(0.5),
            b_tracker.animate.set_value(2.0),
            run_time=2
        )
        self.wait(2)
    


