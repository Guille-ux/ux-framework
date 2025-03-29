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

responses_file = "responses.json"
vocab_file = "vocab.json"
corpus_file = "corpus.json"
train_data = "train_data.json"
embeddings_file = "embeds.json"
with open(vocab_file, "r") as f:
	vocab = json.load(f)
with open(corpus_file, "r") as f:
	corpus = json.load(f)
matrix = mm.CooCurrencyMatrix(vocab)
matrix.build_matrix(corpus)
embs=matrix.get_vector("hola")
matrix.save_matrix("matrix.json")
auto = mm.AutoEncoder(len(embs), 10)
auto.load("reducer.json")



saved = []
for word in vocab:
	i = matrix.get_vector(word)
	saved.append(auto.reduce(i))
with open(embeddings_file, "w") as f:
	json.dump(saved, f)

