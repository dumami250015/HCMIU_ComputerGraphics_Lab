# **International University**

School of Computer Science and Engineering



**Computer Graphics Lab 02 – Transformation**

**Semester: 1, Year: 2026 - 2027 Lab Instructor: MSc. Thai Trung Tin**

**Full name:** Võ Trí Khôi **Student ID:** ITCSIU24045 **Group:** G01

## **1. Introduction**

This report documents the completion of Lab 2 for the Computer Graphics course. The lab focuses on **Uniform Data and Transformations** — two fundamental concepts in computer graphics programming. We study how to pass dynamic data (uniforms) from the CPU to the GPU, and how to apply geometric transformations (translation, rotation, scaling) to animate objects in both 2D and 3D scenes.

For each exercise, we present the solution code, describe the key implementation details, and explain the underlying computer graphics concepts, including the mathematics of transformation matrices and the OpenGL rendering pipeline.

## **2. Part 1: In-Class Practices and Exercises**

### **2.1 Exercise 1 – Part D1: Orbiting & Spinning Triangle**

#### **Task Description:**

Implement a program that draws a triangle that **orbits around the origin** and **spins around its own center** simultaneously. The orbit uses trigonometric equations $x = r \cdot \cos(\theta)$, $y = r \cdot \sin(\theta)$, and a rotation matrix handles the self-spin. Both transformations are combined inside the vertex shader.

#### **Solution code:**

```python
import math
import OpenGL.GL as GL

from py3d.core.base import Base
from py3d.core.utils import Utils
from py3d.core.attribute import Attribute
from py3d.core.uniform import Uniform


class Example(Base):
    """Orbiting and spinning triangle"""
    def initialize(self):
        print("Initializing program...")
        vs_code = """
            in vec3 position;
            uniform vec3 translation;
            uniform float rotation;
            void main()
            {
                float c = cos(rotation);
                float s = sin(rotation);
                vec3 rotated = vec3(
                    position.x * c - position.y * s,
                    position.x * s + position.y * c,
                    position.z
                );
                vec3 pos = rotated + translation;
                gl_Position = vec4(pos, 1.0);
            }
        """
        fs_code = """
            uniform vec3 baseColor;
            out vec4 fragColor;
            void main()
            {
                fragColor = vec4(baseColor.r, baseColor.g, baseColor.b, 1.0);
            }
        """
        self.program_ref = Utils.initialize_program(vs_code, fs_code)
        GL.glClearColor(0.0, 0.0, 0.0, 1.0)
        vao_ref = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vao_ref)

        position_data = [[ 0.0,  0.2,  0.0],
                         [ 0.2, -0.2,  0.0],
                         [-0.2, -0.2,  0.0]]
        self.vertex_count = len(position_data)
        position_attribute = Attribute('vec3', position_data)
        position_attribute.associate_variable(self.program_ref, 'position')

        self.translation = Uniform('vec3', [0.0, 0.0, 0.0])
        self.translation.locate_variable(self.program_ref, 'translation')
        self.base_color = Uniform('vec3', [1.0, 1.0, 0.0])
        self.base_color.locate_variable(self.program_ref, 'baseColor')
        self.rotation = Uniform('float', 0.0)
        self.rotation.locate_variable(self.program_ref, 'rotation')

    def update(self):
        self.translation.data[0] = 0.75 * math.cos(self.time)
        self.translation.data[1] = 0.75 * math.sin(self.time)
        self.rotation.data = self.time * 3.0

        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glUseProgram(self.program_ref)
        self.translation.upload_data()
        self.base_color.upload_data()
        self.rotation.upload_data()
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, self.vertex_count)


Example().run()
```

#### **Implementation details and explanation:**

**1. Vertex Shader — Combined Transformation:**

The vertex shader performs two transformations in sequence:

- **Self-rotation (spin):** Each vertex position is rotated around the origin (which is the triangle's local center) using a 2D rotation matrix applied in GLSL:

$$R(\theta) = \begin{bmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{bmatrix}$$

In the shader, this is computed as:
```glsl
vec3 rotated = vec3(
    position.x * c - position.y * s,
    position.x * s + position.y * c,
    position.z
);
```

- **Orbit translation:** After rotation, the rotated position is translated to the orbit position:
```glsl
vec3 pos = rotated + translation;
```

The combined transformation in matrix form (homogeneous coordinates) is:

$$M = T(t_x, t_y) \cdot R(\theta) = \begin{bmatrix} \cos\theta & -\sin\theta & t_x \\ \sin\theta & \cos\theta & t_y \\ 0 & 0 & 1 \end{bmatrix}$$

This order — **rotate first, then translate** — is critical. If we translated first, the triangle would orbit around the origin but not spin around its own center; instead, it would orbit and always face the same direction.

**2. Update Loop — Orbit and Spin Parameters:**

```python
self.translation.data[0] = 0.75 * math.cos(self.time)
self.translation.data[1] = 0.75 * math.sin(self.time)
self.rotation.data = self.time * 3.0
```

- **Orbit:** The translation follows a circular path with radius $r = 0.75$. As `self.time` increases, the angle $\theta = t$ traces a circle: $x = 0.75 \cos(t)$, $y = 0.75 \sin(t)$. The orbit speed is 1 radian per second.

- **Spin:** The rotation angle is $\theta_{spin} = 3t$, meaning the triangle completes one full spin ($2\pi$ radians) every $\frac{2\pi}{3} \approx 2.09$ seconds — about 3× faster than the orbit. This makes the spinning visually distinct from the orbiting.

**3. Uniform Variables:**

Three uniforms are used to communicate CPU-side animation state to the GPU:

| Uniform | Type | Purpose |
|---------|------|---------|
| `translation` | `vec3` | Orbit position $(x, y, 0)$ on the circular path |
| `rotation` | `float` | Self-spin angle in radians |
| `baseColor` | `vec3` | Triangle color (yellow: 1.0, 1.0, 0.0) |

Each frame, the CPU computes the new translation and rotation values, uploads them via `upload_data()`, and the GPU applies them to every vertex in parallel.

#### **Screenshot:**



**_Figure 2.1_** _Screenshot of Exercise 1 – Part D1: The yellow triangle simultaneously orbits in a circular path (r = 0.75) and spins around its own center._

---

### **2.2 Exercise 1 – Part D2: Two Triangles (Linear vs Circular Motion)**

#### **Task Description:**

Implement a program that draws **two triangles simultaneously**: the first moves linearly across the screen and resets when leaving the right side; the second moves in a circular path around the origin. Both triangles should be drawn in different colors.

#### **Solution code:**

```python
import math
import OpenGL.GL as GL

from py3d.core.base import Base
from py3d.core.utils import Utils
from py3d.core.attribute import Attribute
from py3d.core.uniform import Uniform


class Example(Base):
    """Two triangles: linear + circular motion"""
    def initialize(self):
        print("Initializing program...")
        vs_code = """
            in vec3 position;
            uniform vec3 translation;
            void main()
            {
                vec3 pos = position + translation;
                gl_Position = vec4(pos, 1.0);
            }
        """
        fs_code = """
            uniform vec3 baseColor;
            out vec4 fragColor;
            void main()
            {
                fragColor = vec4(baseColor, 1.0);
            }
        """
        self.program_ref = Utils.initialize_program(vs_code, fs_code)
        GL.glClearColor(0.0, 0.0, 0.0, 1.0)

        self.vao1 = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vao1)
        pos1 = [[ 0.0,  0.1,  0.0],
                [ 0.1, -0.1,  0.0],
                [-0.1, -0.1,  0.0]]
        self.vertex_count = len(pos1)
        Attribute('vec3', pos1).associate_variable(self.program_ref, 'position')

        self.vao2 = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vao2)
        pos2 = [[ 0.0,  0.1,  0.0],
                [ 0.1, -0.1,  0.0],
                [-0.1, -0.1,  0.0]]
        Attribute('vec3', pos2).associate_variable(self.program_ref, 'position')

        self.translation = Uniform('vec3', [0.0, 0.0, 0.0])
        self.translation.locate_variable(self.program_ref, 'translation')
        self.base_color = Uniform('vec3', [1.0, 0.0, 0.0])
        self.base_color.locate_variable(self.program_ref, 'baseColor')

    def update(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glUseProgram(self.program_ref)

        t1_x = -1.2 + (self.time * 0.5) % 2.4
        self.translation.data = [t1_x, 0.3, 0.0]
        self.base_color.data = [1.0, 0.0, 0.0]
        self.translation.upload_data()
        self.base_color.upload_data()
        GL.glBindVertexArray(self.vao1)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, self.vertex_count)

        self.translation.data = [0.5 * math.cos(self.time),
                                  0.5 * math.sin(self.time) - 0.3,
                                  0.0]
        self.base_color.data = [0.0, 0.5, 1.0]
        self.translation.upload_data()
        self.base_color.upload_data()
        GL.glBindVertexArray(self.vao2)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, self.vertex_count)


Example().run()
```

#### **Implementation details and explanation:**

**1. Two Separate VAOs (Vertex Array Objects):**

Each triangle has its own VAO (`self.vao1` and `self.vao2`). While both triangles share the same shader program, they have independent vertex data buffers. This is essential because OpenGL requires binding the correct VAO before each `glDrawArrays` call to use the right vertex data.

**2. Drawing Two Objects with One Shader:**

The key technique here is **re-using the same shader program** with different uniform values for each triangle. The draw cycle per frame is:

1. Clear the screen
2. Set Triangle 1's uniforms → bind VAO 1 → draw
3. Set Triangle 2's uniforms → bind VAO 2 → draw

This "set uniforms → draw" pattern is the standard approach for rendering multiple objects with the same shader.

**3. Triangle 1 — Linear Motion:**

```python
t1_x = -1.2 + (self.time * 0.5) % 2.4
```

- The x-position starts at $-1.2$ (off-screen left) and increases at a speed of $0.5$ units per second.
- The modulo `% 2.4` wraps the value back to $0$ after the triangle has traveled $2.4$ units (from $-1.2$ to $+1.2$), creating a seamless loop.
- The y-position is fixed at $0.3$ (upper half of the screen).
- Color: **red** $(1.0, 0.0, 0.0)$.

The wrapping range of $[-1.2, +1.2]$ slightly exceeds the NDC range of $[-1, +1]$, so the triangle appears to smoothly enter from the left edge and exit from the right edge before reappearing.

**4. Triangle 2 — Circular Motion:**

```python
self.translation.data = [0.5 * math.cos(self.time),
                          0.5 * math.sin(self.time) - 0.3,
                          0.0]
```

- The triangle follows a circular path with radius $r = 0.5$ centered at $(0, -0.3)$.
- The $-0.3$ offset in y positions the circular orbit in the lower half of the screen, visually separating it from the linear triangle above.
- Color: **blue** $(0.0, 0.5, 1.0)$.

**5. Vertex Shader — Translation Only:**

Unlike D1, this shader only applies a translation (no rotation):
```glsl
vec3 pos = position + translation;
gl_Position = vec4(pos, 1.0);
```

This is a simple additive translation: $P' = P + T$, which in matrix form is:

$$\begin{bmatrix} x' \\ y' \\ 1 \end{bmatrix} = \begin{bmatrix} 1 & 0 & t_x \\ 0 & 1 & t_y \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} x \\ y \\ 1 \end{bmatrix}$$

#### **Screenshot:**



**_Figure 2.2_** _Screenshot of Exercise 1 – Part D2: Red triangle moves linearly (top), blue triangle orbits in a circle (bottom)._

---

### **2.3 Exercise 1 – Part D3: Linear Motion with Rotation + Circular Motion**

#### **Task Description:**

Implement a program that draws **two triangles with different behaviors**:
- **Triangle A:** moves linearly across the screen and also rotates around its own center while moving. Uses the combined transformation $M = T(t_x, 0) \cdot R(\theta)$.
- **Triangle B:** moves in a circular orbit around the origin (no rotation).

#### **Solution code:**

```python
import math
import OpenGL.GL as GL

from py3d.core.base import Base
from py3d.core.utils import Utils
from py3d.core.attribute import Attribute
from py3d.core.uniform import Uniform


class Example(Base):
    """Triangle A: linear + spin. Triangle B: circular orbit."""
    def initialize(self):
        print("Initializing program...")
        vs_code = """
            in vec3 position;
            uniform vec3 translation;
            uniform float rotation;
            void main()
            {
                float c = cos(rotation);
                float s = sin(rotation);
                vec3 rotated = vec3(
                    position.x * c - position.y * s,
                    position.x * s + position.y * c,
                    position.z
                );
                vec3 pos = rotated + translation;
                gl_Position = vec4(pos, 1.0);
            }
        """
        fs_code = """
            uniform vec3 baseColor;
            out vec4 fragColor;
            void main()
            {
                fragColor = vec4(baseColor, 1.0);
            }
        """
        self.program_ref = Utils.initialize_program(vs_code, fs_code)
        GL.glClearColor(0.0, 0.0, 0.0, 1.0)

        self.vao_a = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vao_a)
        pos = [[0.0, 0.1, 0.0], [0.1, -0.1, 0.0], [-0.1, -0.1, 0.0]]
        self.vertex_count = 3
        Attribute('vec3', pos).associate_variable(self.program_ref, 'position')

        self.vao_b = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vao_b)
        Attribute('vec3', pos).associate_variable(self.program_ref, 'position')

        self.translation = Uniform('vec3', [0.0, 0.0, 0.0])
        self.translation.locate_variable(self.program_ref, 'translation')
        self.base_color = Uniform('vec3', [1.0, 0.0, 0.0])
        self.base_color.locate_variable(self.program_ref, 'baseColor')
        self.rotation = Uniform('float', 0.0)
        self.rotation.locate_variable(self.program_ref, 'rotation')

    def update(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glUseProgram(self.program_ref)

        t_x = -1.2 + (self.time * 0.4) % 2.4
        self.translation.data = [t_x, 0.3, 0.0]
        self.rotation.data = self.time * 2.0
        self.base_color.data = [0.0, 1.0, 0.0]
        self.translation.upload_data()
        self.rotation.upload_data()
        self.base_color.upload_data()
        GL.glBindVertexArray(self.vao_a)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, self.vertex_count)

        self.translation.data = [0.6 * math.cos(self.time),
                                  0.6 * math.sin(self.time) - 0.3,
                                  0.0]
        self.rotation.data = 0.0
        self.base_color.data = [0.0, 1.0, 1.0]
        self.translation.upload_data()
        self.rotation.upload_data()
        self.base_color.upload_data()
        GL.glBindVertexArray(self.vao_b)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, self.vertex_count)


Example().run()
```

#### **Implementation details and explanation:**

**1. Triangle A — Linear Motion + Self-Rotation (Combined Transformation):**

Triangle A demonstrates the combined transformation $M = T(t_x, 0) \cdot R(\theta)$:

```python
t_x = -1.2 + (self.time * 0.4) % 2.4      # linear motion
self.rotation.data = self.time * 2.0         # self-spin at 2 rad/s
```

The transformation pipeline in the vertex shader is:
1. **Rotate** the vertex around the local origin: $P_{rotated} = R(\theta) \cdot P$
2. **Translate** the rotated vertex to the world position: $P_{final} = P_{rotated} + T$

In matrix notation:

$$P' = T(t_x, 0.3) \cdot R(2t) \cdot P = \begin{bmatrix} \cos(2t) & -\sin(2t) & t_x \\ \sin(2t) & \cos(2t) & 0.3 \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} x \\ y \\ 1 \end{bmatrix}$$

The triangle moves at $0.4$ units/second horizontally (slightly slower than D2's $0.5$) and spins at $2$ radians/second. The green color $(0, 1, 0)$ distinguishes it from the other triangle.

**2. Triangle B — Circular Orbit (No Rotation):**

Triangle B only orbits with no self-rotation:

```python
self.rotation.data = 0.0                     # no spin
self.translation.data = [0.6 * math.cos(self.time),
                          0.6 * math.sin(self.time) - 0.3, 0.0]
```

Setting `rotation = 0.0` causes the rotation matrix to become the identity matrix ($\cos(0) = 1$, $\sin(0) = 0$), so only the translation is applied. The orbit radius is $r = 0.6$, centered at $(0, -0.3)$, with a cyan color $(0, 1, 1)$.

**3. Key Difference from D1 and D2:**

This exercise combines elements from both:
- From D1: the rotation uniform and combined rotation + translation in the shader
- From D2: two separate VAOs and the multi-draw technique

The critical insight is that the **same vertex shader** handles both a rotating triangle (Triangle A, rotation ≠ 0) and a non-rotating triangle (Triangle B, rotation = 0) — demonstrating the flexibility of uniform-driven shaders.

#### **Screenshot:**



**_Figure 2.3_** _Screenshot of Exercise 1 – Part D3: Green triangle moves linearly and spins (top), cyan triangle orbits in a circle without spinning (bottom)._

---

### **2.4 Exercise 2 – Parts A, B, C: Spinning Sphere with Keyboard Controls**

#### **Task Description:**

Extend the spinning sphere program to add interactive controls:
- **Part A:** Add keyboard controls for global translations (WASDZX) and local translations (IJKL).
- **Part B:** Add key controls for Y-axis rotation — global (Q/E) and local (U/O).
- **Part C:** Combine auto-spinning with interactive keyboard controls.

#### **Solution code:**

```python
#!/usr/bin/python3
from math import pi
from py3d.core.base import Base
from py3d.core_ext.camera import Camera
from py3d.core_ext.mesh import Mesh
from py3d.core_ext.renderer import Renderer
from py3d.core_ext.scene import Scene
from py3d.geometry.sphere import SphereGeometry
from py3d.material.material import Material


class Example(Base):
    """Spinning sphere with keyboard controls"""
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)
        self.camera.set_position([0, 0, 7])
        geometry = SphereGeometry(radius=2)
        vs_code = """
        uniform mat4 modelMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 projectionMatrix;
        in vec3 vertexPosition;
        out vec3 position;
        void main()
        {
            vec4 pos = vec4(vertexPosition, 1.0);
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * pos;
            position = vertexPosition;
        }
        """
        fs_code = """
        in vec3 position;
        out vec4 fragColor;
        void main()
        {
            vec3 color = mod(position, 1.0);
            fragColor = vec4(color, 1.0);
        }
        """
        material = Material(vs_code, fs_code)
        material.locate_uniforms()
        self.mesh = Mesh(geometry, material)
        self.scene.add(self.mesh)

        self.move_speed = 2.0
        self.turn_speed = 90 * (pi / 180)

    def update(self):
        move_amount = self.move_speed * self.delta_time
        turn_amount = self.turn_speed * self.delta_time

        if self.input.is_key_pressed('w'):
            self.mesh.translate(0,  move_amount, 0, local=False)
        if self.input.is_key_pressed('s'):
            self.mesh.translate(0, -move_amount, 0, local=False)
        if self.input.is_key_pressed('a'):
            self.mesh.translate(-move_amount, 0, 0, local=False)
        if self.input.is_key_pressed('d'):
            self.mesh.translate( move_amount, 0, 0, local=False)
        if self.input.is_key_pressed('z'):
            self.mesh.translate(0, 0,  move_amount, local=False)
        if self.input.is_key_pressed('x'):
            self.mesh.translate(0, 0, -move_amount, local=False)

        if self.input.is_key_pressed('q'):
            self.mesh.rotate_y( turn_amount, local=False)
        if self.input.is_key_pressed('e'):
            self.mesh.rotate_y(-turn_amount, local=False)

        if self.input.is_key_pressed('i'):
            self.mesh.translate(0,  move_amount, 0, local=True)
        if self.input.is_key_pressed('k'):
            self.mesh.translate(0, -move_amount, 0, local=True)
        if self.input.is_key_pressed('j'):
            self.mesh.translate(-move_amount, 0, 0, local=True)
        if self.input.is_key_pressed('l'):
            self.mesh.translate( move_amount, 0, 0, local=True)

        if self.input.is_key_pressed('u'):
            self.mesh.rotate_y( turn_amount, local=True)
        if self.input.is_key_pressed('o'):
            self.mesh.rotate_y(-turn_amount, local=True)

        self.mesh.rotate_y(0.00514)
        self.mesh.rotate_x(0.00337)

        self.renderer.render(self.scene, self.camera)


Example(screen_size=[800, 600]).run()
```

#### **Implementation details and explanation:**

**1. Part A — Global vs Local Translation:**

| Key | Action | Type | Code |
|-----|--------|------|------|
| W / S | Move up / down | Global | `translate(0, ±move, 0, local=False)` |
| A / D | Move left / right | Global | `translate(±move, 0, 0, local=False)` |
| Z / X | Move forward / backward | Global | `translate(0, 0, ±move, local=False)` |
| I / K | Move up / down | Local | `translate(0, ±move, 0, local=True)` |
| J / L | Move left / right | Local | `translate(±move, 0, 0, local=True)` |

**Why global uses $M = T \cdot M$ and local uses $M = M \cdot T$:**

- **Global transformation ($M_{new} = T \cdot M_{old}$):** The translation matrix $T$ is pre-multiplied (applied to the left). Since matrix multiplication is applied right-to-left, $T$ is applied **after** all existing transformations. This means the translation happens in the **world coordinate system**, regardless of the object's current orientation. Pressing W always moves the sphere upward in the world.

- **Local transformation ($M_{new} = M_{old} \cdot T$):** The translation matrix $T$ is post-multiplied (applied to the right). This means $T$ is applied **before** the existing model transformation, operating in the **object's local coordinate system**. If the sphere has been rotated, pressing I moves it "forward" relative to its current orientation.

**2. Part B — Interactive Y-axis Rotation:**

| Key | Action | Type |
|-----|--------|------|
| Q | Rotate Y+ (counterclockwise) | Global |
| E | Rotate Y- (clockwise) | Global |
| U | Rotate Y+ (counterclockwise) | Local |
| O | Rotate Y- (clockwise) | Local |

The Y-axis rotation matrix used:

$$R_y(\theta) = \begin{bmatrix} \cos\theta & 0 & \sin\theta & 0 \\ 0 & 1 & 0 & 0 \\ -\sin\theta & 0 & \cos\theta & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}$$

**Difference between global and local rotation:**
- **Global rotation** rotates the sphere around the **world's Y-axis** (vertical axis at the world origin). If the sphere has been translated away from the origin, global rotation will cause it to orbit around the world Y-axis.
- **Local rotation** rotates the sphere around **its own Y-axis**. The sphere spins in place, regardless of its position in the world. This is equivalent to the object spinning on its own axis.

**3. Part C — Auto-Spin Combined with Controls:**

The auto-spin is applied every frame regardless of user input:
```python
self.mesh.rotate_y(0.00514)
self.mesh.rotate_x(0.00337)
```

These small per-frame rotations accumulate, making the sphere spin continuously around both the X and Y axes. The irrational-looking values ($0.00514$ and $0.00337$) ensure the spin pattern doesn't repeat exactly, creating a visually interesting tumbling effect.

**4. Full Transformation Pipeline:**

The complete pipeline for transforming a vertex from object space to clip space is:

$$gl\_Position = P_{projection} \times V_{view} \times M_{model} \times P_{vertex}$$

Where:
- $P_{vertex}$: the original vertex position in object space
- $M_{model}$: the model matrix (combines all translations, rotations, and scales applied to the mesh)
- $V_{view}$: the view matrix (derived from the camera position and orientation)
- $P_{projection}$: the projection matrix (perspective projection with the camera's aspect ratio)

**5. Frame-Rate Independent Movement:**

```python
move_amount = self.move_speed * self.delta_time
turn_amount = self.turn_speed * self.delta_time
```

By multiplying by `delta_time` (time elapsed since the last frame), the movement speed is consistent regardless of frame rate. At 60 FPS, `delta_time ≈ 0.0167s`, giving `move_amount ≈ 0.033` units per frame. At 30 FPS, `delta_time ≈ 0.033s`, giving `move_amount ≈ 0.067` — twice as much per frame, but at half the frame rate, yielding the same perceived speed.

#### **Screenshot:**



**_Figure 2.4_** _Screenshot of Exercise 2 – Parts A, B, C: Spinning sphere with gradient colors and interactive keyboard controls for both global and local transformations._

---

## **3. Part 2: Homework – Extending the Spinning Sphere (Solar System)**

### **3.1 Question 1 – Spinning Sun**

#### **Task Description:**

Modify the sphere program so that the Sun (radius = 1.0) spins continuously around its Y-axis, using the gradient shader (`mod(position, 1.0)`) so the spinning motion is clearly visible.

#### **Solution code:**

```python
from py3d.core.base import Base
from py3d.core_ext.camera import Camera
from py3d.core_ext.mesh import Mesh
from py3d.core_ext.renderer import Renderer
from py3d.core_ext.scene import Scene
from py3d.geometry.sphere import SphereGeometry
from py3d.material.material import Material


class Example(Base):
    """Solar System"""
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)
        self.camera.set_position([0, 0, 12])

        vs_code = """
        uniform mat4 modelMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 projectionMatrix;
        in vec3 vertexPosition;
        out vec3 position;
        void main()
        {
            vec4 pos = vec4(vertexPosition, 1.0);
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * pos;
            position = vertexPosition;
        }
        """
        fs_code = """
        in vec3 position;
        out vec4 fragColor;
        void main()
        {
            vec3 color = mod(position, 1.0);
            fragColor = vec4(color, 1.0);
        }
        """
        material = Material(vs_code, fs_code)
        material.locate_uniforms()

        sun_geometry = SphereGeometry(radius=1.0)
        self.sun = Mesh(sun_geometry, material)
        self.scene.add(self.sun)

    def update(self):
        self.sun.rotate_y(0.01)

        self.renderer.render(self.scene, self.camera)


Example(screen_size=[800, 600]).run()
```

#### **Implementation details and explanation:**

**1. Sun Creation:**

```python
sun_geometry = SphereGeometry(radius=1.0)
self.sun = Mesh(sun_geometry, material)
self.scene.add(self.sun)
```

A sphere mesh with radius $1.0$ is created using `SphereGeometry`, which generates a UV-sphere with vertices arranged along latitude/longitude lines. The mesh is added to the scene graph.

**2. Continuous Y-axis Rotation:**

```python
def update(self):
    self.sun.rotate_y(0.01)
```

Each frame, the Sun is rotated by $0.01$ radians ($\approx 0.573°$) around its Y-axis. This is a **local rotation** — the Sun spins in place. At 60 FPS, the Sun completes one full rotation ($2\pi$ radians) in approximately $\frac{2\pi}{0.01 \times 60} \approx 10.5$ seconds.

**3. Gradient Shader for Visible Rotation:**

The fragment shader `vec3 color = mod(position, 1.0)` maps vertex positions to colors using modular arithmetic. Since the vertex positions are in **object space** (passed through the `position` varying), the colors are fixed relative to the sphere's surface. As the sphere rotates, the color bands move with it, making the rotation clearly visible. Without this gradient, the sphere would appear stationary since it's a uniform color.

**4. Camera Setup:**

```python
self.camera.set_position([0, 0, 12])
```

The camera is positioned at $z = 12$, looking toward the origin. This provides enough distance to view the entire solar system in later questions.

#### **Screenshot:**



**_Figure 3.1_** _Screenshot of Question 1: The Sun (radius 1.0) spins continuously around its Y-axis with a gradient color pattern._

---

### **3.2 Question 2 – Adding the Earth (Orbit Only)**

#### **Task Description:**

Add a second sphere (radius = 0.5) representing the Earth that **orbits the Sun** at a radius of 3.0 units using cosine and sine functions: $x = R \cdot \cos(\theta)$, $z = R \cdot \sin(\theta)$.

#### **Solution code:**

```python
from py3d.core.base import Base
from py3d.core_ext.camera import Camera
from py3d.core_ext.mesh import Mesh
from py3d.core_ext.renderer import Renderer
from py3d.core_ext.scene import Scene
from py3d.geometry.sphere import SphereGeometry
from py3d.material.material import Material


class Example(Base):
    """Solar System"""
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)
        self.camera.set_position([0, 0, 12])

        vs_code = """
        uniform mat4 modelMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 projectionMatrix;
        in vec3 vertexPosition;
        out vec3 position;
        void main()
        {
            vec4 pos = vec4(vertexPosition, 1.0);
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * pos;
            position = vertexPosition;
        }
        """
        fs_code = """
        in vec3 position;
        out vec4 fragColor;
        void main()
        {
            vec3 color = mod(position, 1.0);
            fragColor = vec4(color, 1.0);
        }
        """
        material = Material(vs_code, fs_code)
        material.locate_uniforms()

        sun_geometry = SphereGeometry(radius=1.0)
        self.sun = Mesh(sun_geometry, material)
        self.scene.add(self.sun)

        earth_geometry = SphereGeometry(radius=0.5)
        earth_material = Material(vs_code, fs_code)
        earth_material.locate_uniforms()
        self.earth = Mesh(earth_geometry, earth_material)
        self.scene.add(self.earth)

        self.earth_orbit_radius = 3.0
        self.earth_orbit_speed = 1.0

    def update(self):
        self.sun.rotate_y(0.01)

        self.renderer.render(self.scene, self.camera)

        import math
        earth_angle = self.time * self.earth_orbit_speed
        earth_x = self.earth_orbit_radius * math.cos(earth_angle)
        earth_z = self.earth_orbit_radius * math.sin(earth_angle)
        self.earth.set_position([earth_x, 0, earth_z])


Example(screen_size=[800, 600]).run()
```

#### **Implementation details and explanation:**

**1. Earth Sphere Creation:**

```python
earth_geometry = SphereGeometry(radius=0.5)
earth_material = Material(vs_code, fs_code)
earth_material.locate_uniforms()
self.earth = Mesh(earth_geometry, earth_material)
self.scene.add(self.earth)
```

The Earth is a separate sphere with radius $0.5$ (half the Sun's size). It requires its **own Material instance** because each mesh needs independent uniform locations. Sharing the same Material object would cause uniform conflicts between meshes.

**2. Circular Orbit Computation:**

```python
earth_angle = self.time * self.earth_orbit_speed    # θ = t × 1.0
earth_x = self.earth_orbit_radius * math.cos(earth_angle)   # x = 3.0 × cos(θ)
earth_z = self.earth_orbit_radius * math.sin(earth_angle)   # z = 3.0 × sin(θ)
self.earth.set_position([earth_x, 0, earth_z])
```

The Earth's position is computed using the parametric circle equations:

$$x_{earth} = R \cdot \cos(\theta), \quad z_{earth} = R \cdot \sin(\theta)$$

where $R = 3.0$ and $\theta = t \times \omega_{orbit}$ with $\omega_{orbit} = 1.0$ rad/s.

Note that the orbit is in the **XZ-plane** (horizontal plane), not the XY-plane. This is because in 3D space with the camera looking down the Z-axis, the XZ-plane appears as a horizontal circle when viewed from above or at an angle — matching how planetary orbits appear.

**3. `set_position` vs `translate`:**

The code uses `set_position` instead of `translate`. This is critical:
- `set_position` **sets an absolute position** each frame, directly updating the translation component of the model matrix.
- `translate` would **accumulate** translations frame-over-frame, causing the Earth to spiral outward.

Since we recompute the exact position from the parametric equation each frame, `set_position` is the correct choice.

**4. What You See:**

When running this program, you see a spinning Sun at the center and a smaller Earth sphere smoothly orbiting around it in a circular path. The Earth does not spin on its own axis yet — it only translates.

#### **Screenshot:**



**_Figure 3.2_** _Screenshot of Question 2: The Sun (center) and Earth (radius 0.5) orbiting at distance R = 3.0._

---

### **3.3 Question 3 – Earth's Self-Spin**

#### **Task Description:**

Extend the Earth so that it also **spins on its own Y-axis** while orbiting. Write the transformation equation combining orbit translation and self-rotation, and explain why both transformations are needed.

#### **Solution code:**

```python
import numpy as np
import math
from py3d.core.base import Base
from py3d.core_ext.camera import Camera
from py3d.core_ext.mesh import Mesh
from py3d.core_ext.renderer import Renderer
from py3d.core_ext.scene import Scene
from py3d.geometry.sphere import SphereGeometry
from py3d.material.material import Material
from py3d.core.matrix import Matrix


class Example(Base):
    """Solar System"""
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)
        self.camera.set_position([0, 0, 12])

        vs_code = """
        uniform mat4 modelMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 projectionMatrix;
        in vec3 vertexPosition;
        out vec3 position;
        void main()
        {
            vec4 pos = vec4(vertexPosition, 1.0);
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * pos;
            position = vertexPosition;
        }
        """
        fs_code = """
        in vec3 position;
        out vec4 fragColor;
        void main()
        {
            vec3 color = mod(position, 1.0);
            fragColor = vec4(color, 1.0);
        }
        """
        material = Material(vs_code, fs_code)
        material.locate_uniforms()

        sun_geometry = SphereGeometry(radius=1.0)
        self.sun = Mesh(sun_geometry, material)
        self.scene.add(self.sun)

        earth_geometry = SphereGeometry(radius=0.5)
        earth_material = Material(vs_code, fs_code)
        earth_material.locate_uniforms()
        self.earth = Mesh(earth_geometry, earth_material)
        self.scene.add(self.earth)

        self.earth_orbit_radius = 3.0
        self.earth_orbit_speed = 1.0

    def update(self):
        self.sun.rotate_y(0.01)

        self.renderer.render(self.scene, self.camera)

        earth_angle = self.time * self.earth_orbit_speed
        earth_x = self.earth_orbit_radius * math.cos(earth_angle)
        earth_z = self.earth_orbit_radius * math.sin(earth_angle)

        earth_spin_angle = self.time * 3.0
        T = Matrix.make_translation(earth_x, 0, earth_z)
        R = Matrix.make_rotation_y(earth_spin_angle)
        self.earth.local_matrix = T @ R


Example(screen_size=[800, 600]).run()
```

#### **Implementation details and explanation:**

**1. Combined Transformation — Translation × Rotation:**

The key change from Q2 is replacing `set_position` with a manually composed model matrix:

```python
earth_spin_angle = self.time * 3.0
T = Matrix.make_translation(earth_x, 0, earth_z)
R = Matrix.make_rotation_y(earth_spin_angle)
self.earth.local_matrix = T @ R
```

The Earth's model matrix is computed as:

$$M_{earth} = T(x_{earth}, 0, z_{earth}) \cdot R_y(\theta_{spin})$$

Where:
- $T$ = translation matrix that moves the Earth to its orbital position
- $R_y$ = rotation matrix that spins the Earth around its Y-axis

**2. Transformation Order (T × R):**

The order $T \cdot R$ is critical. Since matrix transformations are applied right-to-left:

1. **First, $R$ is applied:** The Earth's vertices are rotated around the **local Y-axis** (the Earth spins around its own center).
2. **Then, $T$ is applied:** The rotated Earth is translated to its position on the orbital circle.

If the order were reversed ($R \cdot T$), the Earth would first be translated to its orbital position, then rotated around the **world Y-axis** — this would cause the Earth to orbit around the Sun's Y-axis rather than spinning in place.

**3. Earth's Spin Speed:**

```python
earth_spin_angle = self.time * 3.0
```

The spin speed is $3.0$ rad/s, which is $3\times$ faster than the orbital speed ($1.0$ rad/s). This means the Earth completes 3 full rotations for every one orbit, making the self-spin clearly visible.

**4. Using `local_matrix` Directly:**

Instead of calling `translate()` and `rotate_y()` (which accumulate transformations), we directly set `self.earth.local_matrix = T @ R`. This is a **fresh computation each frame**, avoiding floating-point drift from accumulated matrix multiplications. The `@` operator performs matrix multiplication (Python's `__matmul__`).

**5. Why Both Transformations Are Needed:**

In reality, the Earth simultaneously:
- **Orbits** the Sun (revolution) — modeled by the translation $T$
- **Spins** on its axis (rotation) — modeled by the rotation $R_y$

Without the orbit (no $T$), the Earth would spin in place at the origin, coinciding with the Sun. Without the spin (no $R_y$), the Earth would orbit but always show the same face — like Q2, where the gradient pattern doesn't change. The combination of both creates a realistic simulation where the Earth orbits the Sun while also spinning on its own axis.

#### **Screenshot:**



**_Figure 3.3_** _Screenshot of Question 3: The Earth orbits the Sun and simultaneously spins on its own Y-axis._

---

### **3.4 Question 4 – Adding the Moon**

#### **Task Description:**

Add a third sphere (radius = 0.2) representing the Moon. The Moon should orbit around the **Earth** at a radius of 1.0, with its position computed relative to Earth's position. The Moon should also spin on its own Y-axis.

#### **Solution code:**

```python
import numpy as np
import math
from py3d.core.base import Base
from py3d.core_ext.camera import Camera
from py3d.core_ext.mesh import Mesh
from py3d.core_ext.renderer import Renderer
from py3d.core_ext.scene import Scene
from py3d.geometry.sphere import SphereGeometry
from py3d.material.material import Material
from py3d.core.matrix import Matrix


class Example(Base):
    """Solar System"""
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)
        self.camera.set_position([0, 0, 12])

        vs_code = """
        uniform mat4 modelMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 projectionMatrix;
        in vec3 vertexPosition;
        out vec3 position;
        void main()
        {
            vec4 pos = vec4(vertexPosition, 1.0);
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * pos;
            position = vertexPosition;
        }
        """
        fs_code = """
        in vec3 position;
        out vec4 fragColor;
        void main()
        {
            vec3 color = mod(position, 1.0);
            fragColor = vec4(color, 1.0);
        }
        """
        material = Material(vs_code, fs_code)
        material.locate_uniforms()

        sun_geometry = SphereGeometry(radius=1.0)
        self.sun = Mesh(sun_geometry, material)
        self.scene.add(self.sun)

        earth_geometry = SphereGeometry(radius=0.5)
        earth_material = Material(vs_code, fs_code)
        earth_material.locate_uniforms()
        self.earth = Mesh(earth_geometry, earth_material)
        self.scene.add(self.earth)

        self.earth_orbit_radius = 3.0
        self.earth_orbit_speed = 1.0

        moon_geometry = SphereGeometry(radius=0.2)
        moon_material = Material(vs_code, fs_code)
        moon_material.locate_uniforms()
        self.moon = Mesh(moon_geometry, moon_material)
        self.scene.add(self.moon)

        self.moon_orbit_radius = 1.0
        self.moon_orbit_speed = 3.0

    def update(self):
        self.sun.rotate_y(0.01)

        self.renderer.render(self.scene, self.camera)

        earth_angle = self.time * self.earth_orbit_speed
        earth_x = self.earth_orbit_radius * math.cos(earth_angle)
        earth_z = self.earth_orbit_radius * math.sin(earth_angle)

        earth_spin_angle = self.time * 3.0
        T = Matrix.make_translation(earth_x, 0, earth_z)
        R = Matrix.make_rotation_y(earth_spin_angle)
        self.earth.local_matrix = T @ R

        moon_angle = self.time * self.moon_orbit_speed
        moon_x = earth_x + self.moon_orbit_radius * math.cos(moon_angle)
        moon_z = earth_z + self.moon_orbit_radius * math.sin(moon_angle)

        moon_spin_angle = self.time * 5.0
        T_moon = Matrix.make_translation(moon_x, 0, moon_z)
        R_moon = Matrix.make_rotation_y(moon_spin_angle)
        self.moon.local_matrix = T_moon @ R_moon


Example(screen_size=[800, 600]).run()
```

#### **Implementation details and explanation:**

**1. Moon Creation:**

```python
moon_geometry = SphereGeometry(radius=0.2)
moon_material = Material(vs_code, fs_code)
moon_material.locate_uniforms()
self.moon = Mesh(moon_geometry, moon_material)
self.scene.add(self.moon)

self.moon_orbit_radius = 1.0
self.moon_orbit_speed = 3.0
```

The Moon is the smallest sphere ($r = 0.2$), orbiting at radius $1.0$ around the Earth with a speed of $3.0$ rad/s — 3× faster than Earth's orbital speed, creating a visually interesting nested orbit effect.

**2. Moon's Orbit — Relative to Earth:**

```python
moon_angle = self.time * self.moon_orbit_speed
moon_x = earth_x + self.moon_orbit_radius * math.cos(moon_angle)
moon_z = earth_z + self.moon_orbit_radius * math.sin(moon_angle)
```

The Moon's position is computed **relative to the Earth's current position**:

$$x_{moon} = x_{earth} + r_{moon} \cdot \cos(\phi)$$
$$z_{moon} = z_{earth} + r_{moon} \cdot \sin(\phi)$$

Where:
- $(x_{earth}, z_{earth})$: Earth's position from the orbit computation in Q3
- $r_{moon} = 1.0$: Moon's orbit radius around Earth
- $\phi = t \times \omega_{moon}$ with $\omega_{moon} = 3.0$ rad/s

This creates a **compound circular motion** — the Moon traces an epicycloid path in world space (a circle around a moving circle).

**3. Moon's Combined Transformation:**

```python
moon_spin_angle = self.time * 5.0
T_moon = Matrix.make_translation(moon_x, 0, moon_z)
R_moon = Matrix.make_rotation_y(moon_spin_angle)
self.moon.local_matrix = T_moon @ R_moon
```

The Moon's model matrix follows the same $T \cdot R$ pattern as the Earth:

$$M_{moon} = T(x_{moon}, 0, z_{moon}) \cdot R_y(\theta_{moon\_spin})$$

The Moon's self-spin speed is $5.0$ rad/s — the fastest in the system — making its gradient pattern change rapidly.

**4. Complete Solar System Hierarchy:**

The final simulation contains three celestial bodies with these parameters:

| Body | Radius | Orbit Radius | Orbit Speed | Spin Speed | Orbits Around |
|------|--------|-------------|-------------|------------|---------------|
| Sun | 1.0 | — | — | 0.01 rad/frame | — (center) |
| Earth | 0.5 | 3.0 | 1.0 rad/s | 3.0 rad/s | Sun |
| Moon | 0.2 | 1.0 | 3.0 rad/s | 5.0 rad/s | Earth |

**5. Transformation Hierarchy:**

The full transformation pipeline for each body's vertex:

$$gl\_Position = P_{proj} \times V_{view} \times M_{model} \times P_{vertex}$$

Where $M_{model}$ for each body is:

- **Sun:** $M_{sun}$ = accumulated rotations from `rotate_y(0.01)` each frame
- **Earth:** $M_{earth} = T(x_e, 0, z_e) \cdot R_y(3t)$
- **Moon:** $M_{moon} = T(x_m, 0, z_m) \cdot R_y(5t)$

The Moon's world position depends on Earth's position, creating a hierarchical transformation chain typical of scene graphs in computer graphics.

**6. Visual Result:**

When running the program, you see:
- A **spinning Sun** at the center with the gradient color pattern rotating
- A **spinning Earth** orbiting the Sun in a circle (radius 3.0), with its own gradient pattern rotating faster
- A **spinning Moon** orbiting the Earth in a smaller circle (radius 1.0), with the fastest gradient pattern rotation

The Moon traces a complex path in world space — it follows a circular orbit around the Earth, which itself is orbiting the Sun. This creates an epicycloid trajectory that demonstrates the power of hierarchical transformations in computer graphics.

#### **Screenshot:**



**_Figure 3.4_** _Screenshot of Question 4: Complete solar system with spinning Sun (center), spinning Earth orbiting the Sun, and spinning Moon orbiting the Earth._
