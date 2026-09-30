CG Lab 01 - Part 2 (homework) - materials
=========================================

One folder per exercise, because each exercise has its OWN shaders/vertex.txt
and shaders/fragment.txt:

    ex1/  window.py              (+ cat.png, an example image)
    ex2/  triangle.py            + shaders/
    ex3/  textured_triangle.py   + shaders/ + gfx/ (cat.png, wood.jpeg)
    ex4/  spinningCube.py        + shaders/ + gfx/ (cat.png, wood.jpeg)

Install (inside your activated .venv):
    pip install PyOpenGL numpy pygame pyrr        (pyrr is needed for ex4)

Run each program FROM ITS OWN FOLDER, e.g.:
    cd ex2
    python triangle.py

Keep each exercise in its own folder when you submit (shaders are different).
Tasks: see Lab1.pdf, Part 2.
