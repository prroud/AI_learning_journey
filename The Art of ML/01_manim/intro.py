from manim import *
import os

class Intro(Scene):
    def construct(self):
        self.camera.background_color = "#020e21"

        # Scene 1 - channel name

        channel_name = Text("The Art of Machine Learning", font_size=52, weight=BOLD)
        channel_name[:10].set_color("#94A3B8")
        channel_name[:10].set_color("#38BDF8")

        underline = Line(LEFT, RIGHT, color="#38BDF8", stroke_width=3)
        underline.match_width(channel_name)
        underline.next_to(channel_name, DOWN, buff=0.25)

        intro_group = VGroup(channel_name, underline).move_to(ORIGIN)

        self.play(Write(channel_name), run_time=1.8)
        self.play(Create(underline), run_time=0.6)
        self.wait(2.5)

        self.play(FadeOut(intro_group, shift=UP * 0.4), run_time=0.8)
        self.wait(0.3)


