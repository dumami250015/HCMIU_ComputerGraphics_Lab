# Environment check for CG Lab 1: prints versions and the OpenGL version of your GPU driver.
import sys, platform
print("Python  :", sys.version.split()[0], platform.architecture()[0])
import OpenGL; print("PyOpenGL:", OpenGL.__version__)
import numpy;  print("NumPy   :", numpy.__version__)
try:
    import pygame; print("pygame  :", pygame.version.ver)
except ImportError:
    print("pygame  : NOT INSTALLED (needed for homework)")
from OpenGL.GL import glGetString, GL_VERSION, GL_RENDERER
from OpenGL.GLUT import glutInit, glutInitDisplayMode, glutCreateWindow, GLUT_RGB, glutDestroyWindow
glutInit(); glutInitDisplayMode(GLUT_RGB); win = glutCreateWindow(b"check")
print("OpenGL  :", glGetString(GL_VERSION).decode())
print("GPU     :", glGetString(GL_RENDERER).decode())
glutDestroyWindow(win)
print("OK - GLUT works")
