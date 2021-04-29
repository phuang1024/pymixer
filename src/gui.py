#
#  Pymixer
#  Video editor with a Python API.
#  Copyright Patrick Huang 2021
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from os import getrandom
import pygame
import vpy
import shared
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from constants import *
from gui_utils import kmod, setup_api
from prefs import Preferences
from preview import Preview
pygame.init()
Tk().withdraw()


class WindowManager:
    def __init__(self):
        self.preview = Preview()

    def draw(self, surface):
        width, height = surface.get_size()
        x_sep = width * 0.8
        y_sep = height * 0.5

        # Preview
        loc = (0, 0)
        size = (x_sep, y_sep)
        self.preview.draw(surface, loc, size)

        # Window separating grid
        pygame.draw.line(surface, GRAY_DARK, (0, y_sep), (x_sep, y_sep), 2)
        pygame.draw.line(surface, GRAY_DARK, (x_sep, 0), (x_sep, height), 2)


def gui():
    setup_api()
    path = ""

    pygame.display.set_caption("Pymixer")
    clock = pygame.time.Clock()
    surface = pygame.display.set_mode((INIT_WIDTH, INIT_HEIGHT), pygame.RESIZABLE)
    surface.fill(BLACK)

    resized = False
    width, height = INIT_WIDTH, INIT_HEIGHT

    wm = WindowManager()
    prefs = Preferences(PREFS_PATH, PREFS_LOCK_PATH)

    while get_run():
        clock.tick(FPS)
        pygame.display.update()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                set_run(False)

            elif event.type == pygame.VIDEORESIZE:
                resized = True
                width, height = event.w, event.h

            elif event.type == pygame.KEYDOWN:
                if kmod(event.key, pygame.K_q, ctrl=True):
                    set_run(False)

                elif kmod(event.key, pygame.K_s, ctrl=True):
                    if vpy.context.scene.is_saved and path:
                        vpy.ops.core.save_scene(path=path)
                        vpy.context.scene.is_saved = True
                    else:
                        path = asksaveasfilename()
                        if path:
                            vpy.ops.core.save_scene(path=path)
                            vpy.context.scene.is_saved = True

                elif kmod(event.key, pygame.K_s, ctrl=True, shift=True):
                    path = asksaveasfilename()
                    if path:
                        vpy.ops.core.save_scene(path=path)
                        vpy.context.scene.is_saved = True

                elif kmod(event.key, pygame.K_o, ctrl=True):
                    path = askopenfilename()
                    if path:
                        vpy.ops.core.open_scene(path=path)
                        vpy.context.scene.is_saved = True

        # Set constants to minimize pygame calls
        shared.mouse_pos = pygame.mouse.get_pos()
        shared.mouse_pressed = pygame.mouse.get_pressed()
        shared.keys_pressed = pygame.key.get_pressed()
        shared.events = events

        if resized:
            surface.fill(BLACK)
        wm.draw(surface)

        resized = False

    set_run(False)
    pygame.quit()
