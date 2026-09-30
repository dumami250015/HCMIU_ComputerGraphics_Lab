# Exercise 3 Starter - Rectangles & Ellipses (Outlines)
from window_glut import Simple2DApp
from OpenGL.GLUT import glutMainLoop

class App(Simple2DApp):
    def draw(self):
        # TODO: at least 2 rectangles and 2 ellipses using outline helpers
        # self.draw_rect_outline(80, 80, 200, 120, color=(0.1,0.1,0.8), width=2)
        # self.draw_rect_outline(340, 100, 160, 240, color=(0.8,0.1,0.1), width=3)
        # self.draw_oval_outline(80, 280, 200, 120, color=(0.1,0.6,0.1), width=2)
        # self.draw_oval_outline(360, 80, 120, 120, color=(0.6,0,0.6), width=3)
        pass

if __name__ == "__main__":
    App(800, 600, b"Ex3 - Rectangles & Ellipses")
    glutMainLoop()
