# **International University** 

School of Computer Science and Engineering 



<!-- Start of picture text -->
AeA Ue)<br>e %,<br>S %<br>Fy g<br>= =<br>sh S)<br>»<br>°Hom-\ ° y<br><!-- End of picture text -->

**Computer Graphics Lab 01 – Introduction to Computer Graphics** 

**Semester: 1, Year: 2026 - 2027 Lab Instructor: MSc. Tran Khai Minh** 

**Full name:** Võ Trí Khôi **Student ID:** ITCSIU24045 **Group:** G01 

## **1. Introduction** 

This report documents the completion of Lab 1 for the Computer Graphics course. For each exercise, we present the original template code, describe the modifications made to complete the tasks, provide the final solution code, and explain the underlying computer graphics concepts. 

## **2. Part 1: In-Class Practices and Exercises** 

### **2.1 Exercise 1A – Fan of Rays** 

### **Original code:** 

class App(Simple2DApp): 

def draw(self): 

W, H = self.width, self.height 

N = 9 

- # TODO: loop i in [1..N], compute t = i/(N+1), and draw one ray per i 

- # TODO: draw the diagonal 

The template defined the window dimensions and the number of rays N = 9, but the loop body and diagonal drawing were left as TODO comments. 

### **Changes made:** 

1. Added the ray-drawing loop: A for loop iterates i from 1 to N. For each i, a parameter t=i/(N+1) is computed. This t linearly interpolates from 0 to 1 (exclusive), distributing N points evenly along the diagonal. Each ray is drawn from the top-left corner (0, H) to the interpolated point (W*t, H*t) on the diagonal. 

2. Added the diagonal line: A single call to self.draw_line(0, 0, W, H, ...) draws the main diagonal from the bottom-left to the top-right. 

### **Solution code:** 

class App(Simple2DApp): 

def draw(self): 

W, H = self.width, self.height N = 9 

for i in range(1, N + 1): t = i / (N + 1) 

self.draw_line(0, H, W * t, H * t, color=(0, 0, 0), width=1) 

self.draw_line(0, 0, W, H, color=(0, 0, 0), width=1) 

**Explanation:** The interpolation formula t=i/(N+1) ensures that the first ray at i=1 starts slightly past the corner and the last ray at i=N ends slightly before the opposite corner, creating an evenlyfanned distribution. The draw_line helper sets the color via glColor3f, sets the line width via glLineWidth, and draws using glBegin(GL_LINES). 

### **Screenshot:** 



**_Figure 2.1_** _Screenshot of exercise 1A_ 

### **2.2 Exercise 1B — Axes + Main Line** 

### **Original code:** 

class App(Simple2DApp): def draw(self): W, H = self.width, self.height cx, cy = W//2, H//2 # TODO: axes 

- # TODO: main line (thicker) 

### **Changes made:** 

1. Added horizontal axis: Draws a gray line from (40, cy) to (W-40, cy) with color=(0.8, 0.8, 0.8) and width=1. The 40-pixel margins prevent the axis from touching the window edges. 

2. Added vertical axis: Same concept, from (cx, 40) to (cx, H-40). 

3. Added main line: Draws a bold black diagonal from (100, 100) to (W-100, H-120) with width=3 for visual emphasis. 

### **Solution code:** 

class App(Simple2DApp): 

def draw(self): 

- W, H = self.width, self.height 

cx, cy = W//2, H//2 

self.draw_line(40, cy, W - 40, cy, color=(0.8, 0.8, 0.8), width=1) 

self.draw_line(cx, 40, cx, H - 40, color=(0.8, 0.8, 0.8), width=1) 

self.draw_line(100, 100, W - 100, H - 120, color=(0, 0, 0), width=3) 

**Explanation:** The axes are drawn using relative coordinates (cx, cy) so they stay centered when the window is resized, thanks to the _reshape callback in the framework. The main line uses a thicker width=3 to visually stand out against the gray axes. 

### **Screenshot:** 



**_Figure 2.2_** _Screenshot of exercise 1B_ 

### **2.3 Exercise 2A — Colored Filled Circles** 

### **Original code:** 

class App(Simple2DApp): def draw(self): cx0, cy0 = 120, 120 dx, dy = 140, 140 r = 50 colors = [ (1.0, 0.2, 0.2), (1.0, 0.6, 0.2), (1.0, 0.9, 0.2), (0.2, 0.8, 0.2), (0.2, 0.6, 1.0), (0.6, 0.2, 1.0), ] # TODO: nested loop, use k to pick colors[k % len(colors)] 

The template provided grid parameters and a color palette but lacked the nested loop. 

**Changes made:** Added a nested loop with a color counter k. For each (row, col) combination: 

- Center computation: cx = cx0 + col * dx, cy = cy0 + row * dy 

- Bounding box conversion: The draw_oval_filled method takes a bounding box (x, y, width, height), not center/radius. So we convert: x = cx - r, y = cy - r, width = height = 2*r. 

- Draw filled circle with colors[k % len(colors)], then draw outline with black. 

### **Solution code:** 

color = 0 for row in range(2): for col in range(3): x = cx0 + col * dx - r y = cy0 + row * dy - r self.draw_oval_filled(x, y, 2 * r, 2 * r, color=colors[color % len(colors)]) self.draw_oval_outline(x, y, 2 * r, 2 * r, color=(0, 0, 0), width=2) color += 1 

**Explanation:** The draw_oval_filled method internally uses GL_TRIANGLE_FAN to fill an ellipse approximation with 128 line segments. The modulo operator color % len(colors) allows the palette to cycle if there are more circles than colors. The outline is drawn on top to create a clean border effect. 

### **Screenshot:** 



**_Figure 2.3_** _Screenshot of exercise 2A_ 

### **2.4 Exercise 2B — Flower of Circles** 

### **Original code:** 

class App(Simple2DApp): def draw(self): W, H = self.width, self.height cx, cy = W*0.5, H*0.5 N = 24 

r = min(W, H)*0.18 

R = r 

- # TODO: loop k in [0..N-1]: compute angle, draw circle 

### **Changes made:** 

1. Circle placement loop: For each k in [0, N-1], the angle th = 2π·k/N places the circle center at (cx + R·cos(th), cy + R·sin(th)). Since r = R, each circle passes through the window center, creating the "flower" pattern. 

2. Boundary circle: A large circle of radius 2r centered at (cx, cy) serves as the outer boundary. 

3. Center dot: A small filled oval at the center marks the origin. 

### **Solution code:** 

for k in range(N): th = 2 * math.pi * k / N x = cx + R * math.cos(th) y = cy + R * math.sin(th) self.draw_oval_outline(x - r, y - r, 2 * r, 2 * r, color=(0, 0, 0), width=2) 

self.draw_oval_outline(cx - 2*r, cy - 2*r, 4*r, 4*r, color=(0, 0, 0), width=2) self.draw_oval_filled(cx - 3, cy - 3, 6, 6, color=(0, 1, 0)) 

**Explanation:** The key insight is that setting r = R (circle radius equals ring radius) ensures every circle passes through the center (cx, cy). This is because the distance from the center to any circle's center is R, and each circle has radius r = R, so the center point lies exactly on each circle's circumference. The 24 overlapping circles create the characteristic petal-like "flower" pattern. 

### **Screenshot:** 



**_Figure 2.4_** _Screenshot of exercise 2B_ 

### **2.5 Exercise 3 — Rectangles & Ellipses** 

### **Original code:** 

class App(Simple2DApp): 

def draw(self): 

# TODO: at least 2 rectangles and 2 ellipses using outline helpers 

pass 

**Changes made:** Replaced pass with four drawing calls using different colors and line widths 

### **Solution code:** 

class App(Simple2DApp): 

def draw(self): 

self.draw_rect_outline(100, 100, 200, 120, color=(0.1, 0.1, 0.8), width=2) self.draw_rect_outline(340, 100, 160, 240, color=(0.8, 0.1, 0.5), width=3) self.draw_oval_outline(80, 280, 200, 120, color=(0.1, 0.6, 0.1), width=2) self.draw_oval_outline(360, 180, 120, 120, color=(0.6, 0, 0.6), width=3) 

**Explanation:** Both draw_rect_outline and draw_oval_outline take bounding box parameters (x, y, width, height). The rectangle helper uses GL_LINE_LOOP with four vertices; the oval helper approximates the ellipse with 128 line segments. By varying the width/height ratio, we get rectangles of different aspect ratios and ellipses vs. circles (when width == height). 

### **Screenshot:** 



**_Figure 2.5_** _Screenshot of exercise 3_ 

### **2.6 Exercise 4A — Star + Caption** 

### **Original code:** 

def star_points(cx, cy, R_outer=120, R_inner=50, start_angle_deg=-90): 

# TODO: compute 5 outer and 5 inner points (alternating ring) 

return [] 

class App(Simple2DApp): 

def draw(self): 

- W, H = self.width, self.height 

- # TODO: call star_points, fill with GL_TRIANGLE_FAN, draw outline, add text 

### **Changes made:** 

1. Implemented star_points function: For each of the 5 points (i = 0..4): 

   - Outer tip: angle = start_angle_deg + 72° × i (360°/5 = 72° spacing), position = (cx + R_outer·cos(angle), cy + R_outer·sin(angle)) 

   - Inner valley: angle shifted by +36° (halfway between outer tips), position = (cx + R_inner·cos(angle), cy + R_inner·sin(angle)) 

   - Points are appended alternating: outer, inner, outer, inner, ... creating a 10-point ring. 

2. Filled star: Uses GL_TRIANGLE_FAN with the center (cx, cy) as the hub vertex and the 10 ring points as the fan. The fan closes by repeating the first ring point. 

3. Outline star: Uses self.draw_polyline(..., loop=True) which renders the 10-point ring as a closed GL_LINE_LOOP. 

4. Captions: self.draw_text(...) renders text using glutBitmapCharacter with the Helvetica 18 font. 

### **Solution code:** 

def star_points(cx, cy, R_outer=120, R_inner=50, start_angle_deg=-90): pts = [] for i in range(5): angle_out = math.radians(start_angle_deg + 72 * i) pts.append((cx + R_outer * math.cos(angle_out), cy + R_outer * math.sin(angle_out))) angle_in = math.radians(start_angle_deg + 72 * i + 36) pts.append((cx + R_inner * math.cos(angle_in), cy + R_inner * math.sin(angle_in))) return pts 

class App(Simple2DApp): def draw(self): W, H = self.width, self.height 

# Filled star 

cx1, cy1 = W * 0.35, H * 0.6 pts1 = star_points(cx1, cy1, R_outer=120, R_inner=50) glColor3f(1.0, 0.85, 0.1) glBegin(GL_TRIANGLE_FAN) glVertex2f(cx1, cy1) for (x, y) in pts1: glVertex2f(x, y) glVertex2f(pts1[0][0], pts1[0][1]) glEnd() self.draw_polyline(pts1, color=(0, 0, 0), width=2, loop=True) self.draw_text(cx1 - 60, cy1 - 160, "This is a star", color=(0, 0, 0)) 

# Outline-only star cx2, cy2 = W * 0.7, H * 0.6 pts2 = star_points(cx2, cy2, R_outer=100, R_inner=42) self.draw_polyline(pts2, color=(0.0, 0.0, 0.8), width=2, loop=True) self.draw_text(cx2 - 60, cy2 - 140, "This is a star", color=(0, 0, 0)) 

**Explanation:** Starting at -90° places the topmost point at 12 o'clock. The GL_TRIANGLE_FAN primitive efficiently fills the star by creating triangles that all share the center vertex, radiating outward through alternating outer and inner points. The 36° offset for inner points places them exactly between adjacent outer tips. 

### **Screenshot:** 



**_Figure 2.6_** _Screenshot of exercise 4A_ 

### **2.7 Exercise 4B — Pentagram (Complete) + Labels** 

### **Original code:** 

def star_points_regular(cx, cy, R): 

- # TODO: compute outer[5] and inner[5] with r = R * sin(18°)/sin(54°) return [], [] 

class App(Simple2DApp): 

def draw(self): 

- # TODO: get points, fill, draw pentagram outline, label 

### **Changes made:** 

1. Inner radius formula: r = R × sin(18°) / sin(54°). This formula derives from the geometry of a regular pentagram — the intersection points of the diagonals of a regular pentagon divide each diagonal in the golden ratio. This yields r ≈ 0.382 × R. 

2. Pentagram outline order: Instead of connecting adjacent outer points (which would draw a regular pentagon), the pentagram connects every 2nd vertex: 0 → 2 → 4 → 1 → 3 → 0. This creates the characteristic five-pointed star with crossing lines. 

3. Vertex labels: Each outer vertex is labeled p1(x,y) through p5(x,y) using draw_text. 

### **Solution code:** 

def star_points_regular(cx, cy, R): r = R * math.sin(math.radians(18)) / math.sin(math.radians(54)) outer, inner = [], [] for i in range(5): a_out = math.radians(-90 + 72 * i) outer.append((cx + R * math.cos(a_out), cy + R * math.sin(a_out))) a_in = math.radians(-90 + 72 * i + 36) inner.append((cx + r * math.cos(a_in), cy + r * math.sin(a_in))) return outer, inner 

class App(Simple2DApp): def draw(self): W, H = self.width, self.height cx, cy = W*0.5, H*0.55 R = min(W, H) * 0.32 outer, inner = star_points_regular(cx, cy, R) # Build alternating ring and fill ring = [] for i in range(5): ring.append(outer[i]) ring.append(inner[i]) glColor3f(1.0, 0.85, 0.1) glBegin(GL_TRIANGLE_FAN) glVertex2f(cx, cy) for (x, y) in ring: glVertex2f(x, y) glVertex2f(ring[0][0], ring[0][1]) glEnd() # Pentagram outline (skip-one connection) order = [0, 2, 4, 1, 3, 0] 

penta_pts = [outer[i] for i in order] self.draw_polyline(penta_pts, color=(0, 0, 0), width=2) 

# Labels 

for i, (x, y) in enumerate(outer): label = f"p{i+1}({int(x)},{int(y)})" 

self.draw_text(x - 30, y + 10, label, color=(1, 0, 0)) 

self.draw_text(cx - 50, cy - R - 40, "This is a star", color=(0, 0, 0)) 

**Explanation:** The difference from Ex 4A is the mathematically derived inner radius and the skipconnection outline. The sin(18°)/sin(54°) formula ensures the inner valleys fall exactly at the intersection points of the pentagram's diagonals, making the star geometrically regular. The outline order [0, 2, 4, 1, 3, 0] draws a continuous path that visits each outer tip while skipping one between each pair, forming the iconic five-pointed star pattern. 

### **Screenshot:** 



<!-- Start of picture text -->
1 8- Pentagram Complete — Oo x<br>p4(297,485) 3(512,485)<br>paz; 582,270)<br>pilgoo,138)<br>This is a star<br><!-- End of picture text -->

**_Figure 2.7_** _Screenshot of exercise 4B_ 

### **2.8 Exercise 5 — Hello 2D Transforms + Filled Ellipses** 

### **Original code:** 

class App(Simple2DApp): 

def draw_ellipse_filled(self, cx, cy, rx, ry, color=(0,0,1,1), segments=120): # TODO: implement triangle-fan filled ellipse 

pass 

def draw(self): 

# TODO: apply Translate -> Scale -> Rotate, draw ellipses pass 

### **Changes made:** 

1. draw_ellipse_filled implementation: Uses GL_TRIANGLE_FAN with glColor4f (4-component color for alpha transparency). The center vertex is placed first, then segments+1 rim vertices are computed parametrically: x = cx + rx·cos(t), y = cy + ry·sin(t) for t ∈ [0, 2π]. 

2. **Transformation stack:** The draw method uses glPushMatrix/glPopMatrix to isolate the transform. The transformation order is: 

   - glTranslatef(300, 200, 0): move to position (300, 200) 

   - glScalef(2.0, 2.0, 1.0): double the size 

   - glRotatef(30.0, 0, 0, 1): rotate 30° around the Z-axis 

3. **Alpha blending:** glEnable(GL_BLEND) with glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) enables semi-transparent fills. The ellipses use alpha = 0.35 for a translucent effect. 

### **Solution code:** 

class App(Simple2DApp): def draw_ellipse_filled(self, cx, cy, rx, ry, color=(0,0,1,1), segments=120): glColor4f(*color) glBegin(GL_TRIANGLE_FAN) glVertex2f(cx, cy) for i in range(segments + 1): t = 2.0 * math.pi * (i / segments) glVertex2f(cx + rx * math.cos(t), cy + ry * math.sin(t)) glEnd() 

def draw(self): glEnable(GL_BLEND) glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) glPushMatrix() 

glTranslatef(300, 200, 0) glScalef(2.0, 2.0, 1.0) glRotatef(30.0, 0, 0, 1) 

self.draw_ellipse_filled(0, 0, 100, 50, color=(0.1, 0.6, 1.0, 0.35)) 

self.draw_ellipse_outline(0, 0, 100, 50, color=(0, 0, 1), width=2) 

self.draw_ellipse_filled(0, 0, 50, 100, color=(1.0, 0.2, 0.6, 0.35)) self.draw_ellipse_outline(0, 0, 50, 100, color=(0.6, 0.0, 0.3), width=2) 

self.draw_text(0, 0, "Hello 2D", color=(0, 0, 0)) glPopMatrix() 

**Explanation:** The two ellipses have swapped radii (rx=100, ry=50) and (rx=50, ry=100), creating a horizontal and vertical ellipse respectively. When overlaid with the 30° rotation and semitransparent fills, the overlapping region shows the blended color, demonstrating both the transformation pipeline and alpha compositing. Drawing at the origin (0, 0) and relying on the matrix stack for positioning is a clean pattern that separates geometry definition from placement. 

### **Screenshot:** 



**_Figure 2.8_** _Screenshot of exercise 5_ 

## **3. Part 2: Homework Exercises** 

### **3.1 Exercise 1 — Background Practice with PyOpenGL** 

### **3.1.1 Task 1: Solid Background Color** 

### **Original code:** 

def _set_up_opengl(self) -> None: 

if self.mode == 1: 

- # TODO(Part 1): Change these numbers to different RGB values 

- pass 

The original had a pass statement where glClearColor should be called. 

### **Solution code:** 

def _set_up_opengl(self) -> None: 

if self.mode == 1: 

glClearColor(0, 0, 1, 1)  # Blue background 

**Changes and explanation:** Replaced pass with glClearColor(0, 0, 1, 1). This sets the clear color to blue (R=0, G=0, B=1, A=1). Every frame, glClear(GL_COLOR_BUFFER_BIT) fills the framebuffer with this color. The four parameters represent RGBA values in the range [0.0, 1.0]. 

### **Screenshot:** 



<!-- Start of picture text -->
_® pygeme window<br><!-- End of picture text -->

**_Figure 3.1.1_** _Screenshot of task 1 homework exercise 1_ 

### **3.1.2 Task 2: Background Image** 

### **Original code:** 

if self.mode == 2: # TODO(Part 2): replace with your image file pass 

and at the bottom: 

myApp = App(mode=1) 

### **Solution code:** 

if self.mode == 2: self.bg_tex = self._load_texture("background.jpg") 

and: 

myApp = App(mode=2) 

### **Changes and explanation:** 

1. Loaded the texture: Replaced pass with self.bg_tex = self._load_texture("background.jpg"). The _load_texture method loads an image using Pygame's pg.image.load, converts it to raw bytes with pg.image.tostring, creates an OpenGL texture object, and uploads the pixel data via glTexImage2D. 

2. Switched to mode 2: Changed the constructor call to App(mode=2) to activate the image background mode. 

3. Flipped texture coordinates: In _draw_background, the texture coordinates were modified from: glTexCoord2f(0, 0); glVertex2f(-1, -1) glTexCoord2f(1, 0); glVertex2f( 1, -1) glTexCoord2f(1, 1); glVertex2f( 1,  1) glTexCoord2f(0, 1); glVertex2f(-1,  1) 

### to: 

glTexCoord2f(0, 1); glVertex2f(-1, -1) glTexCoord2f(1, 1); glVertex2f( 1, -1) glTexCoord2f(1, 0); glVertex2f( 1,  1) glTexCoord2f(0, 0); glVertex2f(-1,  1) 

This swaps the vertical t coordinate, flipping the image vertically to correct for the difference between OpenGL's bottom-up coordinate system and the image's top-down pixel order. 

### **Screenshot:** 



**_Figure 3.1.2_** _Screenshot of task 2 homework exercise 1_ 

### **3.2 Exercise 2 — Introduction to Shaders** 

### **3.2.1 Task 1: Change Vertex Colors** 

### **Original vertex data:** 

vertices = ( 

- -0.5, -0.5, 0.0, 1.0, 0.0, 0.0,   # Red 

- 0.5, -0.5, 0.0, 0.0, 1.0, 0.0,   # Green 

- 0.0,  0.5, 0.0, 0.0, 0.0, 1.0    # Blue 

) 

### **Solution code:** 

vertices = ( 

- -0.5, -0.5, 0.0, 1.0, 1.0, 0.0,   # Yellow 

- 0.5, -0.5, 0.0, 0.0, 1.0, 1.0,   # Cyan 

- 0.0,  0.5, 0.0, 1.0, 1.0, 1.0    # White 

) 

**Explanation:** Changed the RGB color components from (1,0,0), (0,1,0), (0,0,1) (primary colors) to (1,1,0), (0,1,1), (1,1,1) (yellow, cyan, white). The GPU interpolates these colors across the triangle's surface, producing smooth gradients between the vertices. Yellow = Red+Green, Cyan = Green+Blue, White = all channels at maximum. 

### **3.2.2 Task 2: Modify Fragment Shader (Solid Color)** 

### **Original fragment shader:** 

void main() 

{ 

color = vec4(fragmentColor, 1.0); 

} 

### **Solution fragment shader:** 

void main() 

{ 

color = vec4(1.0, 0.0, 0.0, 1.0);   // Always red 

} 

**Explanation:** By hardcoding vec4(1.0, 0.0, 0.0, 1.0), the fragment shader ignores the interpolated fragmentColor variable entirely. Every pixel of the triangle receives the same solid red color, eliminating the gradient effect. This demonstrates that the fragment shader has final authority over pixel color. 

### **3.2.3 Task 3: Scale in Vertex Shader** 

### **Original vertex shader:** 

void main() 

{ 

gl_Position = vec4(vertexPos, 1.0); 

fragmentColor = vertexColor; 

} 

### **Solution vertex shader:** 

void main() 

{ 

gl_Position = vec4(vertexPos.x * 0.5, vertexPos.y, vertexPos.z, 1.0); fragmentColor = vertexColor; 

} 

**Explanation:** Multiplying vertexPos.x by 0.5 scales the triangle horizontally to half its original width. In Normalized Device Coordinates (NDC), positions range from -1 to +1, so x * 0.5 compresses the horizontal extent from [-0.5, 0.5] to [-0.25, 0.25]. The Y coordinate is unchanged, so the triangle becomes narrower but keeps its height — a non-uniform scale. 

### **Screenshot:** 



**_Figure 3.2_** _Screenshot of homework exercise 2_ 

### **3.3 Exercise 3 — Textured Triangle with Shaders** 

### **3.3.1 Task 1: Change Texture** 

### **Original code:** 

self.wood_texture = Material("gfx/wood.jpeg") 

### **Solution code:** 

self.wood_texture = Material("gfx/background.png") 

**Explanation:** Simply changed the file path passed to the Material constructor. The Material class handles loading any image format supported by Pygame (PNG, JPEG, BMP, etc.), converting it to 

RGBA pixel data, and uploading it to an OpenGL texture object. The same triangle geometry now displays a different image. 

### **3.3.2 Task 2: Experiment with Texture Coordinates** 

### **Original texture coordinates:** 

vertices = ( 

-0.5, -0.5, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0,   # s=0, t=1 (bottom-left) 0.5, -0.5, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0,   # s=1, t=1 (bottom-right) 0.0,  0.5, 0.0, 0.0, 0.0, 1.0, 0.5, 0.0     # s=0.5, t=0 (top-center) 

) 

### **Solution code (vertical flip):** 

vertices = ( 

-0.5, -0.5, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0,   # s=0, t=0 0.5, -0.5, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0,   # s=1, t=0 0.0,  0.5, 0.0, 0.0, 0.0, 1.0, 0.5, 1.0     # s=0.5, t=1 

) 

**Explanation:** The t coordinates were swapped: bottom vertices changed from t=1.0 to t=0.0, and the top vertex from t=0.0 to t=1.0. This flips the texture vertically on the triangle. The s coordinate controls horizontal mapping and was left unchanged. Texture coordinates use the range [0, 1] where (0,0) is typically the top-left of the image. 

### **3.3.3 Task 3: Modify Fragment Shader (Blending Modes)** 

### **Original fragment shader:** 

color = vec4(fragmentColor, 1.0) * texture(imageTexture, fragmentTexCoord); 

The original multiplies vertex color by texture color, which tints the texture. 

### **Solution fragment shader (additive blending):** 

color = vec4(fragmentColor, 1.0) + texture(imageTexture, fragmentTexCoord); 

**Explanation:** Changing from multiplication (*) to addition (+) produces additive blending. With multiplication, vertexColor × textureColor, dark vertex areas (near 0) make the texture invisible. With addition, vertexColor + textureColor, the colors are combined additively, producing a brighter result. Values above 1.0 are clamped, so bright areas appear washed out/white. The commentedout alternatives show: 

- texture(...) alone — pure texture, no vertex color influence 

- vec4(fragmentColor, 1.0) alone — pure vertex color gradient, no texture 

### **Screenshot:** 



**_Figure 3.3_** _Screenshot of homework exercise 3_ 

### **4.4 Exercise 4 — Spinning Textured Cube** 

### **4.4.1 Task 1: Change Texture** 

### **Original code:** 

self.wood_texture = Material("gfx/wood.jpeg") 

### **Solution code:** 

self.wood_texture = Material("gfx/cat.png") 

**Explanation:** Replaced the wood texture with the cat image. Since all six faces of the cube share the same texture and use the full [0,1] × [0,1] UV range, the cat image appears on every face. 

### **4.4.2 Task 2: Modify Rotation Speed** 

### **Original code:** 

def update(self) -> None: self.eulers[1] += 0.25     # 0.25° per frame 

### **Solution code:** 

def update(self) -> None: 

self.eulers[1] += 4.0      # 4.0° per frame (16× faster) 

**Explanation:** Changed from 0.25° to 4.0° per frame. At 60 FPS, the original cube completed one full rotation in 360° / 0.25° × (1/60) ≈ 24 seconds. The modified version completes a rotation in 360° / 4.0° × (1/60) = 1.5 seconds, making the spinning visually dramatic. 

### **4.4.3 Task 3: Apply Different Transformations** 

### **Original code:** 

model_transform = pyrr.matrix44.create_identity(dtype=np.float32) 

model_transform = pyrr.matrix44.multiply( m1=model_transform, m2=pyrr.matrix44.create_from_axis_rotation( axis = [0, 1, 0],          # Y-axis rotation only theta = np.radians(self.eulers[1]), dtype = np.float32 ) ) 

### **Solution code (added scaling and changed axis):** 

model_transform = pyrr.matrix44.create_identity(dtype=np.float32) 

# Scale 1.5× larger scale_matrix = np.array([ [1.5, 0,   0,   0], [0,   1.5, 0,   0], [0,   0,   1.5, 0], [0,   0,   0,   1] ], dtype=np.float32) model_transform = pyrr.matrix44.multiply( m1=model_transform, m2=scale_matrix 

) 

model_transform = pyrr.matrix44.multiply( 

m1=model_transform, m2=pyrr.matrix44.create_from_axis_rotation( axis = [1, 1, 0],          # Diagonal axis (X+Y) theta = np.radians(self.eulers[1]), dtype = np.float32 ) 

) 

### **Changes and explanation:** 

1. Added uniform scaling: Inserted a 4×4 scale matrix with factor 1.5 on the diagonal. This makes the cube 50% larger in all three dimensions. The scale is applied first (leftmost in the multiplication chain), so it operates in local space before rotation. 

2. Changed rotation axis from [0, 1, 0] to [1, 1, 0]: The original rotated around the Y-axis only (like a lazy Susan). The new axis is the diagonal of the XY-plane, making the cube tumble in a more complex, visually interesting pattern. The pyrr library normalizes this vector internally before computing the rotation matrix. 

### **4.4.4 Task 4: Experiment with Shaders (Tinting)** 

### **Original fragment shader:** 

void main() 

{ 

color = texture(imageTexture, fragmentTexCoord); 

} 

### **Solution fragment shader:** 

void main() 

{ 

color = texture(imageTexture, fragmentTexCoord) * vec4(1.0, 0.5, 0.5, 1.0); 

- } 

**Explanation:** Multiplying the texture color by vec4(1.0, 0.5, 0.5, 1.0) applies a red tint. The red channel is preserved at full intensity (×1.0), while green and blue channels are halved (×0.5). This shifts the overall color balance toward red/pink. The commented-out alternatives show a blue tint (0.5, 0.5, 1.0) and a warm/sepia tint (1.0, 0.8, 0.6). 

### **Screenshot:** 



**_Figure 4.4.1_** _Screenshot of task 1, 2, 3, 4 homework exercise 4_ 

### **4.4.5 Task 5 (Bonus): Pyramid Mesh** 

**Solution code:** # Pyramid apex = (0.0, 0.7, 0.0) bl = (-0.5, -0.5, 0.5) br = (0.5, -0.5, 0.5) tl = (-0.5, -0.5, -0.5) tr = (0.5, -0.5, -0.5) vertices = ( *apex, 0.5, 0.0, *bl,   0.0, 1.0, *br,   1.0, 1.0, *apex, 0.5, 0.0, *br,   0.0, 1.0, *tr,   1.0, 1.0, *apex, 0.5, 0.0, 

*tr,   0.0, 1.0, *tl,   1.0, 1.0, *apex, 0.5, 0.0, *tl,   0.0, 1.0, *bl,   1.0, 1.0, *bl,   0.0, 0.0, *br,   1.0, 0.0, *tr,   1.0, 1.0, *tr,   1.0, 1.0, *tl,   0.0, 1.0, *bl,   0.0, 0.0, ) 

### **Explaination:** 

- The pyramid is defined by 5 points: one apex at (0, 0.7, 0) and four base corners at y = -0.5. It consists of 6 triangles — 4 side faces (each connecting the apex to two adjacent base corners) and 2 triangles forming the square base. 

- Each vertex carries texture coordinates (s, t): the apex maps to the texture's top-center (0.5, 0), and base corners map to the bottom edge (0, 1) / (1, 1), so the image tapers to a point at the tip. The base maps the full texture flat. 

- Since the data format is identical to the cube (5 floats per vertex: x, y, z, s, t), no shader or VAO changes are needed — only the vertex array is swapped. 

### **Screenshot:** 



<!-- Start of picture text -->
@ ry peve window = .<br><!-- End of picture text -->

**_Figure 4.4.2_** _Screenshot of task 5 homework exercise 4_ 

