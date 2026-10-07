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