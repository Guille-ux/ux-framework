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
def coparse(code, n):
	txt = code.split("\n")
	final_txt = []
	counter = 0
	counter_list = []
	for i in txt:
		rtxt = []
		if i.startswith("if")
			counter_list.append(counter)
			splitted = i.split(" ")
			cof = splitted[1]
			tco = splitted[2]
			cos = splitted[3]
			the = splitted[4]
			if tco == "==":
				rtxt.append(f"var_var tmp {cos}\n")
				rtxt.append(f"tmp -= {cof}\n")
				rtxt.append(f"jeq tmp {the}\n")
				rtxt.append(f"remove tmp\n")
			if tco == ">":
				rtxt.append(f"var_var tmp {cos}\n")
				rtxt.append(f"tmp -= {cof}\n")
				rtxt.append(f"jlt tmp {the}\n")
				rtxt.append(f"remove tmp\n")
			if tco == "<":
				rtxt.append(f"var_var tmp {cos}\n")
				rtxt.append(f"tmp -= {cof}\n")
				rtxt.append(f"jgt tmp {the}\n")
				rtxt.append(f"remove tmp\n")
			if tco == "!=":
				rtxt.append(f"var_var tmp {cos}\n")
				rtxt.append(f"tmp -= {cof}\n")
				rtxt.append(f"jnq tmp {the}\n")
				rtxt.append(f"remove tmp\n")
			final_txt.append(rtxt)
		counter += 1
	try:
		return [final_txt[n], counter_list[n]]
	except Exception:
		raise Exception("Fatal ERROR")
