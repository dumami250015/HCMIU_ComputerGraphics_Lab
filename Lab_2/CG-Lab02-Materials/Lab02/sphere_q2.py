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
