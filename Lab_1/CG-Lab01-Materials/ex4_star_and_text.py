# Exercise 4A - Star + Caption
import math
from OpenGL.GL import *
from OpenGL.GLUT import glutMainLoop
from window_glut import Simple2DApp

def star_points(cx, cy, R_outer=120, R_inner=50, start_angle_deg=-90):
    pts = []
    for i in range(5):
        angle_out = math.radians(start_angle_deg + 72 * i)
        pts.append((cx + R_outer * math.cos(angle_out),
                     cy + R_outer * math.sin(angle_out)))
        angle_in = math.radians(start_angle_deg + 72 * i + 36)
        pts.append((cx + R_inner * math.cos(angle_in),
                     cy + R_inner * math.sin(angle_in)))
    return pts

class App(Simple2DApp):
    def draw(self):
        W, H = self.width, self.height

        # Filled star (left)
        cx1, cy1 = W * 0.35, H * 0.6
        pts1 = star_points(cx1, cy1, R_outer=120, R_inner=50)
        glColor3f(1.0, 0.85, 0.1)
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(cx1, cy1)
        for (x, y) in pts1:
            glVertex2f(x, y)
        glVertex2f(pts1[0][0], pts1[0][1])
        glEnd()
        self.draw_polyline(pts1, color=(0, 0, 0), width=2, loop=True)
        self.draw_text(cx1 - 55, cy1 - 160, "This is a star", color=(0, 0, 0))

        # Outline star (right)
        cx2, cy2 = W * 0.7, H * 0.6
        pts2 = star_points(cx2, cy2, R_outer=100, R_inner=42)
        self.draw_polyline(pts2, color=(0.0, 0.0, 0.8), width=2, loop=True)
        self.draw_text(cx2 - 55, cy2 - 140, "This is a star", color=(0, 0, 0))

if __name__ == "__main__":
    App(900, 600, b"Ex4A - Star + Text")
    glutMainLoop()
