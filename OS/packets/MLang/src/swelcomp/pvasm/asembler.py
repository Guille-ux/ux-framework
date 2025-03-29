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
INS_SIZE = 5

# Diccionario para simular los registros
registers = {
    "AX": 0, "BX": 1, "CX": 2, "DX": 3, "EX": 4, "FX": 5, "GX": 6, "HX": 7, "IX": 8
}

def vasm_len(s):
    """Devuelve la longitud de la cadena"""
    return len(s)

def vasm_strcmp(str1, str2, length, offset=0):
    """Compara las cadenas desde una posición específica"""
    for i in range(length):
        if str1[i + offset] != str2[i]:
            return False
    return True

def asemble(line):
    """Simula el ensamblador"""
    opcode = -1
    reg_idx = -1
    value = -1
    in_reg = -1

    if vasm_strcmp(line, "MOV", 3, 0):
        opcode = 1
    elif vasm_strcmp(line, "ADD", 3, 0):
        opcode = 2
    elif vasm_strcmp(line, "SUB", 3, 0):
        opcode = 3
    elif vasm_strcmp(line, "MUL", 3, 0):
        opcode = 4
    elif vasm_strcmp(line, "DIV", 3, 0):
        opcode = 5
    elif vasm_strcmp(line, "JNQ", 3, 0):
        opcode = 7
        value = 4
    elif vasm_strcmp(line, "LOA", 3, 0):
        opcode = 8
    elif vasm_strcmp(line, "STR", 3, 0):
        opcode = 6
    elif vasm_strcmp(line, "JLT", 3, 0):
        opcode = 7
        value = 1
    elif vasm_strcmp(line, "JGT", 3, 0):
        opcode = 7
        value = 3
    elif vasm_strcmp(line, "JQT", 3, 0):
        opcode = 7
        value = 2
    elif vasm_strcmp(line, "JMP", 3, 0):
        opcode = 7
        value = 5
    elif vasm_strcmp(line, "INT", 3, 0):
        opcode = 9
        if vasm_strcmp(line, "PUT", 3, 7):
            value = 1
        else:
            return -3

    if opcode < 0:
        return -1

    # Comprobamos los registros
    for reg, idx in registers.items():
        if vasm_strcmp(line, reg, len(reg), 4):
            reg_idx = idx
            break

    if reg_idx < 0:
        return -2

    if opcode == 7:
        if vasm_strcmp(line, "JMP", 3, 7) == False:
            return -4
    else:
        if value < 0:
            if vasm_strcmp(line, "NUM", 3, 7):
                value = 0
            elif vasm_strcmp(line, "REG", 3, 7):
                value = 1

    if value < 0:
        return -3

    # Comprobamos el registro de entrada para los saltos
    if opcode == 7 or value != 0:
        for reg, idx in registers.items():
            if vasm_strcmp(line, reg, len(reg), 11):
                in_reg = idx
                break
    elif value == 0:
        in_reg = int(line[11])

    # Calculamos el bytecode final
    bytecode = 10000 + in_reg * 1000 + value * 100 + reg_idx * 10 + opcode
    return bytecode

