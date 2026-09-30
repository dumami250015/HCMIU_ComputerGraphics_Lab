
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np

class Simple2DApp:
    def __init__(self, width=800, height=600, title=b"Lab Window"):
        self.width = width
        self.height = height
        self.title = title
        self.bg = (1.0, 1.0, 1.0, 1.0)
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_MULTISAMPLE)
        glutInitWindowSize(self.width, self.height)
        glutCreateWindow(self.title)
        glClearColor(*self.bg)
        glEnable(GL_MULTISAMPLE)
        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        self._set_ortho(self.width, self.height)
        glutDisplayFunc(self._display)
        glutReshapeFunc(self._reshape)
        glutKeyboardFunc(self._keyboard)

    def _set_ortho(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION); glLoadIdentity()
        gluOrtho2D(0, w, 0, h)
        glMatrixMode(GL_MODELVIEW); glLoadIdentity()

    def _display(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        self.draw()
        glutSwapBuffers()

    def _reshape(self, w, h):
        if h == 0: h = 1
        self.width, self.height = w, h
        self._set_ortho(w, h)
        glutPostRedisplay()

    def _keyboard(self, key, x, y):
        if key in (b'\x1b', b'q'):
            try:
                glutLeaveMainLoop()
            except Exception:
                import sys; sys.exit(0)

    # override
    def draw(self): pass

    # helpers
    def draw_line(self, x0, y0, x1, y1, color=(0,0,0), width=1.5):
        glColor3f(*color); glLineWidth(width)
        glBegin(GL_LINES); glVertex2f(x0,y0); glVertex2f(x1,y1); glEnd()

    def draw_rect_outline(self, x, y, w, h, color=(0,0,0), width=1.5):
        glColor3f(*color); glLineWidth(width)
        glBegin(GL_LINE_LOOP)
        glVertex2f(x,y); glVertex2f(x+w,y); glVertex2f(x+w,y+h); glVertex2f(x,y+h)
        glEnd()

    def draw_rect_filled(self, x, y, w, h, color=(0,0,0)):
        glColor3f(*color)
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(x,y); glVertex2f(x+w,y); glVertex2f(x+w,y+h); glVertex2f(x,y+h)
        glEnd()

    def draw_oval_outline(self, x, y, w, h, color=(0,0,0), width=1.5, segments=128):
        glColor3f(*color); glLineWidth(width)
        rx, ry = w/2.0, h/2.0; cx, cy = x+rx, y+ry
        glBegin(GL_LINE_LOOP)
        for i in range(segments):
            t = 2.0*np.pi*(i/segments)
            glVertex2f(cx + rx*np.cos(t), cy + ry*np.sin(t))
        glEnd()

    def draw_oval_filled(self, x, y, w, h, color=(0,0,0), segments=128):
        glColor3f(*color)
        rx, ry = w/2.0, h/2.0; cx, cy = x+rx, y+ry
        glBegin(GL_TRIANGLE_FAN); glVertex2f(cx,cy)
        for i in range(segments+1):
            t = 2.0*np.pi*(i/segments)
            glVertex2f(cx + rx*np.cos(t), cy + ry*np.sin(t))
        glEnd()

    def draw_polyline(self, pts, color=(0,0,0), width=1.5, loop=False):
        glColor3f(*color); glLineWidth(width)
        glBegin(GL_LINE_LOOP if loop else GL_LINE_STRIP)
        for (x,y) in pts: glVertex2f(x,y)
        glEnd()

    def draw_text(self, x, y, text, color=(0,0,0)):
        glColor3f(*color); glRasterPos2f(x, y)
        for ch in text: glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
