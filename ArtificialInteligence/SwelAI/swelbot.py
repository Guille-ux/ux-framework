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
import json
import random

class SimpleBot:
	def __init__(self, emb_size, responses_file, vocab_file, n_heads=1, tokens=10, lr=0.01):
		self.chatbot = mm.PreChatBotV2(vocab_file, emb_size, n_heads, tokens, lr)
		self.v_file = vocab_file
		self.emb_size = emb_size
		self.num_heads = n_heads
		self.tokens = tokens
		self.lr = lr
		self.corpus = []
		self.responses_file = responses_file
		with open(responses_file, "r") as f:
			self.responses = json.load(f)
	def train_chatbot(self, data_file, epochs=10):
		with open(data_file, "r") as f:
			data = json.load(f)
		att_outs=data["attention"]["outs"]
		att_ins = data["attention"]["inputs"]
		for h in att_ins:
			for s in h:
				s["q"]=s["q"].lower()
				s["q"]=s["q"].split(" ")
				for word in s["q"]:
					word = self.chatbot.word_to_id.get_id(word)
				s["q"] = sum(s["q"], [])
		neural_outs = data["neural"]["outs"]
		neural_ins = data["neural"]["inputs"]
		neural_ins = [sum([(self.chatbot.word_to_id.get_id(word) for word in ins], []) for ins in neural_ins]
		att_data = {"inputs":att_ins, "outs":att_outs}
		neural_data = {"inputs":neural_ins, "outs":neural_outs}
		self.chatbot.train(att_data, neural_data, epochs)
	def predict(self, inputs):
		return self.responses[self.chatbot.predict_answer(inputs)] % len(self.responses)
	def sl(self, base_name, sl):
		base_head = base_name + "_heads_"
		neural = base_name + "_neural.json"
		ider = base_name + "_word_to_id.json"
		matrix = base_name + "_matrix.json"
		head_names = [base_head+str(i) for i in self.num_heads]
		names = {"matrix":matrix, "id":ider, "predicter":neural, "attention":head_names}
		if sl=="save":
			self.chatbot.save_model(names)
		elif sl=="load":
			self.chatbot.load_model(names)
		else:
			return -1

