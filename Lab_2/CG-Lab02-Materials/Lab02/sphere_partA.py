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