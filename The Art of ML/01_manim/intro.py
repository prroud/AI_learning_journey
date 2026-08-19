from manim import *
import os

class Intro(Scene):
    def construct(self):
        self.camera.background_color = "#020b1a"

        # Scene 1 - Channel Name

        channel_name = Text("The Art of Machine Learning", font_size=52, weight=BOLD)

        underline = Line(LEFT, RIGHT, color="#334155", stroke_width=3)
        underline.match_width(channel_name)
        underline.next_to(channel_name, DOWN, buff=0.25)

        intro_group = VGroup(channel_name, underline).move_to(ORIGIN)

        self.play(Write(channel_name), run_time=1.8)
        self.play(Create(underline), run_time=0.6)
        self.wait(2.5)

        self.play(FadeOut(intro_group, shift=UP * 0.4), run_time=0.8)
        self.wait(0.3)




        # Scene 2 - Topic and Agenda

        topic_title = Text("How neural network learns linear function", font_size=40, weight=BOLD)
        topic_title.to_edge(UP, buff=0.8)

        divider = Line(start=ORIGIN, end=RIGHT*11.2, color="#334155", stroke_width=2)
        divider.next_to(topic_title, DOWN, buff=0.25, aligned_edge=LEFT)

        agenda_items = [
            "1. Short introduction to linear functions",
            "2. Creating, spliting and analysing the data",
            "3. Building and training the model",
            "4. Analysing model output",
            "5. Saving the model"
        ]

        agenda_group = VGroup()
        for item in agenda_items:
            text = Text(item, font_size=26, color=WHITE)
            agenda_group.add(text)

        agenda_group.arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        agenda_group.next_to(divider, DOWN, buff=0.6, aligned_edge=LEFT)

        logos = self.get_tech_logos()

        logos_box = VGroup(
            Text("Using: ", font_size=20, color=WHITE),
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

    def get_tech_logos(self):
            python_path = "python_logo.svg"
            pytorch_path = "pytorch_logo.svg"
            
            py_img = SVGMobject(python_path)
            pt_img = SVGMobject(pytorch_path)
            
            py_img.height = 1.0
            pt_img.height = 1.0

            if len(py_img) >= 2:
                py_img[0].set_color("#306998")  
                py_img[1].set_color("#FFD43B")  
            else:
                py_img.set_color_by_gradient("#306998", "#FFD43B")

            return VGroup(py_img, pt_img).arrange(RIGHT, buff=0.8)


