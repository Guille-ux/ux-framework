/* This program is free software: you can redistribute it and/or modify
/* it under the terms of the GNU General Public License as published by
/* the Free Software Foundation, either version 3 of the License, or
/* (at your option) any later version.
/* This program is distributed in the hope that it will be useful,
/* but WITHOUT ANY WARRANTY; without even the implied warranty of
/* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
/* GNU General Public License for more details.
/* You should have received a copy of the GNU General Public License
/* along with this program. If not, see <https://www.gnu.org/licenses/>.
/* Copyright (c) 2025 Guillermo Leira Temes
/* */

void putchar(int pos, char c) {
    char *cpt = (char *)0xB8000;
    cpt += pos * 2;
    *cpt = c;
}

char getchar() {
    unsigned char tecla;
    asm volatile ("inb $0x60, %0" : "=a"(tecla));
    return tecla;
}
