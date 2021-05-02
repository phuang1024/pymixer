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

import pygame
import vpy
import shared
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from constants import *
from gui_utils import kmod, setup_api
from prefs import Preferences
from ui.wm import WindowManager
pygame.init()
Tk().withdraw()


def saveas():
    path = asksaveasfilename(
        defaultextension=".mix",
        filetypes=(
            ("Mix File", "*.mix"),
            ("All Files", "*.*")
        )
    )
    if path:
        vpy.ops.core.save_scene(path=path)
        vpy.context.scene.is_saved = True

    return path


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
                        path = saveas()

                elif kmod(event.key, pygame.K_s, ctrl=True, shift=True):
                    path = saveas()

                elif kmod(event.key, pygame.K_o, ctrl=True):
                    path = askopenfilename()
                    if path:
                        vpy.ops.core.open_scene(path=path)
                        vpy.context.scene.is_saved = True

        # Set constants to minimize pygame calls
        shared.mouse_pos = pygame.mouse.get_pos()
        shared.mouse_pressed = pygame.mouse.get_pressed()

        shared.events = events
        shared.mouse_event_1 = False
        shared.mouse_event_2 = False
        shared.mouse_event_3 = False

        shared.keys_pressed = pygame.key.get_pressed()
        shared.keys_ctrl = (shared.keys_pressed[pygame.K_LCTRL] or shared.keys_pressed[pygame.K_RCTRL])
        shared.keys_shift = (shared.keys_pressed[pygame.K_LSHIFT] or shared.keys_pressed[pygame.K_RSHIFT])
        shared.keys_alt = (shared.keys_pressed[pygame.K_LALT] or shared.keys_pressed[pygame.K_RALT])

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
