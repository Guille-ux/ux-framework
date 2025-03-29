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
import asembler as asm
from executer import VMachine

nombre = "code.pasm"
with open(nombre, "r") as f:
	code = f.read().splitlines()
code_ext = [asm.asemble(line) for line in code]
code_ext.append(10000)
machine = VMachine()
print("CODIGO COMPILADO: " + str(code_ext))
machine.counter = 0
while True:
	instruction=code_ext[machine.counter]
	if instruction == 10000:
		break
	machine.exec(instruction)

