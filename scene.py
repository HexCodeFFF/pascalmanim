from manim import *


def pascal_row(n):
    line = [1]
    for k in range(n):
        line.append(round(line[k] * (n - k) / (k + 1)))
    return line


def only_numeric_subobjects(mobj: MathTex) -> List[SingleStringMathTex]:
    return [m for m in mobj.submobjects if m.get_tex_string().strip().isnumeric()]


def split_text_by_word(text: Text) -> List[VGroup]:
    i = 0
    out = []
    vg = VGroup()
    for char in text.original_text:
        if char == " ":
            if len(vg) > 0:
                out.append(vg)
                vg = VGroup()
        else:
            vg += text[i]
            i += 1
    if len(vg) > 0:
        out.append(vg)
    return out


class Scene(MovingCameraScene):
    def construct(self):
        tex = Text("1", font_size=16).to_edge(UP)
        self.add(tex)
        all_mobjects = [tex]
        self.camera.frame.match_height(tex)
        self.camera.frame.rescale_to_fit(tex.length_over_dim(1) + 1, 1)
        self.camera.frame.move_to(tex)
        self.play(Write(tex), run_time=2)
        for i in range(1, 20):
            newtex = Text(r"   ".join([f'{j:g}' for j in pascal_row(i)]),
                          font_size=16).next_to(tex, DOWN)
            all_mobjects.append(newtex)
            transforms = []
            onsnewtex = split_text_by_word(newtex)
            for j, mobj in enumerate(split_text_by_word(tex)):
                transforms += [Transform(mobj.copy(), onsnewtex[j]),
                               Transform(mobj.copy(), onsnewtex[j + 1])]
            self.play(*transforms, self.camera.auto_zoom(all_mobjects, 1), run_time=2)
            # self.add(newtex)
            # self.play(self.camera.auto_zoom(all_mobjects, 1), run_time=2)
            tex = newtex
