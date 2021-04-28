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


def register_class(cls):
    import vpy

    if issubclass(cls, vpy.types.Operator):
        group, name = cls.idname.split(".")
        if not hasattr(vpy.ops, group):
            vpy.ops.colls[group] = vpy.types.OpCollection()
        coll = getattr(vpy.ops, group)
        if not hasattr(coll, name):
            coll.operators[name] = cls()

    elif issubclass(cls, vpy.types.PropertyGroup):
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
        raise ValueError("Class to register must inherit from Operator")
