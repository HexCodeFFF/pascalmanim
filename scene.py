from manim import *


class Scene(Scene):
    def construct(self):
        tex = Text(r"\LaTeX", font_size=144)
        self.add(tex)
        self.wait(1)
