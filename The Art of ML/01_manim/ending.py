from manim import *
import os
from get_tech_logos import get_tech_logos

class Outro(Scene):
    def construct(self):
        self.camera.background_color = "#020b1a"

        # -------------------------------------------------------------
        # Scene 7 - Topic, Agenda & Moving Underline
        # -------------------------------------------------------------
        topic_title = Text("How neural network learns linear function", font_size=40, weight=BOLD, color="#fffcd6")
        topic_title.to_edge(UP, buff=0.8)

        divider = Line(start=ORIGIN, end=RIGHT * 11.2, color="#78716c", stroke_width=2)
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
        logos_box.shift(UP * 0.5)

        highlight = Line(LEFT, RIGHT, color="#78716c", stroke_width=3)
        highlight.match_width(agenda_group[0])
        highlight.next_to(agenda_group[0], DOWN, buff=0.1, aligned_edge=LEFT)

        self.play(
            Create(topic_title),
            Create(divider),
            FadeIn(agenda_group),
            FadeIn(logos_box),
            Create(highlight),
            run_time=1.0
        )
        self.wait(0.5)

        for item in agenda_group[1:]:
            self.play(
                highlight.animate.match_width(item).next_to(item, DOWN, buff=0.1, aligned_edge=LEFT),
                run_time=0.6
            )
            self.wait(0.4)

        self.wait(1.0)

        self.play(
            FadeOut(VGroup(topic_title, divider, agenda_group, logos_box, highlight)),
            run_time=0.8
        )
        self.wait(0.3)

        thanks_text = Text("Thank you for your attention", font_size=52, weight=BOLD, color="#fffcd6")

        thanks_underline = Line(LEFT, RIGHT, color="#78716c", stroke_width=3)
        thanks_underline.match_width(thanks_text)
        thanks_underline.next_to(thanks_text, DOWN, buff=0.25)

        outro_group = VGroup(thanks_text, thanks_underline).move_to(ORIGIN)

        self.play(Write(thanks_text), run_time=1.8)
        self.play(Create(thanks_underline), run_time=0.6)
        self.wait(1.5)

        # self.play(FadeOut(Group(*self.mobjects)), run_time=1.2)
        
        # Opcjonalne przestawienie tła na czyste #000000 i krótka pauza w czerni
        fade_to_black = Rectangle(
                width=config.frame_width + 1,
                height=config.frame_height + 1,
                color=BLACK,
                fill_color=BLACK,
                fill_opacity=1
            )

            # Płynny FadeIn czarnego ekranu (możesz dostosować run_time, np. 1.5 lub 2.0 sekundy)
        self.play(FadeIn(fade_to_black), run_time=1.5)
        self.wait(0.5)