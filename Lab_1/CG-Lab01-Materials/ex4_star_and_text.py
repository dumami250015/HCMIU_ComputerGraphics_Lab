# Exercise 4A Starter - Star + Caption
import math
from OpenGL.GL import *
from OpenGL.GLUT import glutMainLoop
from window_glut import Simple2DApp

def star_points(cx, cy, R_outer=120, R_inner=50, start_angle_deg=-90):
    # TODO: compute 5 outer and 5 inner points (alternating ring)
    # return list_of_10_vertices
    return []

class App(Simple2DApp):
    def draw(self):
        W,H = self.width, self.height
        cx, cy = W*0.35, H*0.6

        # TODO: call star_points and build the alternating ring
        # TODO: fill star with GL_TRIANGLE_FAN (glBegin/glEnd)
        # TODO: draw outline-only star with self.draw_polyline(..., loop=True)
        # TODO: caption with self.draw_text(..., "This is a star")

if __name__ == "__main__":
    App(900, 600, b"Ex4A - Star + Text")
    glutMainLoop()
