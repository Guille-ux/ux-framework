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
from PIL import Image
import math

def div_channels(pixels, vx, vy): #returns 3 matrix there are the image separated in RGB
	red_m = []
	green_m = []
	blue_m = []
	for x in range(vx):
		rline = []
		gline = []
		bline = []
		for y in range(vy):
			p = pixels[x, y]
			rline.append(p[0])
			gline.append(p[1])
			bline.append(p[2])
		red_m.append(rline)
		green_m.append(gline)
		blue_m.append(bline)
	return (red_m, green_m, blue_m)
def join_channels(channels, vx, vy):
	r_m =channels[0]
	g_m =channels[1]
	b_m =channels[2]
	pixels = []
	for x in range(vx):
		line = []
		for y in range(vy):
			r = r_m[x][y]
			g = g_m[x][y]
			b = b_m[x][y]
			r=min(abs(r), 255)
			g=min(abs(g), 255)
			b=min(abs(b), 255)
			r=int(r)
			g=int(g)
			b=int(b)

			line.append((r, g, b))
		pixels.append(line)
	return pixels
def rematrix(array, vx, vy):
	if vx*vy==len(array):
		matrix = []
		for x in range(vx):
			line = []
			for y in range(vy):
				line.append(array[x*vy+y])
			matrix.append(line)
		return matrix
	else:
		return [[-1]*vy for _ in range(vx)]
def matrix_to_image(matrix):
	x=len(matrix)
	y=len(matrix[0])
	image = Image.new("RGB", (x, y))
	pixels = image.load()
	for i in range(x):
		for j in range(y):
			pixels[i, j] =matrix[i][j]
	return image
class ImageCleaner(mm.AutoEncoder):
	def __init__(self, x=500, y=500, rfactor=2, lr=0.01):
		super().__init__(x*y, rfactor, lr)
		self.height=y
		self.width=x
		self.rfactor = rfactor
		self.lr=lr
		self.size = x*y
	def train(self, channels, epochs=300):
		channels=[self.format(channel) for channel in channels]
		super().train(channels, epochs)
	def reduce(self, channel):
		return super().reduce(self.format(channel))
	def rebuild(self, reduced):
		for i in range(self.out_size):
			self.out_out[i] = 0
			for j in range(self.hidden_size):
				self.out_out[i]+=self.hidden_out[j]*self.out_w[i][j]
			self.out_out[i]=self.relu(self.out_out[i])
			self.out_out[i]=int(min(max(0, self.out_out[i]), 255))
		return self.out_out
	def build(self, channel):
		return super().forward(self.format(channel))
	def clean(self, channel):
		reduced = self.reduce(channel)
		return self.rebuild(reduced)
	def format(self, channel):
		return sum(channel, [])
	def save(self, filename): # to avoid train the model every time we use it
		super().save(filename)
	def load(self, filename):
		super().load(filename)

epochs=5
lr=0.01
rfactor = 1
imagen = Image.open("prueba.jpeg")
x, y = imagen.size
rprueba = ImageCleaner(x, y, rfactor, lr)
gprueba = ImageCleaner(x, y, rfactor, lr)
bprueba = ImageCleaner(x, y, rfactor, lr)
pixels = imagen.load()
channels = div_channels(pixels, x, y)
rprueba.train([channels[0]], epochs)
gprueba.train([channels[1]], epochs)
bprueba.train([channels[2]], epochs)
cr = rprueba.clean(channels[0])
cg = gprueba.clean(channels[1])
cb = bprueba.clean(channels[2])
cr = rematrix(cr, x, y)
cg = rematrix(cg, x, y)
cb = rematrix(cb, x, y)
matrix = join_channels([cr, cg, cb], x, y)
fimage = matrix_to_image(matrix)
fimage.save("final.jpeg")
imagen.show()
fimage.show()
