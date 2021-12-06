import math

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


def fib(n):
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a


class Scene(MovingCameraScene):
    def construct(self):
        num_of_rows = 10
        texts = []
        tex = Text("1", font_size=16).to_edge(UP)
        texts.append(tex)
        self.add(tex)
        square = Square().to_edge(UP)
        fit_mobject_within_another(tex, square)
        squares = [square]
        self.add(tex)
        for i in range(1, num_of_rows):
            newtex = Text(r"   ".join([f'{j:g}' for j in pascal_row(i)]),
                          font_size=16).next_to(tex, DOWN)
            newsquares = VGroup(*[Square().next_to(squares[-1], DOWN, buff=LARGE_BUFF) for _ in range(i + 1)])
            newsquares.arrange_in_grid(cols=i + 1, rows=1, buff=LARGE_BUFF)
            squares.append(newsquares)
            texts.append(newtex)
            onsnewtex = split_text_by_word(newtex)
            for i, square in enumerate(newsquares.submobjects):
                fit_mobject_within_another(onsnewtex[i], square)
            self.add(newtex)
        everything = VGroup(*squares)
        self.camera.frame.match_height(everything)
        self.camera.frame.rescale_to_fit(everything.length_over_dim(1) + 2, 1)
        self.camera.frame.move_to(everything)
        self.wait(1)
        arrs = []
        nums = []
        for i, row in enumerate(squares):
            start = row[0].get_center()
            # constant slope calculated through pain
            end = start + (np.array([2.25, 1.5, 0]) * (i + 1))
            arr = Arrow(start=start, end=end)
            arrs.append(arr)

            num = fit_mobject_within_another(Text(str(fib(i))), Square(side_length=1).next_to(arr, UR))
            nums.append(num)

        self.play(LaggedStart(*[Create(arr) for arr in arrs]), run_time=3)
        self.play(LaggedStart(self.camera.auto_zoom(nums, 4),
                              *[Write(num) for num in nums]), run_time=2)
        newsquares = VGroup(*[Square().next_to(squares[-1], DOWN, buff=LARGE_BUFF) for _ in range(num_of_rows)])
        newsquares.arrange_in_grid(rows=1, buff=LARGE_BUFF)
        fit_mobject_within_another(newsquares, self.camera.frame)
        newnums = []
        for i, square in enumerate(newsquares.submobjects):
            num = Text(str(fib(i)))
            newnums.append(num)
            fit_mobject_within_another(num, square)
        self.play(*[Transform(nums[i], newnums[i]) for i in range(num_of_rows)],
                  *[FadeOut(obj) for obj in arrs + texts],
                  run_time=2)
        self.wait(1)
        numscopy = [n.copy() for n in nums]
        self.play(LaggedStart(*[Unwrite(i) for i in nums[2:][::-1]]), run_time=1.5)
        nums_to_fade_out = []
        for i, numtowrite in enumerate(nums[2:]):
            i += 2  # first 2 numbers are already drawn
            nmin2 = numscopy[i - 2].copy()
            nmin1 = numscopy[i - 1].copy()
            nums_to_fade_out += [nmin1, nmin2]
            self.play(
                # MoveAlongPath(nmin2, ArcBetweenPoints(start=nmin2.get_start(), end=numtowrite.get_start())),
                Transform(nmin2, numscopy[i], path_arc=math.pi),
                Transform(nmin1, numscopy[i], path_arc=-math.pi),
                # MoveAlongPath(nmin1, ArcBetweenPoints(start=nmin1.get_start(), end=numtowrite.get_start())),
            )
        self.wait(1)
        frac = SingleStringMathTex(r"\frac{1}{1}", font_size=300)
        numerator = VGroup(frac.submobjects[0])
        line = frac.submobjects[1]
        denominator = VGroup(frac.submobjects[2])
        fracpos = np.mean(nums[0].get_center(), nums[1].get_center())
        frac.move_to(fracpos)
        self.play(
            # *[FadeOut(o) for o in nums_to_fade_out],
            Transform(nums[0], frac.submobjects[0], replace_mobject_with_target_in_scene=True),
            Create(frac.submobjects[1]),
            Transform(nums[1], frac.submobjects[2], replace_mobject_with_target_in_scene=True),
            run_time=2
        )
        for fibn in range(2, 20):
            newnumerator = str(fib(fibn + 1))
            newdenominator = str(fib(fibn))
            newfrac = SingleStringMathTex(r"\frac{" + newnumerator + "}{" + newdenominator + "}",
                                          font_size=300).move_to(fracpos)
            newnumerator = VGroup(*newfrac.submobjects[:len(newnumerator)])
            newline = newfrac.submobjects[len(newnumerator)]
            newdenominator = VGroup(*newfrac.submobjects[-len(newdenominator):])
            numcopy = numerator.copy()
            self.play(
                Transform(numerator, newnumerator, replace_mobject_with_target_in_scene=True),
                Transform(line, newline, replace_mobject_with_target_in_scene=True),
                Transform(numcopy, newdenominator, replace_mobject_with_target_in_scene=True),
                Transform(denominator, newdenominator, replace_mobject_with_target_in_scene=True)
            )
            frac = newfrac
            denominator = newdenominator
            line = newline
            numerator = newnumerator
        phi = MathTex(r"\frac{1+\sqrt{5}}{2}", font_size=300).move_to(self.camera.frame.get_center())
        self.play(Transform(frac, phi, replace_mobject_with_target_in_scene=True))
        self.wait(1)
        self.play(Transform(phi, MathTex(r"\varphi", font_size=500).move_to(self.camera.frame.get_center())))
        self.wait(1)
        self.play(Transform(phi, MathTex(r"1 + \cfrac{1}{1 + \cfrac{1}{1 + \cfrac{1}{1 + \cfrac{1}{1 + \ddots}}}}",
                                         font_size=100).move_to(self.camera.frame.get_center())))
        self.wait(1)
        self.play(Transform(phi, MathTex(r"\sqrt{1 + \sqrt{1 + \sqrt{1 + \cdots}}}",
                                         font_size=200).move_to(self.camera.frame.get_center())))
        self.wait(1)
        self.play(Transform(phi, MathTex(r"2\sin 54^\circ",
                                         font_size=300).move_to(self.camera.frame.get_center())))
        self.wait(1)
        print(frac)


def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


class BuildTriangle(MovingCameraScene):
    def construct(self):
        tex = Text("1", font_size=16).to_edge(UP)
        self.add(tex)
        square = Square().to_edge(UP)
        fit_mobject_within_another(tex, square)
        squares = [square]
        self.camera.frame.match_height(square)
        self.camera.frame.rescale_to_fit(square.length_over_dim(1) + 1, 1)
        self.camera.frame.move_to(square)
        self.play(Write(tex), run_time=2)
        for i in range(1, 20):
            newtex = Text(r"   ".join([f'{j:g}' for j in pascal_row(i)]),
                          font_size=16).next_to(tex, DOWN)
            newsquares = VGroup(*[Square().next_to(squares[-1], DOWN, buff=LARGE_BUFF) for _ in range(i + 1)])
            newsquares.arrange_in_grid(cols=i + 1, rows=1, buff=LARGE_BUFF)
            squares.append(newtex)
            transforms = []
            onsnewtex = split_text_by_word(newtex)
            for i, square in enumerate(newsquares.submobjects):
                fit_mobject_within_another(onsnewtex[i], square)
            for j, mobj in enumerate(split_text_by_word(tex)):
                transforms += [Transform(mobj.copy(), onsnewtex[j]),
                               Transform(mobj.copy(), onsnewtex[j + 1])]
            self.play(*transforms, self.camera.auto_zoom(squares, 1), run_time=2)
            # self.add(newtex)
            # self.play(self.camera.auto_zoom(all_mobjects, 1), run_time=2)
            tex = newtex


def fit_mobject_within_another(mobj: Mobject, fit: Mobject) -> Mobject:
    mobj.move_to(fit)
    mobj.scale_to_fit_width(fit.width)
    if mobj.height > fit.height:
        mobj.scale_to_fit_height(fit.width)
    return mobj


class Squares(MovingCameraScene):
    def construct(self):
        square = Square().to_edge(UP)
        squares = [square]
        self.add(square)
        for i in range(1, 10):
            newsquares = VGroup(*[Square().next_to(squares[-1], DOWN, buff=LARGE_BUFF) for _ in range(i + 1)])
            newsquares.arrange_in_grid(cols=i + 1, rows=1, buff=LARGE_BUFF)
            self.add(newsquares)
            prow = pascal_row(i)
            for i, square in enumerate(newsquares.submobjects):
                self.add(fit_mobject_within_another(Text(str(prow[i]), font_size=16), square))
            squares.append(newsquares)
            self.play(self.camera.auto_zoom(squares, 1), run_time=0.5)
