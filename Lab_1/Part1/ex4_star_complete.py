# Exercise 4B Starter - Pentagram (Complete) + Labels
import math
from OpenGL.GL import *
from OpenGL.GLUT import glutMainLoop
from window_glut import Simple2DApp

def star_points_regular(cx, cy, R):
    # TODO: compute outer[5] and inner[5] with r = R * sin(18deg)/sin(54deg)
    r = R * math.sin(math.radians(18)) / math.sin(math.radians(54))
    outer = []
    inner = []
    for i in range(5):
        # Outer tips: start at -90° (top), spaced 72° apart
        a_out = math.radians(-90 + 72 * i)
        outer.append((cx + R * math.cos(a_out), cy + R * math.sin(a_out)))
        # Inner valleys: offset by 36°
        a_in = math.radians(-90 + 72 * i + 36)
        inner.append((cx + r * math.cos(a_in), cy + r * math.sin(a_in)))
    return outer, inner

class App(Simple2DApp):
    def draw(self):
        W,H = self.width, self.height
        cx, cy = W*0.5, H*0.55
        R = min(W, H) * 0.32

        # TODO: get outer, inner = star_points_regular(cx, cy, R)
        outer, inner = star_points_regular(cx, cy, R)

        # TODO: build ring and fill with GL_TRIANGLE_FAN
        ring = []
        for i in range(5):
            ring.append(outer[i])
            ring.append(inner[i])
            
        glColor3f(1.0, 0.85, 0.1)
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(cx, cy)         
        for (x, y) in ring:
            glVertex2f(x, y)
        glVertex2f(ring[0][0], ring[0][1])  
        glEnd()

        # TODO: draw pentagram outline using order = [0,2,4,1,3,0]
        order = [0, 2, 4, 1, 3, 0]
        penta_pts = [outer[i] for i in order]
        self.draw_polyline(penta_pts, color=(0, 0, 0), width=2)

        # TODO: label p1..p5 near the outer vertices, and add caption
        for i, (x, y) in enumerate(outer):
            label = f"p{i+1}({int(x)},{int(y)})"
            self.draw_text(x - 30, y + 10, label, color=(1, 0, 0))

        self.draw_text(cx - 50, cy - R - 40, "This is a star", color=(0, 0, 0))

if __name__ == "__main__":
    App(800, 600, b"Ex4B - Pentagram Complete")
    glutMainLoop()
