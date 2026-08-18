from manim import *

class Pith(Scene):
    def construct(self):
        name = Tex("The Art of Machine Learning")


        self.play(Write(name))
        self.wait()