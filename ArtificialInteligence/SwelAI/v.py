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
from utils import models as mm
import random

nv = int(input("Nº de vectores: "))
epochs = int(input("Nº de Epochs: "))

vectors = [[random.randint(0, 9) for _ in range(10)] for _ in range(nv)]

auto = mm.AutoEncoder(10, 2)
auto.train(vectors, epochs)
merror=0
for i in vectors:
	error = 0
	r=auto.forward(i)
	for h in range(10):
		error += i[h]-r[h]
	error /= 10
	merror+=error
merror /= nv
print("Error de la IA: " + str(merror))
