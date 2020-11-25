#!/usr/bin/env python3
DEBUG =False
NUM_BLACK_SCREENS = 0
from manimlib.imports import *
import numpy as np


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


class MomentLift(Scene):
    def construct(self):

        f1 = TexMobject("{", "a_{1}","\over","b_{1}", "}"," = ","{","a_{2}","\over","b_{2}","}")
        f1.set_color_by_tex("a_{1}", color=RED, substring=False)
        f1.set_color_by_tex("a_{2}", color=RED, substring=False)
        f1.set_color_by_tex("b_{1}", color=YELLOW, substring=False)
        f1.set_color_by_tex("b_{2}", color=YELLOW, substring=False)
        self.add(f1)
        self.wait(1)



class RigorousApproach(MovingCameraScene):
    def construct(self):
       self.setup_labels()
       # self.add(*self.labels)
       self.wait(1.)

    def setup_labels(self):
        label_shortest_path = TextMobject(r"Shortest Feasible\\ Path").scale(.8)
        circ_shortest_path = Circle(color=PURPLE_A)
        circ_shortest_path.surround(label_shortest_path)
        circ_shortest_path.scale(.9)

        label_le = TexMobject(r"\le").scale(2)
        label_le_2 = label_le.copy()
        label_le.next_to(circ_shortest_path, RIGHT, LARGE_BUFF)
        label_le_2.next_to(circ_shortest_path, LEFT, LARGE_BUFF)

        self.play(ShowCreation(VGroup(label_shortest_path, circ_shortest_path,)))
        add_black_screen(self)
        self.play(Write(label_le))
        add_black_screen(self)
        self.play(Write(label_le))
        add_black_screen(self)
        return


        self.play(
            # Move the camera to the object
            self.camera_frame.shift, 4*RIGHT
        )
        self.remove(label_converge)
        self.wait(.5)






# Local variables:
# eval: (my-buffer-local-set-key (kbd "C-c C-a") (lambda ()  (interactive) (async-shell-command "cd .. && make mpv")))
# eval: (my-buffer-local-set-key (kbd "C-c C-b") (lambda ()  (interactive) (async-shell-command "cd .. && make play")))
# compile-command: "cd .. && make  hq && make play"
# END:
