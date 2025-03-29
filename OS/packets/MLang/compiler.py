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
import src.swelcomp.compiler as comp
from src.utils import findutils as find
from src.utils import parser

print(str(find.find_funcs("func hola: {\nprint hola \n}"))) # prueba de findutils [éxito]
print(parser.parse_var("var hola 5 * 5")) # prueba de var_parser [éxito]
