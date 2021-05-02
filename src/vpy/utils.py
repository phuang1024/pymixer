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

import numpy as np
import pygame
from typing import Tuple, Union
pygame.init()

GET_PROP = """
@property
def getter(self):
    return self._values[{0}].get()
""".strip()

SET_PROP = """
@coll.{0}.setter
def setter(self, value):
    self._values[{0}].set(value)
""".strip()


def register_class(cls) -> None:
    import vpy

    if issubclass(cls, vpy.types.Operator):
        if not cls.idname.count(".") == 1:
            raise ValueError(f"Operator {cls.idname} idname must have exactly 1 period")

        group, name = cls.idname.split(".")
        if not hasattr(vpy.ops, group):
            vpy.ops.colls[group] = vpy.types.OpCollection()
        coll = getattr(vpy.ops, group)
        if not hasattr(coll, name):
            coll.operators[name] = cls()

        for i, (letter, shift, alt, ctrl) in enumerate(cls.kboard_shortcuts):
            v = ord(letter.lower())
            if not 0 <= v < 256:
                raise ValueError(f"Invalid key {letter} in Operator {cls.idname} keyboard shortcut.")

            idx = shortcut_value((letter, shift, alt, ctrl))
            if idx in vpy.data.kboard_shortcuts:
                vpy.logging.warning(f"Operator {cls.idname} keyboard shortcut {i+1} already exists, skipping.")
                continue
            vpy.data.kboard_shortcuts[idx] = cls.idname

    elif issubclass(cls, vpy.types.PropertyGroup):
        if not cls.idname.count(".") == 0:
            raise ValueError(f"PropertyGroup {cls.idname} idname must not have a dot.")

        coll = vpy.types.PropCollection()
        for attr in cls.__dict__:
            if not attr.startswith("__") and attr != "idname":
                setattr(coll, attr, getattr(cls, attr))
                # coll._values[attr] = getattr(cls, attr)

                # Decorators for getting and setting
                # exec(GET_PROP.format(attr))
                # exec(SET_PROP.format(attr))
                # setattr(coll, attr, getter)
                # setattr(coll, f"{attr}.setter", setter)

        setattr(vpy.types.Scene, cls.idname, coll)

    else:
        raise ValueError("Class to register must inherit from Operator or PropertyGroup")

def unregister_class(cls) -> None:
    import vpy


def shortcut_value(shortcut: Tuple[str, bool, bool, bool]) -> int:
    letter, shift, alt, ctrl = shortcut
    return ord(letter.lower()) + (shift<<8) + (alt<<9) + (ctrl<<10)

def shortcut_to_op(shortcut: Tuple[str, bool, bool, bool]) -> Union[None, str]:
    import vpy

    idx = shortcut_value(shortcut)
    if idx in vpy.data.kboard_shortcuts:
        return vpy.data.kboard_shortcuts[idx]
    else:
        return None


def surf_to_array(surf: pygame.Surface) -> np.ndarray:
    return pygame.surfarray.array3d(surf).swapaxes(0, 1)

def array_to_surf(array: np.ndarray) -> pygame.Surface:
    return pygame.image.frombuffer(array.tobytes(), array.shape[1::-1], "RGB")
