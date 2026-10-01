# Exercise 2B - Flower of Circles
import math
from window_glut import Simple2DApp
from OpenGL.GLUT import glutMainLoop

class App(Simple2DApp):
    def draw(self):
        W, H = self.width, self.height
        cx, cy = W * 0.5, H * 0.5
        N = 24
        r = min(W, H) * 0.18
        R = r

        for k in range(N):
            th = 2 * math.pi * k / N
            x = cx + R * math.cos(th)
            y = cy + R * math.sin(th)
            self.draw_oval_outline(x - r, y - r, 2 * r, 2 * r, color=(0, 0, 0), width=2)

        self.draw_oval_outline(cx - 2 * r, cy - 2 * r, 4 * r, 4 * r, color=(0, 0, 0), width=2)
        self.draw_oval_filled(cx - 3, cy - 3, 6, 6, color=(0, 1, 0))

if __name__ == "__main__":
    App(640, 640, b"Ex2B - Flower of Circles")
    glutMainLoop()
