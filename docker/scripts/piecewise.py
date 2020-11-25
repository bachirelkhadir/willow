#!/usr/bin/env python3

# PROJECT_DIR = '/home/bachir/Dropbox/Conferences/IBM_Oct_22/Slides/manim'
DEBUG = False
import sys, os
# sys.path.append(os.path.join(PROJECT_DIR, '/PATH/'))
# sys.path.append(os.path.join(PROJECT_DIR, 'common_imports'))

sys.DEBUG = DEBUG

NUM_BLACK_SCREENS = 0
from scipy.integrate import odeint
from manimlib.imports import *

from scipy import linalg
import numpy as np
# from color_map import *
# from helper_functions import *
from os import walk
from tqdm import tqdm


def helper_grid(scene, add_numbers=False):
    for x in range(-5, 5):
        for y in range(-5, 5):
            c = WHITE
            if x*y < 0:
                c = RED

            dot = Dot(point=(x, y, 0)).scale(.5).set_fill(WHITE, opacity=0.2)
            if add_numbers:
                annot = TexMobject(f"({x},{y})").scale(.4)
                annot.next_to(dot, DOWN, SMALL_BUFF)
                scene.add(annot)
            scene.add(dot)
    scene.add(Line((-5,0,0,), (5,0,0,)).fade(.5))
    scene.add(Line((0,-5,0,), (0,5,0,)).fade(.5))


def make_def(label, name=r"\textbf{Def}"):
    return make_thm(label, name=r"\textbf{Def.}")


def make_thm(label, name=r"\textbf{Thm}", line_break=True):
    if name is not None:
        label_name = TextMobject(name).set_color("#f1bf27")
    else:
        # placeholder
        label_name = Dot().fade(1)

    if line_break:
        label_name.next_to(label, UP, MED_LARGE_BUFF)\
              .align_to(label, LEFT)\
              .shift(LEFT/3)
    else:
        label_name.next_to(label, LEFT, MED_LARGE_BUFF)

    rect = SurroundingRectangle(VGroup(label_name, label))
    rect.scale((1.1, 1.2, 1.))
    rect.set_fill(BLACK, opacity=.5)
    rect.set_stroke(BLACK)
    return VGroup(rect, label_name, label)


def align_group_text(group, dir=LEFT):
    for g in group[1:]:
        g.align_to(group[0], dir)
    return group


def stack_group_text(group, dir=DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER):
    for g_prev, g in zip(group, group[1:]):
        g.next_to(g_prev, dir, buff=buff)
    return group


def add_black_screen(scene, timeout=1):
    global NUM_BLACK_SCREENS
    NUM_BLACK_SCREENS += 1
    print("Blackish Screen: ", NUM_BLACK_SCREENS)
    color = BLACK
    if DEBUG:
        color = '#1f303f'
        scene.wait(.1)
        return

    rect = Rectangle(fill_color=color, strole_color=color, fill_opacity=1).scale(100)
    # make unaffected by camera

    scene.wait(timeout)
    try:
        scene.add_fixed_in_frame_mobjects(rect)
    except AttributeError:
        # we are not in 3D
        scene.add(rect)
    scene.wait(timeout)
    scene.remove(rect)

class Piecewise(MovingCameraScene):
    CONFIG = {
        'pos_ui': (1.9*LEFT+2.8*UP,
                   1.5*UP,
                   .8*LEFT+.8*DOWN,
                   1.15 * RIGHT + 3.3 * DOWN)
    }

    def construct(self):
        background = self.background = ImageMobject("scripts/piece_wise_path.png")
        background.set_height(FRAME_HEIGHT)
        self.add(background)
        add_black_screen(self)


        self.plot_ui()
        add_black_screen(self)
        self.add_tv_ineq()
        add_black_screen(self)
        self.add_moment_explicaton()
        add_black_screen(self)

        self.add_tv_sdp()
        add_black_screen(self)

    def plot_ui(self):
        pos_vi = [uii - ui for uii,ui in zip(self.pos_ui[1:], self.pos_ui)]
        dots = []
        for ui in self.pos_ui:
            dot = Dot()
            dot.move_to(ui)
            dots.append(dot)

        vec = Arrow(dots[2], dots[1], buff=0)
        label_ui = TexMobject(r"u_i")
        label_vi = TexMobject(r"v_i")
        label_ui.next_to(dots[2], LEFT)
        label_vi.next_to(vec, RIGHT, SMALL_BUFF)

        # YELLOW colors:
        for ob in (vec, label_vi):
            ob.set_color(ORANGE)

        for ob in [*dots, label_ui]:
            ob.set_color(BLUE_B)

        # Add to scene
        for dot in dots:
            self.add(dot)


        self.add(label_ui)
        add_black_screen(self)
        self.add(label_vi)
        self.add(vec)


    def add_tv_ineq(self):
        label_ineq = TexMobject(r"g", "(t, ", "u_i ", "+ ", "t ", "v_i", r") \ge 0 \\ \forall t \in  \left[i \frac{T}s, (i+1) \frac{T}s\right]").scale(1).to_corner(RIGHT)
        label_ineq[0].set_color(YELLOW)
        label_ineq[2].set_color(BLUE_B)
        label_ineq[5].set_color(ORANGE)
        self.add(label_ineq)

    def add_moment_explicaton(self):
        # self.background.fade(.5)
        label_mu = TexMobject(r"(u_1, v_1, \ldots ) \sim", r"\mu")
        label_mu_g = TexMobject(r"E_\mu", "[g(t, u_i + t v_i)", "f^2(u_1, v_1, \ldots)", r"] \ge 0", r"\\ \forall f \quad \forall t \in  \left[i \frac{T}s, (i+1) \frac{T}s\right]").\
                    scale(.8)
        label_f = TexMobject(r"f","\in \mathbb R_r[u_1, v_1, \ldots]")

        label_mu_g[0].set_color(RED_A)
        label_mu_g[1].set_color(YELLOW)
        label_mu_g[2].set_color(PURPLE_A)
        label_mu[1].set_color(RED_A)
        label_f[0].set_color(PURPLE_A)

        label_mu.to_corner(UL).shift(DOWN)
        label_mu_g.next_to(label_mu, DOWN, LARGE_BUFF)
        label_f.to_corner(DL).shift(UP)
        align_group_text([label_mu, label_mu_g, label_f])
        label_mu_g[-1].shift(1.2*LEFT)
        self.add(label_mu)
        add_black_screen(self)
        self.add(label_mu_g)
        add_black_screen(self)
        self.add(label_f)

    def add_tv_sdp(self):
       label_tvsdp = TextMobject(r"This is an SDP!")
       label_tvsdp.to_corner(DR).shift(UP*.7+LEFT)
       rect = Rectangle(fill_color=BLUE_E, fill_opacity=.1, color=BLUE_E)\
           .surround(label_tvsdp)\
           .scale(1.1)

       self.add(VGroup(label_tvsdp, rect))






# Local Variables:
# compile-command: "/home/bachir/.local/bin/manim piecewise.py Piecewise -mp -c=#000000"
# End:
