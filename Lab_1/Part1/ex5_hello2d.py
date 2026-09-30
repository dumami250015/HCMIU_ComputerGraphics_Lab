# Exercise 5 Starter - Hello 2D Transforms + Filled Ellipses
from OpenGL.GL import *
from OpenGL.GLUT import glutMainLoop
from window_glut import Simple2DApp
import math

class App(Simple2DApp):
    def draw_ellipse_outline(self, cx, cy, rx, ry, color=(0,0,1), width=2, segments=120):
        glColor3f(*color); glLineWidth(width)
        glBegin(GL_LINE_LOOP)
        for i in range(segments):
            t = 2.0*math.pi*(i/segments)
            glVertex2f(cx + rx*math.cos(t), cy + ry*math.sin(t))
        glEnd()

    def draw_ellipse_filled(self, cx, cy, rx, ry, color=(0,0,1,1), segments=120):
        # TODO: implement triangle-fan filled ellipse (center first, then rim)
        glColor4f(*color)        
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(cx, cy)             
        for i in range(segments + 1):   
            t = 2.0 * math.pi * (i / segments)
            glVertex2f(cx + rx * math.cos(t), cy + ry * math.sin(t))
        glEnd() 

    def draw(self):
        glEnable(GL_BLEND); glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glPushMatrix()
        # TODO: apply Translate -> Scale -> Rotate
        glTranslatef(300, 200, 0)
        glScalef(2.0, 2.0, 1.0)
        glRotatef(30.0, 0, 0, 1)

        # TODO: draw first ellipse (fill then outline)
        self.draw_ellipse_filled(0, 0, 100, 50, color=(0.1,0.6,1.0,0.35))
        self.draw_ellipse_outline(0, 0, 100, 50, color=(0,0,1), width=2)

        # TODO: second ellipse (different radii/color)
        self.draw_ellipse_filled(0, 0, 50, 100, color=(1.0,0.2,0.6,0.35))
        self.draw_ellipse_outline(0, 0, 50, 100, color=(0.6,0.0,0.3), width=2)

        # TODO: caption
        self.draw_text(0, 0, "Hello 2D", color=(0,0,0))
        glPopMatrix()

if __name__ == "__main__":
    App(640, 480, b"Ex5 - Hello 2D")
    glutMainLoop()
