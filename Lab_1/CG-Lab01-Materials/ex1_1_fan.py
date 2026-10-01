# Exercise 1A - Fan of Rays from top-left to diagonal points
from window_glut import Simple2DApp
from OpenGL.GLUT import glutMainLoop

class App(Simple2DApp):
    def draw(self):
        W, H = self.width, self.height
        N = 9

        for i in range(1, N + 1):
            t = i / (N + 1)
            self.draw_line(0, H, W * t, H * t, color=(0, 0, 0), width=1)

        self.draw_line(0, 0, W, H, color=(0, 0, 0), width=1)

if __name__ == "__main__":
    App(400, 400, b"Ex1A - Fan of Rays")
    glutMainLoop()
