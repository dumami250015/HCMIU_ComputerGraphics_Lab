# Exercise 2A Starter - Colored Filled Circles (3x2 grid)
from window_glut import Simple2DApp
from OpenGL.GLUT import glutMainLoop

class App(Simple2DApp):
    def draw(self):
        # Suggested grid parameters
        cx0, cy0 = 120, 120
        dx, dy = 140, 140
        r = 50
        colors = [
            (1.0, 0.2, 0.2), (1.0, 0.6, 0.2), (1.0, 0.9, 0.2),
            (0.2, 0.8, 0.2), (0.2, 0.6, 1.0), (0.6, 0.2, 1.0),
        ]

        # TODO: nested loop, use k to pick colors[k % len(colors)]
        # x = cx0 + col*dx - r; y = cy0 + row*dy - r
        # self.draw_oval_filled(x, y, 2*r, 2*r, color=...)
        # self.draw_oval_outline(x, y, 2*r, 2*r, color=(0,0,0), width=2)

if __name__ == "__main__":
    App(800, 600, b"Ex2A - Colored Circle Grid")
    glutMainLoop()
