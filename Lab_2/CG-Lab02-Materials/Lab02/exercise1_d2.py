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