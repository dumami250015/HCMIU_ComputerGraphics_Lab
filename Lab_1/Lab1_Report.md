# Computer Graphics — Lab 1 Report

**Course:** Introduction to Computer Graphics  
**Instructor:** MSc. Thai Trung Tin  
**Institution:** International University — HCMIU  
**Date:** October 2026

---

## Abstract

This report documents the completion of Lab 1 for the Computer Graphics course. The lab is divided into two parts: **Part 1** covers in-class exercises using the GLUT fixed-function pipeline (8 exercises), and **Part 2** covers homework exercises using the modern OpenGL 3.3 core profile with Pygame and GLSL shaders (4 exercises). For each exercise, we present the original template code, describe the modifications made to complete the tasks, provide the final solution code, and explain the underlying computer graphics concepts.

---

## 1. Introduction

This lab introduces foundational concepts in computer graphics programming using Python and OpenGL. The exercises progress from basic 2D line drawing through geometric primitives, transformations, and finally to shader-based rendering with textures and 3D transformations.

**Technologies used:**
- **Part 1:** Python, PyOpenGL, GLUT (fixed-function pipeline), NumPy
- **Part 2:** Python, PyOpenGL, Pygame, GLSL shaders, Pyrr (matrix library)

**Environment setup:**
```bash
pip install PyOpenGL numpy pygame pyrr
```

---

## 2. Part 1: In-Class Practices and Exercises

All Part 1 exercises share a common framework provided in `window_glut.py`. This file defines the `Simple2DApp` class, which handles GLUT initialization, sets up a 2D orthographic projection via `gluOrtho2D(0, W, 0, H)` (origin at bottom-left), and provides helper methods for drawing lines, rectangles, ovals, polylines, and text. Students override the `draw()` method in subclasses to implement each exercise.

### 2.1 Exercise 1A — Fan of Rays

**Objective:** Draw N evenly-spaced rays from the top-left corner to points along the window diagonal, plus the diagonal itself.

**Original code (template):**
```python
class App(Simple2DApp):
    def draw(self):
        W, H = self.width, self.height
        N = 9
        # TODO: loop i in [1..N], compute t = i/(N+1), and draw one ray per i
        # TODO: draw the diagonal
```

The template defined the window dimensions and the number of rays `N = 9`, but the loop body and diagonal drawing were left as TODO comments.

**Changes made:**

1. **Added the ray-drawing loop (lines 11–13):** A `for` loop iterates `i` from 1 to N. For each `i`, a parameter `t = i / (N + 1)` is computed. This `t` linearly interpolates from 0 to 1 (exclusive), distributing N points evenly along the diagonal. Each ray is drawn from the top-left corner `(0, H)` to the interpolated point `(W*t, H*t)` on the diagonal.

2. **Added the diagonal line (line 15):** A single call to `self.draw_line(0, 0, W, H, ...)` draws the main diagonal from the bottom-left to the top-right.

**Solution code:**
```python
class App(Simple2DApp):
    def draw(self):
        W, H = self.width, self.height
        N = 9

        for i in range(1, N + 1):
            t = i / (N + 1)
            self.draw_line(0, H, W * t, H * t, color=(0, 0, 0), width=1)

        self.draw_line(0, 0, W, H, color=(0, 0, 0), width=1)
```

**Explanation:** The interpolation formula `t = i/(N+1)` ensures that the first ray at `i=1` starts slightly past the corner and the last ray at `i=N` ends slightly before the opposite corner, creating an evenly-fanned distribution. The `draw_line` helper sets the color via `glColor3f`, sets the line width via `glLineWidth`, and draws using `glBegin(GL_LINES)`.

---

### 2.2 Exercise 1B — Axes + Main Line

**Objective:** Draw faint gray cross-hair axes through the window center and one bold black diagonal line.

**Original code (template):**
```python
class App(Simple2DApp):
    def draw(self):
        W, H = self.width, self.height
        cx, cy = W//2, H//2
        # TODO: axes
        # TODO: main line (thicker)
```

**Changes made:**

1. **Added horizontal axis (line 10):** Draws a gray line from `(40, cy)` to `(W-40, cy)` with `color=(0.8, 0.8, 0.8)` and `width=1`. The 40-pixel margins prevent the axis from touching the window edges.

2. **Added vertical axis (line 11):** Same concept, from `(cx, 40)` to `(cx, H-40)`.

3. **Added main line (line 13):** Draws a bold black diagonal from `(100, 100)` to `(W-100, H-120)` with `width=3` for visual emphasis.

**Solution code:**
```python
class App(Simple2DApp):
    def draw(self):
        W, H = self.width, self.height
        cx, cy = W//2, H//2

        self.draw_line(40, cy, W - 40, cy, color=(0.8, 0.8, 0.8), width=1)
        self.draw_line(cx, 40, cx, H - 40, color=(0.8, 0.8, 0.8), width=1)

        self.draw_line(100, 100, W - 100, H - 120, color=(0, 0, 0), width=3)
```

**Explanation:** The axes are drawn using relative coordinates (`cx`, `cy`) so they stay centered when the window is resized, thanks to the `_reshape` callback in the framework. The main line uses a thicker `width=3` to visually stand out against the gray axes.

---

### 2.3 Exercise 2A — Colored Filled Circles (3×2 Grid)

**Objective:** Draw a 3-column × 2-row grid of filled circles, each with a different color and a black outline.

**Original code (template):**
```python
class App(Simple2DApp):
    def draw(self):
        cx0, cy0 = 120, 120
        dx, dy = 140, 140
        r = 50
        colors = [
            (1.0, 0.2, 0.2), (1.0, 0.6, 0.2), (1.0, 0.9, 0.2),
            (0.2, 0.8, 0.2), (0.2, 0.6, 1.0), (0.6, 0.2, 1.0),
        ]
        # TODO: nested loop, use k to pick colors[k % len(colors)]
```

The template provided grid parameters and a color palette but lacked the nested loop.

**Changes made:**

Added a nested loop with a color counter `k`. For each `(row, col)` combination:
- **Center computation:** `cx = cx0 + col * dx`, `cy = cy0 + row * dy`
- **Bounding box conversion:** The `draw_oval_filled` method takes a bounding box `(x, y, width, height)`, not center/radius. So we convert: `x = cx - r`, `y = cy - r`, `width = height = 2*r`.
- **Draw filled circle** with `colors[k % len(colors)]`, then **draw outline** with black.

**Solution code:**
```python
        color = 0
        for row in range(2):
            for col in range(3):
                x = cx0 + col * dx - r
                y = cy0 + row * dy - r
                self.draw_oval_filled(x, y, 2 * r, 2 * r,
                                      color=colors[color % len(colors)])
                self.draw_oval_outline(x, y, 2 * r, 2 * r,
                                       color=(0, 0, 0), width=2)
                color += 1
```

**Explanation:** The `draw_oval_filled` method internally uses `GL_TRIANGLE_FAN` to fill an ellipse approximation with 128 line segments. The modulo operator `color % len(colors)` allows the palette to cycle if there are more circles than colors. The outline is drawn on top to create a clean border effect.

---

### 2.4 Exercise 2B — Flower of Circles

**Objective:** Draw N equal circles with centers placed on a ring of radius R, all passing through the center point, plus a boundary circle and a green center dot.

**Original code (template):**
```python
class App(Simple2DApp):
    def draw(self):
        W, H = self.width, self.height
        cx, cy = W*0.5, H*0.5
        N = 24
        r = min(W, H)*0.18
        R = r
        # TODO: loop k in [0..N-1]: compute angle, draw circle
```

**Changes made:**

1. **Circle placement loop:** For each `k` in `[0, N-1]`, the angle `th = 2π·k/N` places the circle center at `(cx + R·cos(th), cy + R·sin(th))`. Since `r = R`, each circle passes through the window center, creating the "flower" pattern.

2. **Boundary circle:** A large circle of radius `2r` centered at `(cx, cy)` serves as the outer boundary.

3. **Center dot:** A small filled oval at the center marks the origin.

**Solution code:**
```python
        for k in range(N):
            th = 2 * math.pi * k / N
            x = cx + R * math.cos(th)
            y = cy + R * math.sin(th)
            self.draw_oval_outline(x - r, y - r, 2 * r, 2 * r,
                                   color=(0, 0, 0), width=2)

        self.draw_oval_outline(cx - 2*r, cy - 2*r, 4*r, 4*r,
                               color=(0, 0, 0), width=2)
        self.draw_oval_filled(cx - 3, cy - 3, 6, 6, color=(0, 1, 0))
```

**Explanation:** The key insight is that setting `r = R` (circle radius equals ring radius) ensures every circle passes through the center `(cx, cy)`. This is because the distance from the center to any circle's center is `R`, and each circle has radius `r = R`, so the center point lies exactly on each circle's circumference. The 24 overlapping circles create the characteristic petal-like "flower" pattern.

---

### 2.5 Exercise 3 — Rectangles & Ellipses (Outlines)

**Objective:** Draw at least two rectangles and two ellipses with different sizes, positions, colors, and stroke widths.

**Original code (template):**
```python
class App(Simple2DApp):
    def draw(self):
        # TODO: at least 2 rectangles and 2 ellipses using outline helpers
        pass
```

**Changes made:**

Replaced `pass` with four drawing calls using different colors and line widths:

**Solution code:**
```python
class App(Simple2DApp):
    def draw(self):
        self.draw_rect_outline(100, 100, 200, 120, color=(0.1, 0.1, 0.8), width=2)
        self.draw_rect_outline(340, 100, 160, 240, color=(0.8, 0.1, 0.5), width=3)
        self.draw_oval_outline(80, 280, 200, 120, color=(0.1, 0.6, 0.1), width=2)
        self.draw_oval_outline(360, 180, 120, 120, color=(0.6, 0, 0.6), width=3)
```

**Explanation:** Both `draw_rect_outline` and `draw_oval_outline` take bounding box parameters `(x, y, width, height)`. The rectangle helper uses `GL_LINE_LOOP` with four vertices; the oval helper approximates the ellipse with 128 line segments. By varying the width/height ratio, we get rectangles of different aspect ratios and ellipses vs. circles (when `width == height`).

---

### 2.6 Exercise 4A — Star + Caption

**Objective:** Compute the 10 vertices of a five-pointed star (5 outer tips + 5 inner valleys), draw one filled star and one outline-only star, and add text captions.

**Original code (template):**
```python
def star_points(cx, cy, R_outer=120, R_inner=50, start_angle_deg=-90):
    # TODO: compute 5 outer and 5 inner points (alternating ring)
    return []

class App(Simple2DApp):
    def draw(self):
        W, H = self.width, self.height
        # TODO: call star_points, fill with GL_TRIANGLE_FAN, draw outline, add text
```

**Changes made:**

1. **Implemented `star_points` function:** For each of the 5 points (`i = 0..4`):
   - **Outer tip:** angle = `start_angle_deg + 72° × i` (360°/5 = 72° spacing), position = `(cx + R_outer·cos(angle), cy + R_outer·sin(angle))`
   - **Inner valley:** angle shifted by +36° (halfway between outer tips), position = `(cx + R_inner·cos(angle), cy + R_inner·sin(angle))`
   - Points are appended alternating: outer, inner, outer, inner, ... creating a 10-point ring.

2. **Filled star:** Uses `GL_TRIANGLE_FAN` with the center `(cx, cy)` as the hub vertex and the 10 ring points as the fan. The fan closes by repeating the first ring point.

3. **Outline star:** Uses `self.draw_polyline(..., loop=True)` which renders the 10-point ring as a closed `GL_LINE_LOOP`.

4. **Captions:** `self.draw_text(...)` renders text using `glutBitmapCharacter` with the Helvetica 18 font.

**Solution code:**
```python
def star_points(cx, cy, R_outer=120, R_inner=50, start_angle_deg=-90):
    pts = []
    for i in range(5):
        angle_out = math.radians(start_angle_deg + 72 * i)
        pts.append((cx + R_outer * math.cos(angle_out),
                     cy + R_outer * math.sin(angle_out)))
        angle_in = math.radians(start_angle_deg + 72 * i + 36)
        pts.append((cx + R_inner * math.cos(angle_in),
                     cy + R_inner * math.sin(angle_in)))
    return pts

class App(Simple2DApp):
    def draw(self):
        W, H = self.width, self.height

        # Filled star
        cx1, cy1 = W * 0.35, H * 0.6
        pts1 = star_points(cx1, cy1, R_outer=120, R_inner=50)
        glColor3f(1.0, 0.85, 0.1)
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(cx1, cy1)
        for (x, y) in pts1:
            glVertex2f(x, y)
        glVertex2f(pts1[0][0], pts1[0][1])
        glEnd()
        self.draw_polyline(pts1, color=(0, 0, 0), width=2, loop=True)
        self.draw_text(cx1 - 60, cy1 - 160, "This is a star", color=(0, 0, 0))

        # Outline-only star
        cx2, cy2 = W * 0.7, H * 0.6
        pts2 = star_points(cx2, cy2, R_outer=100, R_inner=42)
        self.draw_polyline(pts2, color=(0.0, 0.0, 0.8), width=2, loop=True)
        self.draw_text(cx2 - 60, cy2 - 140, "This is a star", color=(0, 0, 0))
```

**Explanation:** Starting at -90° places the topmost point at 12 o'clock. The `GL_TRIANGLE_FAN` primitive efficiently fills the star by creating triangles that all share the center vertex, radiating outward through alternating outer and inner points. The 36° offset for inner points places them exactly between adjacent outer tips.

---

### 2.7 Exercise 4B — Pentagram (Complete) + Labels

**Objective:** Render a mathematically correct pentagram using the formula for the inner radius, fill it, draw the pentagram outline by connecting every 2nd outer vertex, and label vertices.

**Original code (template):**
```python
def star_points_regular(cx, cy, R):
    # TODO: compute outer[5] and inner[5] with r = R * sin(18°)/sin(54°)
    return [], []

class App(Simple2DApp):
    def draw(self):
        # TODO: get points, fill, draw pentagram outline, label
```

**Changes made:**

1. **Inner radius formula:** `r = R × sin(18°) / sin(54°)`. This formula derives from the geometry of a regular pentagram — the intersection points of the diagonals of a regular pentagon divide each diagonal in the golden ratio. This yields `r ≈ 0.382 × R`.

2. **Pentagram outline order:** Instead of connecting adjacent outer points (which would draw a regular pentagon), the pentagram connects every 2nd vertex: `0 → 2 → 4 → 1 → 3 → 0`. This creates the characteristic five-pointed star with crossing lines.

3. **Vertex labels:** Each outer vertex is labeled `p1(x,y)` through `p5(x,y)` using `draw_text`.

**Solution code:**
```python
def star_points_regular(cx, cy, R):
    r = R * math.sin(math.radians(18)) / math.sin(math.radians(54))
    outer, inner = [], []
    for i in range(5):
        a_out = math.radians(-90 + 72 * i)
        outer.append((cx + R * math.cos(a_out), cy + R * math.sin(a_out)))
        a_in = math.radians(-90 + 72 * i + 36)
        inner.append((cx + r * math.cos(a_in), cy + r * math.sin(a_in)))
    return outer, inner

class App(Simple2DApp):
    def draw(self):
        W, H = self.width, self.height
        cx, cy = W*0.5, H*0.55
        R = min(W, H) * 0.32

        outer, inner = star_points_regular(cx, cy, R)

        # Build alternating ring and fill
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

        # Pentagram outline (skip-one connection)
        order = [0, 2, 4, 1, 3, 0]
        penta_pts = [outer[i] for i in order]
        self.draw_polyline(penta_pts, color=(0, 0, 0), width=2)

        # Labels
        for i, (x, y) in enumerate(outer):
            label = f"p{i+1}({int(x)},{int(y)})"
            self.draw_text(x - 30, y + 10, label, color=(1, 0, 0))

        self.draw_text(cx - 50, cy - R - 40, "This is a star", color=(0, 0, 0))
```

**Explanation:** The difference from Ex 4A is the mathematically derived inner radius and the skip-connection outline. The `sin(18°)/sin(54°)` formula ensures the inner valleys fall exactly at the intersection points of the pentagram's diagonals, making the star geometrically regular. The outline order `[0, 2, 4, 1, 3, 0]` draws a continuous path that visits each outer tip while skipping one between each pair, forming the iconic five-pointed star pattern.

---

### 2.8 Exercise 5 — Hello 2D Transforms + Filled Ellipses

**Objective:** Implement a filled ellipse using `GL_TRIANGLE_FAN`, apply 2D transformations (translate, scale, rotate), and draw two semi-transparent overlapping ellipses with a caption.

**Original code (template):**
```python
class App(Simple2DApp):
    def draw_ellipse_filled(self, cx, cy, rx, ry, color=(0,0,1,1), segments=120):
        # TODO: implement triangle-fan filled ellipse
        pass

    def draw(self):
        # TODO: apply Translate -> Scale -> Rotate, draw ellipses
        pass
```

**Changes made:**

1. **`draw_ellipse_filled` implementation:** Uses `GL_TRIANGLE_FAN` with `glColor4f` (4-component color for alpha transparency). The center vertex is placed first, then `segments+1` rim vertices are computed parametrically: `x = cx + rx·cos(t)`, `y = cy + ry·sin(t)` for `t ∈ [0, 2π]`.

2. **Transformation stack:** The draw method uses `glPushMatrix`/`glPopMatrix` to isolate the transform. The transformation order is:
   - `glTranslatef(300, 200, 0)` — move to position (300, 200)
   - `glScalef(2.0, 2.0, 1.0)` — double the size
   - `glRotatef(30.0, 0, 0, 1)` — rotate 30° around the Z-axis

   **Important:** In OpenGL's fixed pipeline, transformations are applied in reverse order. So the geometry is first rotated, then scaled, then translated.

3. **Alpha blending:** `glEnable(GL_BLEND)` with `glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)` enables semi-transparent fills. The ellipses use alpha = 0.35 for a translucent effect.

**Solution code:**
```python
class App(Simple2DApp):
    def draw_ellipse_filled(self, cx, cy, rx, ry, color=(0,0,1,1), segments=120):
        glColor4f(*color)
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(cx, cy)
        for i in range(segments + 1):
            t = 2.0 * math.pi * (i / segments)
            glVertex2f(cx + rx * math.cos(t), cy + ry * math.sin(t))
        glEnd()

    def draw(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glPushMatrix()

        glTranslatef(300, 200, 0)
        glScalef(2.0, 2.0, 1.0)
        glRotatef(30.0, 0, 0, 1)

        self.draw_ellipse_filled(0, 0, 100, 50, color=(0.1, 0.6, 1.0, 0.35))
        self.draw_ellipse_outline(0, 0, 100, 50, color=(0, 0, 1), width=2)

        self.draw_ellipse_filled(0, 0, 50, 100, color=(1.0, 0.2, 0.6, 0.35))
        self.draw_ellipse_outline(0, 0, 50, 100, color=(0.6, 0.0, 0.3), width=2)

        self.draw_text(0, 0, "Hello 2D", color=(0, 0, 0))
        glPopMatrix()
```

**Explanation:** The two ellipses have swapped radii `(rx=100, ry=50)` and `(rx=50, ry=100)`, creating a horizontal and vertical ellipse respectively. When overlaid with the 30° rotation and semi-transparent fills, the overlapping region shows the blended color, demonstrating both the transformation pipeline and alpha compositing. Drawing at the origin `(0, 0)` and relying on the matrix stack for positioning is a clean pattern that separates geometry definition from placement.

---

## 3. Part 2: Homework Exercises

Part 2 uses the modern OpenGL pipeline with **Pygame** for window management and **GLSL shaders** for rendering. Unlike Part 1's fixed-function approach, this pipeline requires explicit vertex buffers, shaders, and texture management.

### 3.1 Homework Exercise 1 — Background Practice with PyOpenGL

**Objective:** Practice setting background colors and displaying images as backgrounds using OpenGL textures.

#### Task 1: Solid Background Color

**Original code:**
```python
def _set_up_opengl(self) -> None:
    if self.mode == 1:
        # TODO(Part 1): Change these numbers to different RGB values
        pass
```

The original had a `pass` statement where `glClearColor` should be called.

**Solution code:**
```python
def _set_up_opengl(self) -> None:
    if self.mode == 1:
        glClearColor(0, 0, 1, 1)  # Blue background
```

**Changes and explanation:** Replaced `pass` with `glClearColor(0, 0, 1, 1)`. This sets the clear color to blue (R=0, G=0, B=1, A=1). Every frame, `glClear(GL_COLOR_BUFFER_BIT)` fills the framebuffer with this color. The four parameters represent RGBA values in the range [0.0, 1.0].

#### Task 2: Background Image

**Original code:**
```python
if self.mode == 2:
    # TODO(Part 2): replace with your image file
    pass
```

and at the bottom:
```python
myApp = App(mode=1)
```

**Solution code:**
```python
if self.mode == 2:
    self.bg_tex = self._load_texture("background.jpg")
```

and:
```python
myApp = App(mode=2)
```

**Changes and explanation:**
1. **Loaded the texture:** Replaced `pass` with `self.bg_tex = self._load_texture("background.jpg")`. The `_load_texture` method loads an image using Pygame's `pg.image.load`, converts it to raw bytes with `pg.image.tostring`, creates an OpenGL texture object, and uploads the pixel data via `glTexImage2D`.

2. **Switched to mode 2:** Changed the constructor call to `App(mode=2)` to activate the image background mode.

3. **Flipped texture coordinates:** In `_draw_background`, the texture coordinates were modified from:
   ```python
   glTexCoord2f(0, 0); glVertex2f(-1, -1)
   glTexCoord2f(1, 0); glVertex2f( 1, -1)
   glTexCoord2f(1, 1); glVertex2f( 1,  1)
   glTexCoord2f(0, 1); glVertex2f(-1,  1)
   ```
   to:
   ```python
   glTexCoord2f(0, 1); glVertex2f(-1, -1)
   glTexCoord2f(1, 1); glVertex2f( 1, -1)
   glTexCoord2f(1, 0); glVertex2f( 1,  1)
   glTexCoord2f(0, 0); glVertex2f(-1,  1)
   ```
   This swaps the vertical `t` coordinate, flipping the image vertically to correct for the difference between OpenGL's bottom-up coordinate system and the image's top-down pixel order.

---

### 3.2 Homework Exercise 2 — Introduction to Shaders

**Objective:** Learn the shader pipeline by modifying vertex colors, the fragment shader, and applying transformations in the vertex shader.

**Background — Shader Pipeline:**

In modern OpenGL, the fixed-function pipeline is replaced by programmable shaders:
- **Vertex Shader:** Processes each vertex (position, color) and outputs `gl_Position` (clip-space position) and any varying outputs.
- **Rasterizer:** The GPU interpolates varying outputs across the triangle surface.
- **Fragment Shader:** Computes the final color for each pixel.

The vertex data for the triangle is stored in a **Vertex Buffer Object (VBO)** with 6 floats per vertex: `(x, y, z, r, g, b)`. The stride is 24 bytes (6 × 4).

#### Task 1: Change Vertex Colors

**Original vertex data:**
```python
vertices = (
    -0.5, -0.5, 0.0, 1.0, 0.0, 0.0,   # Red
     0.5, -0.5, 0.0, 0.0, 1.0, 0.0,   # Green
     0.0,  0.5, 0.0, 0.0, 0.0, 1.0    # Blue
)
```

**Solution code:**
```python
vertices = (
    -0.5, -0.5, 0.0, 1.0, 1.0, 0.0,   # Yellow
     0.5, -0.5, 0.0, 0.0, 1.0, 1.0,   # Cyan
     0.0,  0.5, 0.0, 1.0, 1.0, 1.0    # White
)
```

**Explanation:** Changed the RGB color components from `(1,0,0)`, `(0,1,0)`, `(0,0,1)` (primary colors) to `(1,1,0)`, `(0,1,1)`, `(1,1,1)` (yellow, cyan, white). The GPU interpolates these colors across the triangle's surface, producing smooth gradients between the vertices. Yellow = Red+Green, Cyan = Green+Blue, White = all channels at maximum.

#### Task 2: Modify Fragment Shader (Solid Color)

**Original fragment shader:**
```glsl
void main()
{
    color = vec4(fragmentColor, 1.0);
}
```

**Solution fragment shader:**
```glsl
void main()
{
    color = vec4(1.0, 0.0, 0.0, 1.0);   // Always red
}
```

**Explanation:** By hardcoding `vec4(1.0, 0.0, 0.0, 1.0)`, the fragment shader ignores the interpolated `fragmentColor` variable entirely. Every pixel of the triangle receives the same solid red color, eliminating the gradient effect. This demonstrates that the fragment shader has final authority over pixel color.

#### Task 3: Scale in Vertex Shader

**Original vertex shader:**
```glsl
void main()
{
    gl_Position = vec4(vertexPos, 1.0);
    fragmentColor = vertexColor;
}
```

**Solution vertex shader:**
```glsl
void main()
{
    gl_Position = vec4(vertexPos.x * 0.5, vertexPos.y, vertexPos.z, 1.0);
    fragmentColor = vertexColor;
}
```

**Explanation:** Multiplying `vertexPos.x` by 0.5 scales the triangle horizontally to half its original width. In Normalized Device Coordinates (NDC), positions range from -1 to +1, so `x * 0.5` compresses the horizontal extent from [-0.5, 0.5] to [-0.25, 0.25]. The Y coordinate is unchanged, so the triangle becomes narrower but keeps its height — a non-uniform scale.

---

### 3.3 Homework Exercise 3 — Textured Triangle with Shaders

**Objective:** Explore texture mapping by changing textures, modifying texture coordinates, and experimenting with the fragment shader's blending mode.

**Background — Texture Mapping:**

Each vertex now carries 8 floats: `(x, y, z, r, g, b, s, t)` where `(s, t)` are texture coordinates mapping the image onto the geometry. The stride is 32 bytes (8 × 4). The fragment shader samples the texture using `texture(sampler, texCoords)` and can combine the result with vertex colors.

#### Task 1: Change Texture

**Original code:**
```python
self.wood_texture = Material("gfx/wood.jpeg")
```

**Solution code:**
```python
self.wood_texture = Material("gfx/background.png")
```

**Explanation:** Simply changed the file path passed to the `Material` constructor. The `Material` class handles loading any image format supported by Pygame (PNG, JPEG, BMP, etc.), converting it to RGBA pixel data, and uploading it to an OpenGL texture object. The same triangle geometry now displays a different image.

#### Task 2: Experiment with Texture Coordinates

**Original texture coordinates:**
```python
vertices = (
    -0.5, -0.5, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0,   # s=0, t=1 (bottom-left)
     0.5, -0.5, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0,   # s=1, t=1 (bottom-right)
     0.0,  0.5, 0.0, 0.0, 0.0, 1.0, 0.5, 0.0     # s=0.5, t=0 (top-center)
)
```

**Solution code (vertical flip):**
```python
vertices = (
    -0.5, -0.5, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0,   # s=0, t=0
     0.5, -0.5, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0,   # s=1, t=0
     0.0,  0.5, 0.0, 0.0, 0.0, 1.0, 0.5, 1.0     # s=0.5, t=1
)
```

**Explanation:** The `t` coordinates were swapped: bottom vertices changed from `t=1.0` to `t=0.0`, and the top vertex from `t=0.0` to `t=1.0`. This flips the texture vertically on the triangle. The `s` coordinate controls horizontal mapping and was left unchanged. Texture coordinates use the range [0, 1] where (0,0) is typically the top-left of the image.

#### Task 3: Modify Fragment Shader (Blending Modes)

**Original fragment shader:**
```glsl
color = vec4(fragmentColor, 1.0) * texture(imageTexture, fragmentTexCoord);
```

The original multiplies vertex color by texture color, which tints the texture.

**Solution fragment shader (additive blending):**
```glsl
color = vec4(fragmentColor, 1.0) + texture(imageTexture, fragmentTexCoord);
```

**Explanation:** Changing from multiplication (`*`) to addition (`+`) produces additive blending. With multiplication, `vertexColor × textureColor`, dark vertex areas (near 0) make the texture invisible. With addition, `vertexColor + textureColor`, the colors are combined additively, producing a brighter result. Values above 1.0 are clamped, so bright areas appear washed out/white. The commented-out alternatives show:
- `texture(...)` alone — pure texture, no vertex color influence
- `vec4(fragmentColor, 1.0)` alone — pure vertex color gradient, no texture

---

### 3.4 Homework Exercise 4 — Spinning Textured Cube

**Objective:** Explore 3D transformations, texture application on a 3D mesh, rotation control, and shader tinting.

**Background — 3D Pipeline:**

This exercise introduces the model-view-projection pipeline. The vertex shader computes:
```glsl
gl_Position = projection * model * vec4(vertexPos, 1.0);
```
- **Model matrix:** Transforms the cube from local space to world space (rotation + translation)
- **Projection matrix:** Creates perspective distortion (objects farther away appear smaller)

The `Entity` class manages position and rotation. Its `update()` method increments the Y-axis rotation angle each frame, and `get_model_transform()` builds the combined rotation-translation matrix using the `pyrr` library.

#### Task 1: Change Texture

**Original code:**
```python
self.wood_texture = Material("gfx/wood.jpeg")
```

**Solution code:**
```python
self.wood_texture = Material("gfx/cat.png")
```

**Explanation:** Replaced the wood texture with the cat image. Since all six faces of the cube share the same texture and use the full [0,1] × [0,1] UV range, the cat image appears on every face.

#### Task 2: Modify Rotation Speed

**Original code:**
```python
def update(self) -> None:
    self.eulers[1] += 0.25     # 0.25° per frame
```

**Solution code:**
```python
def update(self) -> None:
    self.eulers[1] += 4.0      # 4.0° per frame (16× faster)
```

**Explanation:** Changed from 0.25° to 4.0° per frame. At 60 FPS, the original cube completed one full rotation in `360° / 0.25° × (1/60) ≈ 24 seconds`. The modified version completes a rotation in `360° / 4.0° × (1/60) = 1.5 seconds`, making the spinning visually dramatic.

#### Task 3: Apply Different Transformations

**Original `get_model_transform`:**
```python
model_transform = pyrr.matrix44.create_identity(dtype=np.float32)

model_transform = pyrr.matrix44.multiply(
    m1=model_transform,
    m2=pyrr.matrix44.create_from_axis_rotation(
        axis = [0, 1, 0],          # Y-axis rotation only
        theta = np.radians(self.eulers[1]),
        dtype = np.float32
    )
)
```

**Solution code (added scaling and changed axis):**
```python
model_transform = pyrr.matrix44.create_identity(dtype=np.float32)

# Scale 1.5× larger
scale_matrix = np.array([
    [1.5, 0,   0,   0],
    [0,   1.5, 0,   0],
    [0,   0,   1.5, 0],
    [0,   0,   0,   1]
], dtype=np.float32)
model_transform = pyrr.matrix44.multiply(
    m1=model_transform, m2=scale_matrix
)

model_transform = pyrr.matrix44.multiply(
    m1=model_transform,
    m2=pyrr.matrix44.create_from_axis_rotation(
        axis = [1, 1, 0],          # Diagonal axis (X+Y)
        theta = np.radians(self.eulers[1]),
        dtype = np.float32
    )
)
```

**Changes and explanation:**
1. **Added uniform scaling:** Inserted a 4×4 scale matrix with factor 1.5 on the diagonal. This makes the cube 50% larger in all three dimensions. The scale is applied first (leftmost in the multiplication chain), so it operates in local space before rotation.

2. **Changed rotation axis from `[0, 1, 0]` to `[1, 1, 0]`:** The original rotated around the Y-axis only (like a lazy Susan). The new axis is the diagonal of the XY-plane, making the cube tumble in a more complex, visually interesting pattern. The `pyrr` library normalizes this vector internally before computing the rotation matrix.

#### Task 4: Experiment with Shaders (Tinting)

**Original fragment shader:**
```glsl
void main()
{
    color = texture(imageTexture, fragmentTexCoord);
}
```

**Solution fragment shader:**
```glsl
void main()
{
    color = texture(imageTexture, fragmentTexCoord) * vec4(1.0, 0.5, 0.5, 1.0);
}
```

**Explanation:** Multiplying the texture color by `vec4(1.0, 0.5, 0.5, 1.0)` applies a red tint. The red channel is preserved at full intensity (×1.0), while green and blue channels are halved (×0.5). This shifts the overall color balance toward red/pink. The commented-out alternatives show a blue tint `(0.5, 0.5, 1.0)` and a warm/sepia tint `(1.0, 0.8, 0.6)`.

#### Task 5 (Bonus): Pyramid Mesh

The solution also includes a commented-out pyramid mesh definition in the `CubeMesh` class:
```python
# Pyramid
# apex = (0.0, 0.7, 0.0)
# bl = (-0.5, -0.5, 0.5)    # base front-left
# br = (0.5, -0.5, 0.5)     # base front-right
# tl = (-0.5, -0.5, -0.5)   # base back-left
# tr = (0.5, -0.5, -0.5)    # base back-right
```

This defines a pyramid with 4 triangular side faces and 2 triangles for the square base (6 triangles = 18 vertices total). Each vertex includes texture coordinates so the image wraps around each face independently. Uncommenting this section and commenting out the cube vertices would render a spinning textured pyramid instead.

---

## 4. Conclusion

This lab provided hands-on experience with both the legacy fixed-function OpenGL pipeline and the modern shader-based pipeline. Key concepts practiced include:

- **2D Primitives:** Lines, rectangles, circles, and ellipses using `GL_LINES`, `GL_LINE_LOOP`, and `GL_TRIANGLE_FAN`.
- **Trigonometric geometry:** Computing star vertices, circle placement along rings, and parametric ellipse approximation.
- **Transformation pipeline:** Using `glTranslatef`, `glScalef`, `glRotatef` with matrix stack operations (`glPushMatrix`/`glPopMatrix`).
- **GLSL Shaders:** Writing vertex and fragment shaders to control vertex positioning and pixel coloring.
- **Texture mapping:** Loading images as OpenGL textures, assigning UV coordinates, and sampling textures in fragment shaders.
- **3D Rendering:** Using model and projection matrices with the `pyrr` library for perspective 3D rendering.
- **Alpha blending:** Enabling translucent rendering with `GL_BLEND`.

The progression from simple line drawing to 3D textured objects demonstrates the core concepts of the computer graphics rendering pipeline that underpin all modern graphics applications.

---

## References

1. OpenGL Shading Language Tutorial: https://learnopengl.com/Getting-started/Hello-Triangle
2. PyOpenGL Documentation: http://pyopengl.sourceforge.net/documentation/manual-3.0/
3. Pygame Documentation: https://www.pygame.org/docs/
4. Video Tutorials (provided by instructor):
   - https://www.youtube.com/watch?v=mOTE_62i5ag
   - https://www.youtube.com/watch?v=ZK1WyCMK12E
   - https://www.youtube.com/watch?v=K9NeDMGHzfA
