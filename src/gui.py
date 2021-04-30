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

import time
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
    drag_margin = 5

    def __init__(self, prefs: Preferences):
        self.prefs = prefs
        if not prefs.has("layout.verticalsep"):
            prefs.set("layout.verticalsep", 0.8)
        if not prefs.has("layout.horizontalsep"):
            prefs.set("layout.horizontalsep", 0.5)

        self.preview = Preview()

        self.dragging = 0    # bit 0 = dragging vertical, bit 1 = dragging horizontal
        self.x_sep = self.prefs.get("layout.verticalsep")
        self.y_sep = self.prefs.get("layout.horizontalsep")

    def draw(self, surface):
        width, height = surface.get_size()
        x_sep = self.x_sep*width
        y_sep = self.y_sep*height

        # Grid resize
        if shared.mouse_pressed[0]:
            margin = self.drag_margin

            # Drag vertical separator
            if (shared.mouse_event_1 and x_sep-margin<=shared.mouse_pos[0]<=x_sep+margin) or self.dragging&1:
                self.dragging |= 1
                self.x_sep = shared.mouse_pos[0]/width

            # Drag horizontal separator
            if (shared.mouse_event_1 and y_sep-margin<=shared.mouse_pos[1]<=y_sep+margin and
                    shared.mouse_pos[0]<=x_sep+margin) or self.dragging&2:
                self.dragging |= 2
                self.y_sep = shared.mouse_pos[1]/height

        else:
            self.dragging = 0
            self.prefs.set("layout.verticalsep", self.x_sep)
            self.prefs.set("layout.horizontalsep", self.y_sep)

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

    prefs = Preferences(PREFS_PATH, PREFS_LOCK_PATH)
    wm = WindowManager(prefs)

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
        shared.mouse_event_1 = False
        shared.mouse_event_2 = False
        shared.mouse_event_3 = False
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    shared.mouse_event_1 = True
                elif event.button == 2:
                    shared.mouse_event_2 = True
                elif event.button == 3:
                    shared.mouse_event_3 = True

        if resized:
            surface.fill(BLACK)
        wm.draw(surface)

        resized = False

    set_run(False)
    pygame.quit()
