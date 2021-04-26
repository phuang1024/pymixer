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

import pygame
import vpy
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from constants import *
from utils import *
pygame.init()
Tk().withdraw()


def main():
    pygame.display.set_caption("Video Editor")
    surface = pygame.display.set_mode((INIT_WIDTH, INIT_HEIGHT), pygame.RESIZABLE)
    surface.fill(BLACK)

    clock = pygame.time.Clock()

    resized = False
    width, height = INIT_WIDTH, INIT_HEIGHT

    scene = vpy.types.Scene()

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
                    path = asksaveasfilename()
                    if path:
                        vpy.fileio.save_project(scene, path)
                elif kmod(event.key, pygame.K_o, ctrl=True):
                    path = askopenfilename()
                    if path:
                        scene = vpy.fileio.open_project(path)

        resized = False


main()
