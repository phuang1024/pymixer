#
#  Video Editor
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

import sys
import os
from constants import *
sys.path.insert(0, MODULE_PATH)
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import pygame
import vpy
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from gui_utils import kmod
from register import register
pygame.init()
Tk().withdraw()


def main():
    register(ADDON_PATHS)

    scene = vpy.types.Scene()
    path = ""

    pygame.display.set_caption("Video Editor")
    clock = pygame.time.Clock()
    surface = pygame.display.set_mode((INIT_WIDTH, INIT_HEIGHT), pygame.RESIZABLE)
    surface.fill(BLACK)

    resized = False
    width, height = INIT_WIDTH, INIT_HEIGHT

    while True:
        clock.tick(FPS)
        pygame.display.update()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            elif event.type == pygame.VIDEORESIZE:
                resized = True
                width, height = event.w, event.h

            elif event.type == pygame.KEYDOWN:
                if kmod(event.key, pygame.K_q, ctrl=True):
                    pygame.quit()
                    return

                elif kmod(event.key, pygame.K_s, ctrl=True):
                    if scene.is_saved and path:
                        vpy.ops.core.save_scene(scene, path=path)
                        scene.is_saved = True
                    else:
                        path = asksaveasfilename()
                        if path:
                            vpy.ops.core.save_scene(scene, path=path)
                            scene.is_saved = True

                elif kmod(event.key, pygame.K_s, ctrl=True, shift=True):
                    path = asksaveasfilename()
                    if path:
                        vpy.ops.core.save_scene(scene, path=path)
                        scene.is_saved = True

                elif kmod(event.key, pygame.K_o, ctrl=True):
                    path = askopenfilename()
                    if path:
                        scene = vpy.ops.core.open_scene(path=path)
                        scene.is_saved = True

        resized = False


main()
