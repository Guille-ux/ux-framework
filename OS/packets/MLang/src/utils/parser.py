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
def parse_var(var_def):
	code = []
	if not var_def.startswith("var "):
		raise Exception("Not a variable def → " + var_def)
	else:
		parts = var_def[4:].split(" ")
		name = parts[0]
		try:
			num = int(parts[1])
			code.append(f"var_num {name} {parts[1]}\n")
		except Exception:
			code.append(f"var_var {name} {parts[1]}\n")
		i = 2
		while i < len(parts):		
			if parts[i] == "*":
				if var(parts[i+1]):
					code.append(f"{name} *= {parts[i+1]}\n")
				else:
					code.append(f"var_num tmp {parts[i+1]}\n")
					code.append(f"{name} *= tmp\n")
					code.append(f"remove tmp\n")
			elif parts[i] == "-":
				if var(parts[i+1]):
					code.append(f"{name} -= {parts[i+1]}\n")
				else:
					code.append(f"var_num tmp {parts[i+1]}\n")
					code.append(f"{name} -= tmp\n")
					code.append(f"remove tmp\n")
			elif parts[i] == "/":
				if var(parts[i+1]):
					code.append(f"{name} /= {parts[i+1]}\n")
				else:
					code.append(f"var_num tmp {parts[i+1]}\n")
					code.append(f"{name} /= tmp\n")
					code.append(f"remove tmp\n")
			elif parts[i] == "+":
				if var(parts[i+1]):
					code.append(f"{name} += {parts[i+1]}\n")
				else:
					code.append(f"var_num tmp {parts[i+1]}\n")
					code.append(f"{name} += tmp\n")
					code.append(f"remove tmp\n")
			i += 2
		return "".join(code)
			 
def var(part):
	try:
		num = int(part)
	except Exception:
		return True
	return False
