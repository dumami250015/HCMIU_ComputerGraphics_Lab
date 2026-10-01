# Exercise 2A - Colored Filled Circles (3x2 grid)
from window_glut import Simple2DApp
from OpenGL.GLUT import glutMainLoop

class App(Simple2DApp):
    def draw(self):
        cx0, cy0 = 120, 120
        dx, dy = 140, 140
        r = 50
        colors = [
            (1.0, 0.2, 0.2), (1.0, 0.6, 0.2), (1.0, 0.9, 0.2),
            (0.2, 0.8, 0.2), (0.2, 0.6, 1.0), (0.6, 0.2, 1.0),
        ]

        k = 0
        for row in range(2):
            for col in range(3):
                cx = cx0 + col * dx
                cy = cy0 + row * dy
                x = cx - r
                y = cy - r
                self.draw_oval_filled(x, y, 2 * r, 2 * r, color=colors[k % len(colors)])
                self.draw_oval_outline(x, y, 2 * r, 2 * r, color=(0, 0, 0), width=2)
                k += 1

if __name__ == "__main__":
    App(800, 600, b"Ex2A - Colored Circle Grid")
    glutMainLoop()
