from manim import *


def pascal_row(n):
    line = [1]
    for k in range(n):
        line.append(line[k] * (n - k) / (k + 1))
    return line


def only_numeric_subobjects(mobj: MathTex) -> List[SingleStringMathTex]:
    return [m for m in mobj.submobjects if m.get_tex_string().strip().isnumeric()]


class Scene(MovingCameraScene):
    def construct(self):
        tex = MathTex("{{1}}", font_size=64).to_edge(UP)
        self.add(tex)
        all_mobjects = [tex]
        self.camera.frame.match_height(tex)
        self.camera.frame.rescale_to_fit(tex.length_over_dim(1)+1, 1)
        self.camera.frame.move_to(tex)
        self.play(Write(tex))
        for i in range(1, 20):
            newtex = MathTex(r" \enspace ".join([f'{{{{{j:g}}}}}' for j in pascal_row(i)]), font_size=64)\
                .next_to(tex, DOWN)
            all_mobjects.append(newtex)
            transforms = []
            onsnewtex = only_numeric_subobjects(newtex)
            for j, mobj in enumerate(only_numeric_subobjects(tex)):
                transforms += [Transform(mobj.copy(), onsnewtex[j].copy()),
                               Transform(mobj.copy(), onsnewtex[j + 1].copy())]
            print([m for m in tex.submobjects if m.get_tex_string().strip().isnumeric()])
            self.play(*transforms, self.camera.auto_zoom(all_mobjects, 1))
            tex = newtex
