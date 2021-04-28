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
from constants import *
from gui_utils import draw_dashed_line
pygame.init()


class Preview:
    def __init__(self):
        self.prev_size = None
        self.prev_loc = None

        self.size = 540
        self.loc = [0, 0]

    def draw(self, surface, events, loc, size):
        update = False
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                update = True
                if event.button == 4:
                    self.size *= 1.08
                elif event.button == 5:
                    self.size /= 1.08

        if update or size != self.prev_size or loc != self.prev_loc:
            pygame.draw.rect(surface, BLACK, (*loc, *size))

            surf = pygame.Surface(size, pygame.SRCALPHA)
            x_center = loc[0] + size[0]/2
            y_center = loc[1] + size[1]/2

            width = self.size
            height = width / vpy.context.scene.output.x_res.get() * vpy.context.scene.output.y_res.get()
            x = x_center + self.loc[0] - width/2
            y = y_center + self.loc[1] - height/2

            draw_dashed_line(surf, (x, y), (x+width, y), 6, GRAY, 1)
            draw_dashed_line(surf, (x, y+height), (x+width, y+height), 6, GRAY, 1)
            draw_dashed_line(surf, (x, y), (x, y+height), 6, GRAY, 1)
            draw_dashed_line(surf, (x+width, y), (x+width, y+height), 6, GRAY, 1)

            surface.blit(surf, loc)

        self.prev_size = size
        self.prev_loc = loc
