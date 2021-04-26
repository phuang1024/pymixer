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

import struct
from . import types

UINT = "<I"
SINT = "<i"


def save_project(scene: types.Scene, path: str) -> None:
    """
    Saves scene as binary file.
    :param scene: Scene to save. Save the current scene by passing vpy.context.scene
    :param path: Path to save scene.
    """
    with open(path, "wb") as file:
        file.write(struct.pack(UINT, len(scene.meta)))
        file.write(scene.meta)
        file.write(bytes([scene.is_saved, scene.is_dirty]))

        file.write(struct.pack(SINT, scene.frame_start))
        file.write(struct.pack(SINT, scene.frame_end))
        file.write(struct.pack(SINT, scene.frame_step))
        file.write(struct.pack(UINT, scene.fps))


def open_project(path: str) -> types.Scene:
    """
    Opens binary file as a vpy.types.Scene
    :param path: Path to scene file.
    """
    attrs = {}
    with open(path, "rb") as file:
        attrs["meta"] = file.read(struct.unpack(UINT, file.read(4))[0])
        attrs["is_saved"] = (file.read(1) == "\x01")
        attrs["is_dirty"] = (file.read(1) == "\x01")

        attrs["frame_start"] = struct.unpack(SINT, file.read(4))[0]
        attrs["frame_end"] = struct.unpack(SINT, file.read(4))[0]
        attrs["frame_step"] = struct.unpack(SINT, file.read(4))[0]
        attrs["fps"] = struct.unpack(UINT, file.read(4))[0]

    return types.Scene(**attrs)
