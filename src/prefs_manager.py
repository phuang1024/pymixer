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

import json
import subprocess
from constants import *
from prefs import Preferences


def prefs_manager():
    print("Type \"h\" for help.")

    prefs = Preferences(PREFS_PATH, PREFS_LOCK_PATH)
    while True:
        try:
            cmd = input(">>> ").strip().split()
        except EOFError:
            print()
            break
        data = prefs.load()

        if cmd[0] == "h":
            print("p                         print preferences json path")
            print("o                         open preferences json with xdg-open")
            print("l                         list all preferences and values")
            print("r <name>                  remove preference entry")
            print("e <name> <value> <type>   edit or add preference entry, type is optional")

        elif cmd[0] == "p":
            print(PREFS_PATH)

        elif cmd[0] == "o":
            subprocess.Popen(["xdg-open", PREFS_PATH])

        elif cmd[0] == "l":
            print(json.dumps(data, indent=4))

        elif cmd[0] == "r":
            if len(cmd) < 2:
                print("Please run with r <name>")
            else:
                if cmd[1] in data:
                    if input(f"Remove entry {cmd[1]}? (y/N) ").strip().lower() == "y":
                        data.pop(cmd[1], None)
                        prefs.dump(data)
                else:
                    print(f"No entry: {cmd[1]}")

        elif cmd[0] == "e":
            if len(cmd) < 3:
                print("Please run with e <name> <value> <type>")
            else:
                val = cmd[2]
                if len(cmd) >= 4:
                    if cmd[3] == "bool":
                        val = bool(val)
                    elif cmd[3] == "int":
                        val = int(val)
                    elif cmd[3] == "float":
                        val = float(val)
                    elif cmd[3] == "str":
                        val = str(val)
                    elif cmd[3] in ("null", "None", "NoneType"):
                        val = None
                    else:
                        print(f"Unrecognized type: {cmd[3]}")
                        continue
                data[cmd[1]] = val
                prefs.dump(data)
