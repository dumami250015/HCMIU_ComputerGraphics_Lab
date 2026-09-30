# Exercise 1B Starter - Axes + Main Line
from window_glut import Simple2DApp
from OpenGL.GLUT import glutMainLoop

class App(Simple2DApp):
    def draw(self):
        W, H = self.width, self.height
        cx, cy = W//2, H//2

        # TODO: axes
        self.draw_line(40, cy, W - 40, cy, color=(0.8, 0.8, 0.8), width=1)
        self.draw_line(cx, 40, cx, H - 40, color=(0.8, 0.8, 0.8), width=1)

        # TODO: main line (thicker)
        self.draw_line(100, 100, W - 100, H - 120, color=(0, 0, 0), width=3)

if __name__ == "__main__":
    App(800, 600, b"Ex1B - Axes + Line")
    glutMainLoop()
