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
        num_of_rows = 16
        self.next_section("Start")
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
        self.next_section("Highlight Odds")
        pascalsquares = []
        anims = []
        for rown, row in enumerate(squares):
            prow = pascal_row(rown)
            rowfills = []
            for i, square in enumerate(row):
                if prow[i] % 2 == 1:
                    sq: Square = square.copy().set_fill(BLUE, 1.0).set_color(DARK_BLUE)
                    pascalsquares.append(sq)
                    # sq.set_stroke(width=0)
                    rowfills.append(Create(sq))
            anims.append(LaggedStart(*rowfills))
        self.play(LaggedStart(*anims), run_time=4)
        self.wait(1)
        self.next_section("Build Serpinski")
        base = Polygon(squares[0].get_center(), squares[-1].submobjects[0].get_center(),
                       squares[-1].submobjects[-1].get_center()).set_fill(BLUE, 1.0).set_color(DARK_BLUE)
        tris = [base]
        self.play(Create(base), *[Uncreate(o) for o in pascalsquares + texts], run_time=3)
        for i in range(7):
            newtris = []
            anims = []
            for triangle in tris:
                triangle: Polygon
                center, outtris = split_triangle(triangle)
                newtris += outtris
                anims.append(Create(center.set_fill(BLACK)))
            self.play(*anims)
            tris = newtris


def split_triangle(base: Polygon) -> List[Polygon]:
    return [
        base.copy().scale(0.5).align_to(base, DOWN).flip(X_AXIS),
        [
            base.copy().scale(0.5).align_to(base, UP),
            base.copy().scale(0.5).align_to(base, DL),
            base.copy().scale(0.5).align_to(base, DR),
        ]
    ]


class Phi(MovingCameraScene):
    def construct(self):
        self.next_section("Start")
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
        self.next_section("Draw Arrows")
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
        self.next_section("Draw Fibbonaci Numbers")
        newsquares = VGroup(*[Square().next_to(squares[-1], DOWN, buff=LARGE_BUFF) for _ in range(num_of_rows)])
        newsquares.arrange_in_grid(rows=1, buff=LARGE_BUFF)
        fit_mobject_within_another(newsquares, self.camera.frame, LARGE_BUFF)
        newnums = []
        for i, square in enumerate(newsquares.submobjects):
            num = Text(str(fib(i)))
            newnums.append(num)
            fit_mobject_within_another(num, square)
        self.play(*[Transform(nums[i], newnums[i]) for i in range(num_of_rows)],
                  *[FadeOut(obj) for obj in arrs + texts],
                  run_time=2)
        self.wait(1)
        self.next_section("Recreate Fibbonaci Numbers")
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
        self.next_section("Draw Fibbonaci Number Ratios")
        frac = SingleStringMathTex(r"\frac{1}{1}", font_size=300)
        numerator = VGroup(frac.submobjects[0])
        line = frac.submobjects[1]
        denominator = VGroup(frac.submobjects[2])
        fracbound = Square(VGroup(*nums[0:2]).width).next_to(nums[2], LEFT, LARGE_BUFF)
        fit_mobject_within_another(frac, fracbound)

        newsquares += Square().next_to(newsquares[-1], RIGHT, buff=LARGE_BUFF)
        numparade = []
        for i in range(2, num_of_rows + 1):
            num = Text(str(fib(i)))
            numparade.append(num)
            fit_mobject_within_another(num, newsquares[i])
        self.remove(*nums_to_fade_out)
        self.add(*numparade)
        self.play(
            # *[FadeOut(o) for o in nums_to_fade_out],
            Transform(nums[0], frac.submobjects[0], replace_mobject_with_target_in_scene=True),
            Create(frac.submobjects[1]),
            Transform(nums[1], frac.submobjects[2], replace_mobject_with_target_in_scene=True),
            run_time=2
        )
        for fibn in range(2, 10):
            newnumerator = str(fib(fibn + 1))
            newdenominator = str(fib(fibn))
            newfrac = SingleStringMathTex(r"\frac{" + newnumerator + "}{" + newdenominator + "}",
                                          font_size=300)
            fit_mobject_within_another(newfrac, fracbound)
            newnumerator = VGroup(*newfrac.submobjects[:len(newnumerator)])
            newline = newfrac.submobjects[len(newnumerator)]
            newdenominator = VGroup(*newfrac.submobjects[-len(newdenominator):])
            self.play(
                Transform(numparade[0], newnumerator, replace_mobject_with_target_in_scene=True),
                Transform(line, newline, replace_mobject_with_target_in_scene=True),
                Transform(numerator, newdenominator, replace_mobject_with_target_in_scene=True),
                Transform(denominator, newdenominator, replace_mobject_with_target_in_scene=True),
                *[numparade[i].animate.move_to(numparade[i - 1]) for i in
                  range(1, len(numparade))],
                run_time=0.5
            )
            num = Text(str(fib(fibn + num_of_rows)))
            fit_mobject_within_another(num, newsquares[-1])
            del numparade[0]
            numparade.append(num)
            frac = newfrac
            denominator = newdenominator
            line = newline
            numerator = newnumerator
        self.next_section("1.618")
        phi = MathTex(r"1.618\cdots")
        fit_mobject_within_another(phi, self.camera.frame, buff=5)
        self.play(
            Transform(frac, phi, replace_mobject_with_target_in_scene=True),
            *[FadeOut(o) for o in numparade],
            run_time=1.5
        )
        self.wait(1)
        self.next_section("Phi")
        self.play(Transform(phi, fit_mobject_within_another(MathTex(r"\varphi"), self.camera.frame, buff=5)))
        self.next_section("Representations of Phi")
        self.wait(1)
        phireps = [
            r"\frac{1+\sqrt{5}}{2}",
            r"1 + \cfrac{1}{1 + \cfrac{1}{1 + \cfrac{1}{1 + \cfrac{1}{1 + \ddots}}}}",
            r"\sqrt{1 + \sqrt{1 + \sqrt{1 + \cdots}}}",
            r"2\sin 54^\circ"
        ]
        for rep in phireps:
            self.play(Transform(phi, fit_mobject_within_another(MathTex(rep), self.camera.frame, buff=5)))
            self.wait(1)


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


def fit_mobject_within_another(mobj: Mobject, fit: Mobject, buff: float = 0) -> Mobject:
    mobj.move_to(fit)
    mobj.scale_to_fit_width(fit.width - (buff * 2))
    if mobj.height > fit.height:
        mobj.scale_to_fit_height(fit.height - (buff * 2))
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
