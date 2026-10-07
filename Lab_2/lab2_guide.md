# Lab 2 — Step-by-Step Guide
## Computer Graphics: Transformations & Animation

---

## Overview

Lab 2 has **two main exercises**, each with an in-class part and a homework part:

| Exercise | Topic | In-Class | Homework |
|---|---|---|---|
| **Exercise 1** | Animation & Basic Transforms | Parts A–C (theory) + Part D (3 programs) | — |
| **Exercise 2** | Matrix Algebra & 3D Transforms | Study 3 given programs | Extend `sphere.py` into a Solar System |

### Given Source Files

| File | Purpose |
|---|---|
| `animation-1.py` | Triangle moving linearly (translating right, wrapping) |
| `animation-2.py` | Triangle moving in a circle (cos/sin) |
| `key-control.py` | Arrow-key controlled triangle |
| `global-and-local-transformations.py` | Demo of global vs local transforms |
| `sphere.py` | 3D spinning sphere with gradient shader |
| `py3d/` | Framework library (do NOT modify) |

---

## Exercise 1: Introduction to Transformations

### Part A — Theory (Written Answers)

These are written questions. Here are the answers:

**Q: Write the general form of 2D translation in matrix form (homogeneous coordinates).**

$$T = \begin{bmatrix} 1 & 0 & t_x \\ 0 & 1 & t_y \\ 0 & 0 & 1 \end{bmatrix}$$

Multiplying by a point $(x, y, 1)^T$:

$$\begin{bmatrix} 1 & 0 & t_x \\ 0 & 1 & t_y \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} x \\ y \\ 1 \end{bmatrix} = \begin{bmatrix} x + t_x \\ y + t_y \\ 1 \end{bmatrix}$$

**Q: Why do we need the extra '1' in homogeneous coordinates?**

Without the extra `1`, translation cannot be expressed as a matrix multiplication — only rotation and scaling can. By adding a third coordinate (always 1), we embed 2D space into 3D homogeneous space, where translation becomes a linear operation expressible as matrix multiplication.

### Part B — Theory: Translation in `animation-1.py`

Study `animation-1.py`. The triangle starts at `translation = [-0.5, 0, 0]` and moves right by `Δx = 0.03` per frame.

**Translation matrix per frame:**

$$T = \begin{bmatrix} 1 & 0 & 0.03 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{bmatrix}$$

**Example: vertex (0.0, 0.2, 1) after 3 frames:**
- Frame 0: position = (0.0 + (-0.5), 0.2, 1) = (-0.5, 0.2, 1)
- Frame 1: translation.x = -0.47 → (-0.47, 0.2, 1)
- Frame 2: translation.x = -0.44 → (-0.44, 0.2, 1)
- Frame 3: translation.x = -0.41 → (-0.41, 0.2, 1)

**Q: Why reset when x > 1.2?**

OpenGL's clip space ranges from -1 to +1. The triangle has width 0.4 (vertices at ±0.2), so when translation.x > 1.2, the entire triangle has passed beyond the right edge. Resetting to -1.2 makes it reappear from the left edge.

### Part C — Theory: Circular Motion in `animation-2.py`

Study `animation-2.py`. The triangle moves in a circle:
```python
self.translation.data[0] = 0.75 * math.cos(self.time)
self.translation.data[1] = 0.75 * math.sin(self.time)
```

**Derivation:** A point on a circle of radius `r` at angle `θ` is `(r·cos(θ), r·sin(θ))`. As `θ = time` increases, the point traces a circle.

**At specific times:**
- `t = 0`: (0.75·cos(0), 0.75·sin(0)) = **(0.75, 0)** → right side
- `t = π/2`: (0.75·cos(π/2), 0.75·sin(π/2)) = **(0, 0.75)** → top
- `t = π`: (0.75·cos(π), 0.75·sin(π)) = **(-0.75, 0)** → left side

---

### Part D — Implementation (3 Programs to Write)

#### D1: Orbiting & Spinning Triangle

**Goal:** One triangle that orbits around the origin AND spins around its own center simultaneously.

**Step-by-step:**

1. **Create a new file** `exercise1_d1.py` in the `Lab02/` folder.

2. **Start from `animation-2.py`** as your base (it already has circular motion).

3. **Add a rotation matrix in the vertex shader.** The key idea: combine translation (orbit) with rotation (spin) in the shader:

```python
#!/usr/bin/python3
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
                // Step 1: Rotate the vertex around its own center (spin)
                float c = cos(rotation);
                float s = sin(rotation);
                vec3 rotated = vec3(
                    position.x * c - position.y * s,
                    position.x * s + position.y * c,
                    position.z
                );
                // Step 2: Translate the rotated vertex (orbit)
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
        # Orbit: move in a circle
        self.translation.data[0] = 0.75 * math.cos(self.time)
        self.translation.data[1] = 0.75 * math.sin(self.time)
        # Spin: rotate around own center (faster than orbit)
        self.rotation.data = self.time * 3.0

        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glUseProgram(self.program_ref)
        self.translation.upload_data()
        self.base_color.upload_data()
        self.rotation.upload_data()
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, self.vertex_count)


Example().run()
```

**How it works:**
- The **vertex shader** first applies a 2D rotation matrix to each vertex (spinning it in place), then adds the translation (moving the rotated triangle along a circular orbit).
- The transformation order in the shader is: **Rotate first, then Translate** — this is `M = T × R`, which spins around the object's own center, not the world origin.

---

#### D2: Two Triangles (Linear vs Circular)

**Goal:** Draw two triangles simultaneously — one moves linearly, the other moves in a circle. Different colors.

**Step-by-step:**

1. **Create `exercise1_d2.py`**.

2. **Key insight:** You need two separate VAOs (one per triangle) and two sets of uniforms. Draw each triangle in the update loop.

```python
#!/usr/bin/python3
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

        # --- Triangle 1 (linear) ---
        self.vao1 = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vao1)
        pos1 = [[ 0.0,  0.1,  0.0],
                [ 0.1, -0.1,  0.0],
                [-0.1, -0.1,  0.0]]
        self.vertex_count = len(pos1)
        Attribute('vec3', pos1).associate_variable(self.program_ref, 'position')

        # --- Triangle 2 (circular) ---
        self.vao2 = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vao2)
        pos2 = [[ 0.0,  0.1,  0.0],
                [ 0.1, -0.1,  0.0],
                [-0.1, -0.1,  0.0]]
        Attribute('vec3', pos2).associate_variable(self.program_ref, 'position')

        # Uniforms (shared, we update before each draw)
        self.translation = Uniform('vec3', [0.0, 0.0, 0.0])
        self.translation.locate_variable(self.program_ref, 'translation')
        self.base_color = Uniform('vec3', [1.0, 0.0, 0.0])
        self.base_color.locate_variable(self.program_ref, 'baseColor')

    def update(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glUseProgram(self.program_ref)

        # --- Draw Triangle 1: Linear motion (red) ---
        t1_x = -1.2 + (self.time * 0.5) % 2.4  # wraps from -1.2 to 1.2
        self.translation.data = [t1_x, 0.3, 0.0]
        self.base_color.data = [1.0, 0.0, 0.0]
        self.translation.upload_data()
        self.base_color.upload_data()
        GL.glBindVertexArray(self.vao1)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, self.vertex_count)

        # --- Draw Triangle 2: Circular motion (blue) ---
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

**How it works:**
- Two VAOs are created with separate vertex data.
- In `update()`, we clear the screen once, then draw each triangle with different uniforms (different translation + different color).
- Triangle 1 uses modular arithmetic for wrap-around; Triangle 2 uses cos/sin.

---

#### D3: Linear+Rotation + Circular

**Goal:** Triangle A moves linearly AND rotates. Triangle B moves in a circle. The combined transform for A is `M = T(tx, 0) × R(θ)`.

```python
#!/usr/bin/python3
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

        # Triangle A
        self.vao_a = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vao_a)
        pos = [[0.0, 0.1, 0.0], [0.1, -0.1, 0.0], [-0.1, -0.1, 0.0]]
        self.vertex_count = 3
        Attribute('vec3', pos).associate_variable(self.program_ref, 'position')

        # Triangle B
        self.vao_b = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vao_b)
        Attribute('vec3', pos).associate_variable(self.program_ref, 'position')

        # Uniforms
        self.translation = Uniform('vec3', [0.0, 0.0, 0.0])
        self.translation.locate_variable(self.program_ref, 'translation')
        self.base_color = Uniform('vec3', [1.0, 0.0, 0.0])
        self.base_color.locate_variable(self.program_ref, 'baseColor')
        self.rotation = Uniform('float', 0.0)
        self.rotation.locate_variable(self.program_ref, 'rotation')

    def update(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glUseProgram(self.program_ref)

        # --- Triangle A: Linear + Rotation (green) ---
        t_x = -1.2 + (self.time * 0.4) % 2.4
        self.translation.data = [t_x, 0.3, 0.0]
        self.rotation.data = self.time * 2.0  # spinning
        self.base_color.data = [0.0, 1.0, 0.0]
        self.translation.upload_data()
        self.rotation.upload_data()
        self.base_color.upload_data()
        GL.glBindVertexArray(self.vao_a)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, self.vertex_count)

        # --- Triangle B: Circular orbit (cyan, no spin) ---
        self.translation.data = [0.6 * math.cos(self.time),
                                  0.6 * math.sin(self.time) - 0.3,
                                  0.0]
        self.rotation.data = 0.0  # no spin
        self.base_color.data = [0.0, 1.0, 1.0]
        self.translation.upload_data()
        self.rotation.upload_data()
        self.base_color.upload_data()
        GL.glBindVertexArray(self.vao_b)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, self.vertex_count)


Example().run()
```

---

## Exercise 2: Matrix Algebra and Transformations

### Study Phase (In-Class)

First, **run and study** the three given programs to understand how the framework works:

1. **`key-control.py`** — Arrow keys move a triangle via a `translation` uniform. Note `self.speed * self.delta_time` for frame-rate independence.

2. **`global-and-local-transformations.py`** — The crucial program. It shows:
   - **Global transform** (`WASDZXQE`): `M = T × M` (pre-multiply) — moves relative to **world axes**
   - **Local transform** (`IJKLUO`): `M = M × T` (post-multiply) — moves relative to **object's own axes**

3. **`sphere.py`** — 3D sphere rendered with the `py3d` framework (Camera, Scene, Renderer, Mesh). The sphere auto-spins via `self.mesh.rotate_y()` and `self.mesh.rotate_x()`.

### Part A — Adding Keyboard Controls to Sphere

**Goal:** Add WASD+ZX (global) and IJKL (local) movement to `sphere.py`.

**Step-by-step:**

1. Copy `sphere.py` to `sphere_interactive.py`.

2. Add keyboard handling in `update()`. The `Object3D` class (which `Mesh` inherits from) already has `translate()`, `rotate_y()`, etc. with a `local` parameter!

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
        self.turn_speed = 90 * (pi / 180)  # radians per second

    def update(self):
        move_amount = self.move_speed * self.delta_time
        turn_amount = self.turn_speed * self.delta_time

        # === GLOBAL translations (WASDZX) ===
        # M = T * M  (pre-multiply → world axes)
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

        # === GLOBAL rotations (QE) ===
        if self.input.is_key_pressed('q'):
            self.mesh.rotate_y( turn_amount, local=False)
        if self.input.is_key_pressed('e'):
            self.mesh.rotate_y(-turn_amount, local=False)

        # === LOCAL translations (IJKL) ===
        # M = M * T  (post-multiply → object's own axes)
        if self.input.is_key_pressed('i'):
            self.mesh.translate(0,  move_amount, 0, local=True)
        if self.input.is_key_pressed('k'):
            self.mesh.translate(0, -move_amount, 0, local=True)
        if self.input.is_key_pressed('j'):
            self.mesh.translate(-move_amount, 0, 0, local=True)
        if self.input.is_key_pressed('l'):
            self.mesh.translate( move_amount, 0, 0, local=True)

        # === LOCAL rotations (UO) ===
        if self.input.is_key_pressed('u'):
            self.mesh.rotate_y( turn_amount, local=True)
        if self.input.is_key_pressed('o'):
            self.mesh.rotate_y(-turn_amount, local=True)

        # === Auto-spin (Part C) ===
        self.mesh.rotate_y(0.00514)
        self.mesh.rotate_x(0.00337)

        # Render
        self.renderer.render(self.scene, self.camera)


Example(screen_size=[800, 600]).run()
```

**Why global = `T × M` and local = `M × T`?**
- **Global (`local=False`):** The transform `T` is applied in world space — it's pre-multiplied, so it happens *after* the existing model transform. The object moves along world axes regardless of its current orientation.
- **Local (`local=True`):** The transform `T` is post-multiplied, so it happens *before* the existing model transform in the pipeline. The object moves along its own rotated axes.

---

## Part 2 Homework: Solar System

This is the big homework assignment. You'll build it step-by-step.

### Question 1 — Spinning Sun

**Goal:** A sphere (radius=1.0) spinning around its Y-axis.

This is essentially the given `sphere.py` with `radius=1.0`:

```python
#!/usr/bin/python3
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
        self.camera.set_position([0, 0, 12])  # farther back to see orbit

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

        # --- SUN (radius=1.0, at origin) ---
        sun_geometry = SphereGeometry(radius=1.0)
        self.sun = Mesh(sun_geometry, material)
        self.scene.add(self.sun)

    def update(self):
        # Sun spins around Y-axis
        self.sun.rotate_y(0.01)

        self.renderer.render(self.scene, self.camera)


Example(screen_size=[800, 600]).run()
```

### Question 2 — Adding the Earth (Orbit Only)

**Goal:** Add a second sphere (radius=0.5) orbiting the Sun at radius 3.0.

**Key formula:** `x = R·cos(θ)`, `z = R·sin(θ)` where `θ` increases over time.

Add to `initialize()`:
```python
        # --- EARTH (radius=0.5, orbits Sun at R=3.0) ---
        earth_geometry = SphereGeometry(radius=0.5)
        # Must create a NEW Material instance for Earth
        earth_material = Material(vs_code, fs_code)
        earth_material.locate_uniforms()
        self.earth = Mesh(earth_geometry, earth_material)
        self.scene.add(self.earth)

        self.earth_orbit_radius = 3.0
        self.earth_orbit_speed = 1.0  # radians per second
```

Add to `update()`:
```python
        # Earth orbits the Sun
        import math
        earth_angle = self.time * self.earth_orbit_speed
        earth_x = self.earth_orbit_radius * math.cos(earth_angle)
        earth_z = self.earth_orbit_radius * math.sin(earth_angle)
        self.earth.set_position([earth_x, 0, earth_z])
```

> **Important:** `set_position()` overwrites the translation part of the model matrix. We'll add self-spin in Question 3.

### Question 3 — Earth's Self-Spin

**Goal:** Earth spins on its own Y-axis WHILE orbiting.

**Problem:** `set_position()` resets the rotation! We need to **build the model matrix manually**.

**Solution:** Replace the Earth update with a combined transformation:

```python
        import numpy as np
        from py3d.core.matrix import Matrix

        # Earth: orbit + self-spin
        earth_angle = self.time * self.earth_orbit_speed
        earth_x = self.earth_orbit_radius * math.cos(earth_angle)
        earth_z = self.earth_orbit_radius * math.sin(earth_angle)

        # Build Earth's model matrix: Translate × Rotate
        # First rotate (spin), then translate (orbit position)
        earth_spin_angle = self.time * 3.0  # spins faster than orbit
        T = Matrix.make_translation(earth_x, 0, earth_z)
        R = Matrix.make_rotation_y(earth_spin_angle)
        self.earth.local_matrix = T @ R
```

**Transformation equation:**
$$M_{earth} = T_{orbit}(R\cos\theta, 0, R\sin\theta) \times R_{spin}(\phi)$$

This first rotates the Earth around its own Y-axis (spin), then translates it to its orbital position. The order matters: `T × R` means "spin first, then place" — so the Earth spins in place at its orbit location.

### Question 4 — Adding the Moon

**Goal:** A third sphere (radius=0.2) orbiting the Earth at radius 1.0, also spinning.

Add to `initialize()`:
```python
        # --- MOON (radius=0.2, orbits Earth at R=1.0) ---
        moon_geometry = SphereGeometry(radius=0.2)
        moon_material = Material(vs_code, fs_code)
        moon_material.locate_uniforms()
        self.moon = Mesh(moon_geometry, moon_material)
        self.scene.add(self.moon)

        self.moon_orbit_radius = 1.0
        self.moon_orbit_speed = 3.0  # orbits Earth faster
```

Add to `update()`:
```python
        # Moon: orbits Earth (which is already orbiting Sun)
        moon_angle = self.time * self.moon_orbit_speed
        moon_x = earth_x + self.moon_orbit_radius * math.cos(moon_angle)
        moon_z = earth_z + self.moon_orbit_radius * math.sin(moon_angle)

        moon_spin_angle = self.time * 5.0
        T_moon = Matrix.make_translation(moon_x, 0, moon_z)
        R_moon = Matrix.make_rotation_y(moon_spin_angle)
        self.moon.local_matrix = T_moon @ R_moon
```

**Key insight:** The Moon's position is **relative to Earth's position**: `x_moon = x_earth + R·cos(θ)`. This creates a hierarchical transformation where the Moon follows the Earth as it orbits the Sun.

---

### Complete Solar System Code

Here's the **final combined program** for all 4 homework questions:

```python
#!/usr/bin/python3
import math
from py3d.core.base import Base
from py3d.core.matrix import Matrix
from py3d.core_ext.camera import Camera
from py3d.core_ext.mesh import Mesh
from py3d.core_ext.renderer import Renderer
from py3d.core_ext.scene import Scene
from py3d.geometry.sphere import SphereGeometry
from py3d.material.material import Material


class SolarSystem(Base):
    """Solar System: Sun + Earth + Moon"""
    def initialize(self):
        print("Initializing Solar System...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)
        self.camera.set_position([0, 3, 12])

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

        # --- SUN ---
        sun_mat = Material(vs_code, fs_code)
        sun_mat.locate_uniforms()
        self.sun = Mesh(SphereGeometry(radius=1.0), sun_mat)
        self.scene.add(self.sun)

        # --- EARTH ---
        earth_mat = Material(vs_code, fs_code)
        earth_mat.locate_uniforms()
        self.earth = Mesh(SphereGeometry(radius=0.5), earth_mat)
        self.scene.add(self.earth)

        # --- MOON ---
        moon_mat = Material(vs_code, fs_code)
        moon_mat.locate_uniforms()
        self.moon = Mesh(SphereGeometry(radius=0.2), moon_mat)
        self.scene.add(self.moon)

        # Orbit parameters
        self.earth_orbit_R = 3.0
        self.earth_orbit_speed = 1.0
        self.moon_orbit_R = 1.0
        self.moon_orbit_speed = 3.0

    def update(self):
        # === SUN: spins in place ===
        self.sun.rotate_y(0.01)

        # === EARTH: orbit + self-spin ===
        earth_angle = self.time * self.earth_orbit_speed
        ex = self.earth_orbit_R * math.cos(earth_angle)
        ez = self.earth_orbit_R * math.sin(earth_angle)
        earth_spin = self.time * 3.0
        T_earth = Matrix.make_translation(ex, 0, ez)
        R_earth = Matrix.make_rotation_y(earth_spin)
        self.earth.local_matrix = T_earth @ R_earth

        # === MOON: orbits Earth + self-spin ===
        moon_angle = self.time * self.moon_orbit_speed
        mx = ex + self.moon_orbit_R * math.cos(moon_angle)
        mz = ez + self.moon_orbit_R * math.sin(moon_angle)
        moon_spin = self.time * 5.0
        T_moon = Matrix.make_translation(mx, 0, mz)
        R_moon = Matrix.make_rotation_y(moon_spin)
        self.moon.local_matrix = T_moon @ R_moon

        self.renderer.render(self.scene, self.camera)


SolarSystem(screen_size=[800, 600]).run()
```

---

## Summary: What to Submit

| Task | File to Create |
|---|---|
| Ex1 Part D1 | `exercise1_d1.py` — Orbiting + spinning triangle |
| Ex1 Part D2 | `exercise1_d2.py` — Two triangles (linear + circular) |
| Ex1 Part D3 | `exercise1_d3.py` — Linear+rotation + circular |
| Ex2 Parts A–C | `sphere_interactive.py` — Sphere with keyboard controls + auto-spin |
| Homework Q1–Q4 | `solar_system.py` — Sun, Earth, Moon simulation |

### Key Concepts to Remember

1. **Homogeneous coordinates** — The extra `1` enables translation as matrix multiplication
2. **Global vs Local transforms** — Pre-multiply (`T × M`) = world space, Post-multiply (`M × T`) = object space
3. **Circular motion** — `x = R·cos(θ)`, `z = R·sin(θ)` traces a circle in the XZ plane
4. **Combined transforms** — `M = T × R` means "rotate first, then translate" (read right-to-left)
5. **Full vertex pipeline** — `gl_Position = Projection × View × Model × vertex`
