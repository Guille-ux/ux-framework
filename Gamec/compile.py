# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# Copyright (c) 2025 Guillermo Leira Temes
# 
import os
import sys

if sys.argv[1] == "help":
	print("usage → python3 compile.py [input_file] [out_file]")
else:
	try:
		in_file = sys.argv[1]
		out_file = sys.argv[2]
		os.system(f"gcc -o {out_file} {in_file} -lglut -lGL -lGLU")
		print("[+] File Compiled! [+]")
	except Exception as e:
		print(f"[!] Error: {e} [!]")
