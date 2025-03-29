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
RAM_SIZE = 512

class VMachine:
    def __init__(self):
        self.counter = 0
        self.regs = [0] * 9
        self.ram = [0] * RAM_SIZE

    def pch(self, char_code, row, col):
        """
        Función que imprime un caracter ASCII en una posición determinada en una pantalla de 80x24
        """
        # Convertimos el código del carácter a su equivalente ASCII
        char = chr(char_code)
        # Imprimimos en la posición adecuada de la consola
        # Limitar las posiciones a un máximo de 80x24
        if 0 <= row < 24 and 0 <= col < 80:
            print(f"\033[{row + 1};{col + 1}H{char}", end="")

    def exec(self, ins):
        self.counter += 1
        opcode = ins % 10
        ins //= 10
        reg_idx = ins % 10
        value = (ins // 10) % 10
        outreg = self.regs[reg_idx]
        inreg = (ins // 100) % 10

        if opcode == 1:  # MOV
            if value == 0:
                self.regs[reg_idx] = inreg
            else:
                self.regs[reg_idx] = self.regs[inreg]

        elif opcode == 2:  # ADD
            if value == 0:
                self.regs[reg_idx] += inreg
            else:
                self.regs[reg_idx] += self.regs[inreg]

        elif opcode == 3:  # SUB
            if value == 0:
                self.regs[reg_idx] -= inreg
            else:
                self.regs[reg_idx] -= self.regs[inreg]

        elif opcode == 4:  # MUL
            if value == 0:
                self.regs[reg_idx] *= inreg
            else:
                self.regs[reg_idx] *= self.regs[inreg]

        elif opcode == 5:  # DIV
            if value == 0:
                self.regs[reg_idx] //= inreg
            else:
                self.regs[reg_idx] //= self.regs[inreg]

        elif opcode == 6:  # STORE
            self.ram[self.regs[reg_idx]] = self.regs[inreg]

        elif opcode == 7:  # JUMP
            condition1 = value
            jump_target = self.regs[inreg]

            reg_val = self.regs[reg_idx]
            condition_met = 0

            if condition1 == 1 and reg_val < 0:
                condition_met = 1
            elif condition1 == 2 and reg_val == 0:
                condition_met = 1
            elif condition1 == 3 and reg_val > 0:
                condition_met = 1
            elif condition1 == 4 and reg_val != 0:
                condition_met = 1
            elif condition1 == 5:
                condition_met = 1

            if condition_met:
                self.counter = jump_target

        elif opcode == 8:  # LOAD
            self.regs[reg_idx] = self.ram[self.regs[inreg]]

        elif opcode == 9:  # INTERRUPT (pch)
            if value == 1:
                # pch(ASCII, row, col)
                self.pch(self.regs[reg_idx], self.regs[inreg] // 80, self.regs[inreg] % 80)

