CG Lab 01 - Part 1 (in class) - starter files
=============================================

1. Create a folder, e.g. D:\cg-lab01, and a virtual environment in it:
       python -m venv .venv
       .venv\Scripts\activate            (macOS/Linux: source .venv/bin/activate)
2. Put ALL files of this ZIP directly in that folder, next to .venv (no sub-folder).
3. Install the libraries:
       pip install -r requirements.txt
   (= PyOpenGL, numpy, pygame, pyrr)
4. Check your setup:
       python check_env.py              -> must end with "OK - GLUT works"
5. Run an exercise, e.g.:
       python ex1_1_fan.py
   Complete the TODOs in ex1_1_fan.py ... ex5_hello2d.py.
   Do not modify window_glut.py.
