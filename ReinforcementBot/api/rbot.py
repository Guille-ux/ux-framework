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
import random
import json
import time

class BotsManager:
	def __init__(self, responses_file, stop_file, maxs, max_contexts=100, jon=None):
		self.bot = ReinforcementBot(responses_file, stop_file, maxs, jon)
		self.max_context =max_contexts
		self.responses_file = responses_file
		self.stop_file = stop_file
		self.max_mat = maxs
		self.users_last={}
		self.actual_context = 0
		self.user_times = {}
	def ask(self, question, user_id):
		now = time.time()
		for k, v in self.user_times.items():
			minutes = (v-now)/60
			if minutes >= 30:
				del self.users_last[k]
				del self.user_times[k]
				self.actual_context -= 1
		ans = self.bot.ask(question)
		if self.actual_context == self.max_context:
			pass
		else:
			if user_id in self.users_last:
				   self.actual_context -= 1
			self.actual_context += 1
			self.users_last[user_id] = self.bot.last
			self.user_times[user_id]=now
		return ans
	def reforce(self, yn, user_id):
		now = time.time()
		for k, v in self.user_times.items():
			minutes = (v-now)/60
			if minutes >= 30:
				del self.users_last[k]
				del self.user_times[k]
				self.actual_context -= 1
		if user_id not in self.users_last:
			return "Lo siento, pero no estas en la lista"
		self.bot.last = self.users_last[user_id]
		self.bot.reforce(yn)
		del self.users_last[user_id]
		self.actual_context -= 1
		return "Gracias por su Opinión"
class ReinforcementBot:
	def __init__(self, responses_file, stop_file, max_saves, jon=None, e=0.1):
		self.e = e
		self.max_mat = max_saves
		self.responses_file = responses_file
		with open(responses_file, "r") as f:
			if jon=="json":
				self.responses=json.load(f)
			else:
				self.responses=f.read().splitlines()
		with open(stop_file, "r") as f:
			self.stop = f.read().splitlines()
		self.pointer = 0
		self.qs = {}
		self.mat = [[0]*len(self.responses) for _ in range(max_saves)]
		self.last = [0, 0]
	def format(self, text):
		ret = text.lower()
		ret = ret.replace("á", "a")
		ret = ret.replace("é", "e")
		ret = ret.replace("í", "i")
		ret = ret.replace("ó", "o")
		ret = ret.replace("ú", "u")
		ret = ret.strip("¿")
		ret = ret.strip("?")
		ret = ret.strip("¡")
		ret = ret.strip("!")
		ret = ret.strip(".")
		ret = ret.strip(",")
		ret = ret.strip("'")
		ret = ret.strip('"')
		ret = ret.strip(";")
		ret = ret.strip("-")
		ret = ret.strip(":")
		ret = ret.split(" ")
		ret = [word for word in ret if word not in self.stop]
		return " ".join(ret)
	def ask(self, text):
		text = self.format(text)
		if text in self.qs:
			num = self.qs[text]
		else:
			self.qs[text]=self.pointer
			num = self.pointer
		self.pointer += 1
		if self.pointer == self.max_mat:
			self.pointer = 0
		tmp = []
		max_num = max(self.mat[num])
		for i in range(len(self.responses)):
			if self.mat[num][i] == max_num:
				tmp.append(i)
			else:
				pass
		if random.uniform(0, 1) < self.e:
			selected = self.responses.index(random.choice(self.responses))
		else:
			selected = random.choice(tmp)
		self.last = [num, selected]
		return self.responses[selected]
	def reforce(self, yn):
		if yn=="y":
			v = 1
		elif yn=="n":
			v = -1
		else:
			return 0
		x = self.last[0]
		y = self.last[1]
		self.mat[x][y]+=v
		return 1
	def converse(self, name, username):
		print("Escribe quit o exit para salir.")
		print("Hola " + username  + ", mi nombre es " + name)
		while True:
			question = input("Di algo: ")
			if question == "quit" or question == "exit":
				break
			print(self.ask(question))
			opt = input("Te gusto la respuesta (y/n): ")
			self.reforce(opt)
		print("Saliste correctamente, espero que lo hayas pasado bien")
	def file_bot(self, filename, sl):
		if sl=="save":
			data = {"mat":self.mat, "pointer":self.pointer}
			with open(filename, "w") as f:
				json.dump(data, f)
		elif sl=="load":
			with open(filename, "r") as f:
				data = json.load(f)
			self.pointer=data["pointer"]
			self.mat=data["mat"]
		else:
			return 0
