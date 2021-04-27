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
import vpy
from vpy.types import Context, Operator, Scene

UINT =   "<I"
SINT =   "<i"
DOUBLE = "d"


class CORE_OT_SaveScene(Operator):
    label = "Save Scene"
    description = "Saves scene as a binary file."
    idname = "core.save_scene"

    def execute(self, context: Context, *args, **kwargs) -> str:
        if "path" not in kwargs:
            self.report("ERROR", "Did not give path argument.")
            return {"status": False}

        with open(kwargs["path"], "wb") as file:
            scene = vpy.context.scene

            file.write(struct.pack(UINT, len(scene.meta)))
            file.write(scene.meta)
            file.write(struct.pack(DOUBLE, scene.time))
            file.write(struct.pack(UINT, len(scene.date)))
            file.write(scene.date)
            file.write(bytes([scene.is_saved, scene.is_dirty]))

        return {"status": True}


class CORE_OT_OpenScene(Operator):
    label = "Open Scene"
    description = "Opens binary file as a scene."
    idname = "core.open_scene"

    def execute(self, context: Context, *args, **kwargs) -> str:
        if "path" not in kwargs:
            self.report("ERROR", "Did not give path argument.")
            return {"status": False}

        scene = Scene()
        with open(kwargs["path"], "rb") as file:
            scene.meta = file.read(struct.unpack(UINT, file.read(4))[0])
            scene.time = struct.unpack(DOUBLE, file.read(8))[0]
            scene.date = file.read(struct.unpack(UINT, file.read(4))[0])
            scene.is_saved = (file.read(1) == "\x01")
            scene.is_dirty = (file.read(1) == "\x01")

        vpy.context.scene = scene
        return "FINISHED"


classes = (
    CORE_OT_SaveScene,
    CORE_OT_OpenScene,
)

def register():
    for cls in classes:
        vpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        # TODO unregister class
        pass
