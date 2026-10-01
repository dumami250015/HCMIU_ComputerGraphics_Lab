import pygame as pg
from OpenGL.GL import *


class App:
    """
        Simple App with two practice modes:
        1) Solid background color
        2) Background image
    """

    def __init__(self, mode=1):
        self.mode = mode   # 1 = solid color, 2 = image background

        self._set_up_pygame()
        self._set_up_timer()
        self._set_up_opengl()

        # Load image only if in mode 2
        if self.mode == 2:
            # TODO(Part 2): replace with your image file 
            # use self._load_texture("background.jpg") for example  
            self.bg_tex = self._load_texture("background.jpg")

    def _set_up_pygame(self) -> None:
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        # Compatibility profile for fixed pipeline
        pg.display.gl_set_attribute(
            pg.GL_CONTEXT_PROFILE_MASK,
            pg.GL_CONTEXT_PROFILE_COMPATIBILITY
        )
        pg.display.set_mode((640, 480), pg.OPENGL | pg.DOUBLEBUF)

    def _set_up_timer(self) -> None:
        self.clock = pg.time.Clock()

    def _set_up_opengl(self) -> None:
        # Mode 1 = solid color
        if self.mode == 1:
            # TODO(Part 1): Change these numbers to different RGB values (between 0 and 1)
            # Example: glClearColor(1, 0, 0, 1) → red background
            glClearColor(0, 0, 1, 1)
        else:
            glClearColor(0, 0, 0, 1)  # hidden behind image
            glEnable(GL_TEXTURE_2D)

    def _load_texture(self, path):
        """Load image as OpenGL texture"""
        surf = pg.image.load(path)
        img = pg.image.tostring(surf, "RGB", True)
        w, h = surf.get_rect().size

        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, w, h, 0,
                     GL_RGB, GL_UNSIGNED_BYTE, img)
        return tex_id

    def _draw_background(self):
        """Draw textured quad covering the screen"""
        # TODO(Part 2, Optional Challenge): Try flipping texture coordinates
        # (swap top and bottom) to see how it affects the image orientation.
        glBindTexture(GL_TEXTURE_2D, self.bg_tex)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 1); glVertex2f(-1, -1)
        glTexCoord2f(1, 1); glVertex2f( 1, -1)
        glTexCoord2f(1, 0); glVertex2f( 1,  1)
        glTexCoord2f(0, 0); glVertex2f(-1,  1)
        glEnd()

    def run(self) -> None:
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

            glClear(GL_COLOR_BUFFER_BIT)

            if self.mode == 2:
                self._draw_background()

            pg.display.flip()
            self.clock.tick(60)

    def quit(self) -> None:
        pg.quit()


if __name__ == "__main__":
    # TODO: Change between modes for practice
    # mode=1 → solid color background
    # mode=2 → image background
    myApp = App(mode=1)
    myApp.run()
    myApp.quit()
