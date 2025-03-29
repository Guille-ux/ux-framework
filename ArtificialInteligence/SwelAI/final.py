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
from swelbot import SimpleBot
import json
import random

responses_file = "responses.json"
vocab_file = "vocab.json"
corpus_file = "corpus.json"
train_data = "train_data.json"
embeddings_file = "embeds.json"

with open(vocab_file, "r") as f:
	vocab = json.load(f)
with open(corpus_file, "r") as f:
	corpus = json.load(f)
with open(embeddings_file, "r") as f:
	embeds = json.load(f)
len_embs = len(embeddings[0])
bot = SimpleBot(len_embs, responses_file, vocab_file)
bot.train_chatbot(train_data)
bot.sl("prueba", "save")
bot.predict("kaboom")
