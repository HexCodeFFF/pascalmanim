import math

from manim import *


def pascal_row(rowIndex):
    # https://medium.com/@duhroach/fast-fun-with-pascals-triangle-6030e15dced0
    row = [0] * (rowIndex + 1)
    row[0] = row[rowIndex] = 1
    for i in range(0, rowIndex >> 1):
        x = row[i] * (rowIndex - i) / (i + 1)

        row[i + 1] = row[rowIndex - 1 - i] = x
    return row


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


def animate_math(scene: Scene, transforms: List[typing.Tuple[str, str]], **mathtexparams) -> MathTex:
    eq = MathTex(transforms[0][0], **mathtexparams)
    for old, new in transforms:
        scene.remove(eq)
        eq = MathTex(old, **mathtexparams)
        scene.add(eq)
        neweq = MathTex(new, **mathtexparams)
        scene.play(TransformMatchingTex(eq, neweq))
        eq = neweq
    return eq


class Scene(MovingCameraScene):
    def construct(self):
        # self.next_section("(x+1)^2")
        # transforms = [
        #     (r"{{ ( x + 1 ) }} ^2", r"{{ ( x + 1 ) }} {{ ( x + 1 ) }}"),
        #     (r"( {{ x }} + {{ 1 }} ) ( {{ x }} + {{ 1 }} )", r"{{ x }} ^2 + {{ x }} + {{ x }} + {{ 1 }}",),
        #     (r"{{ x^2 }} + {{ x }} + {{ x }} + {{ 1 }}", r"{{ x^2 }} + 2 {{ x }} + {{ 1 }}")
        # ]
        # eq = animate_math(self, transforms)
        # self.wait()
        # self.next_section("(x+1)^3")
        # neweq = MathTex(r"( x + 1 )^3")
        # self.play(Transform(eq, neweq))
        # self.remove(eq)
        # transforms = [
        #     (r"{{ ( x + 1 ) }} ^3", r"{{ ( x + 1 ) }} {{ ( x + 1 ) }} {{ ( x + 1 ) }}"),
        #     (r"( {{ x }} + {{ 1 }} ) ( {{ x }} + {{ 1 }} ) ( {{ x }} + {{ 1 }} )",
        #      "{{ x }} ^3 + 3 {{ x }} ^2 + 3 {{ x }} + {{ 1 }}")
        # ]
        # eq = animate_math(self, transforms)
        # self.wait(1)
        # # self.remove(eq)
        # # eqs = MathTex(r"x^3+3x^2+3x+1")
        # # self.add(eqs)
        # binomials = [
        #     "{{ 1 }}",
        #     "{{ x + 1 }}",
        #     "{{ x^2 + 2 x + 1 }}",
        #     "{{ x^3 + 3 x^2 + 3 x + 1 }}",
        #     "{{ x^4 + 4 x^3 + 6 x^2 + 4 x + 1 }}",
        #     "{{ x^5 + 5 x^4 + 10 x^3 + 10 x^2 + 5 x + 1 }}",
        #     "{{ x^6 + 6 x^5 + 15 x^4 + 20 x^3 + 15 x^2 + 6 x + 1 }}",
        #     "{{ x^7 + 7 x^6 + 21 x^5 + 35 x^4 + 35 x^3 + 21 x^2 + 7 x + 1 }}"
        # ]
        # for rep in binomials[3:]:
        #     tobecome = fit_mobject_within_another(MathTex(rep), self.camera.frame, buff=3)
        #     self.play(Transform(eq, tobecome))
        #     self.wait(1)
        # finaleq = fit_mobject_within_another(MathTex("{{ x^7 + 7 x^6 + 21 x^5 + 35 x^4 + 35 x^3 + 21 x^2 + 7 x + 1 }}"),
        #                                      self.camera.frame, buff=3)
        # self.remove(eq)
        # self.add(finaleq)
        # self.wait(1)
        # self.next_section("the pattern")
        # thetrongle = fit_mobject_within_another(
        #     MathTex(r" \\ ".join(binomials), tex_environment="gather*"), self.camera.frame, buff=3)
        # self.play(TransformMatchingTex(finaleq, thetrongle))
        # self.wait(1)
        # self.remove(finaleq)
        # self.add(thetrongle)
        # # all of the possible coeffs till row 8 with spaces so i dont select exponents
        # coeffs = list({f" {math.comb(n, k)} " for n in range(8) for k in range(math.ceil((n + 1) / 2))})
        # # add 1 coeffs to x^n terms
        # newbinomials = []
        # for b in binomials:
        #     if b != "{{ 1 }}":
        #         b = "1 " + b
        #     newbinomials.append(b)
        # thetrongle2 = fit_mobject_within_another(
        #     MathTex(r" \\ ".join(newbinomials), tex_environment="gather*"),
        #     self.camera.frame,
        #     buff=3)
        # self.play(TransformMatchingTex(thetrongle, thetrongle2))
        # # recolor
        # self.remove(thetrongle)
        # self.remove(thetrongle2)
        # thetrongle2 = fit_mobject_within_another(
        #     MathTex(r" \\ ".join(newbinomials), tex_environment="gather*", substrings_to_isolate=coeffs),
        #     self.camera.frame,
        #     buff=3)
        # self.add(thetrongle2)
        # self.play(thetrongle2.animate.set_color_by_tex_to_color_map({coeff: YELLOW for coeff in coeffs} |
        #                                                             {tex.get_tex_string(): GRAY for tex in
        #                                                              thetrongle2.submobjects if
        #                                                              tex.get_tex_string() not in coeffs}))
        # self.wait(1)
        # self.next_section("formula")
        # self.remove(thetrongle2)
        # self.play(FadeOut(thetrongle2))
        bformulatext = r"(1+x)^{n} = 1 + n x + \frac{n(n-1)}{2!}x^2 " \
                       r"+ \frac{n(n-1)(n-2)}{3!}x^3 + \frac{n(n-1)(n-2)(n-3)}{4!}x^4 " \
                       r"+ \cdots "
        # binomialformula = fit_mobject_within_another(MathTex(bformulatext), self.camera.frame, LARGE_BUFF)
        # fit_mobject_within_another(binomialformula, self.camera.frame, LARGE_BUFF)
        # for so in binomialformula.submobjects:
        #     self.next_section()
        #     self.play(Write(so))
        # self.next_section("compact formula")
        # self.play(Transform(binomialformula, MathTex(r"(1+x)^n = \sum_{k=0}^n {n \choose k}x^k")))
        # self.wait(1)
        # self.next_section()
        # self.play(Transform(binomialformula,
        #                     fit_mobject_within_another(MathTex(bformulatext), self.camera.frame, LARGE_BUFF)))
        # self.wait(1)
        # self.next_section()
        # self.play(self.camera.auto_zoom(binomialformula.submobjects[0], 1))
        # self.wait()
        # self.remove(thetrongle2)
        thetrongle2 = fit_mobject_within_another(MathTex(bformulatext), self.camera.frame, 3)
        minusonetriangle, transforms = transform_tex_symbols(thetrongle2, "n", "-1")
        self.add(thetrongle2)
        self.wait()
        self.play(*transforms)
        self.wait()


def transform_tex_symbols(mobj: MathTex, symbol_to_replace: str, target_symbol: str, reverse: bool = False) \
        -> typing.Tuple[MathTex, List[Transform]]:
    # init vars
    symbols_to_replace: List[TexSymbol] = [SingleStringMathTex(symbol_to_replace).submobjects[0].path_string,
                                           SingleStringMathTex(f"^{symbol_to_replace}").submobjects[0].path_string]
    target_tex_symbols = SingleStringMathTex(target_symbol).submobjects
    target = MathTex(mobj.tex_string.replace(symbol_to_replace, target_symbol)) \
        .move_to(mobj).match_height(mobj)

    transforms = []
    for i, tx in enumerate(mobj.submobjects):
        target_symbol_index = 0
        for symbol in tx.submobjects:
            if hasattr(symbol, "path_string") and symbol.path_string in symbols_to_replace:
                target_group = VGroup()
                for j in range(len(target_tex_symbols)):
                    target_group += target.submobjects[i].submobjects[target_symbol_index]
                    target_symbol_index += 1
                if reverse:
                    transforms.append(Transform(target_group, symbol))
                else:
                    transforms.append(Transform(symbol, target_group))
            else:
                if reverse:
                    transforms.append(Transform( target.submobjects[i].submobjects[target_symbol_index], symbol))
                else:
                    transforms.append(Transform(symbol, target.submobjects[i].submobjects[target_symbol_index]))
                target_symbol_index += 1
    return target, transforms


class Serpinski(MovingCameraScene):
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
        self.play(*[o.animate.scale(0) for o in pascalsquares], run_time=0.5)
        self.play(*[AnimationGroup(*[so.animate.scale(0) for so in text.submobjects]) for text in texts], run_time=0.5)
        self.play(GrowFromCenter(base), run_time=0.5)
        [self.remove(text) for text in texts]
        [self.remove(o) for o in pascalsquares]
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
