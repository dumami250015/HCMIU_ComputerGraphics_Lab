# Exercise 4B Starter - Pentagram (Complete) + Labels
import math
from OpenGL.GL import *
from OpenGL.GLUT import glutMainLoop
from window_glut import Simple2DApp

def star_points_regular(cx, cy, R):
    # TODO: compute outer[5] and inner[5] with r = R * sin(18deg)/sin(54deg)
    outer, inner = [], []
    return outer, inner

class App(Simple2DApp):
    def draw(self):
        W,H = self.width, self.height
        cx, cy = W*0.5, H*0.55
        R = min(W, H) * 0.32

        # TODO: get outer, inner = star_points_regular(cx, cy, R)
        # TODO: build ring and fill with GL_TRIANGLE_FAN
        # TODO: draw pentagram outline using order = [0,2,4,1,3,0]
        # TODO: label p1..p5 near the outer vertices, and add caption

if __name__ == "__main__":
    App(800, 600, b"Ex4B - Pentagram Complete")
    glutMainLoop()
