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
import models
import math
import nltk
from nltk.corpus import brown
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import random
import json


def custom_vectorize(sentence, vectorizer, len_vectors):
	out = []
	processed = preprocess([auto_token(sentence)])[0]
	for word in processed:
		if word in vectorizer:
			out.append(vectorizer[word])
		else:
			out.append([0]*len_vectors)
	return out

def preprocess(data):
	stop_words = set(stopwords.words("english"))
	processed_data = []
	for sentence in data:
		sentence = [word.lower() for word in sentence]
		sentence = [word for word in sentence if word not in stop_words]
		sentence = [word.strip(",") for word in sentence]
		sentence = [word.strip(".") for word in sentence]
		sentence = [word.strip(":") for word in sentence]
		sentence = [word.strip("&") for word in sentence]
		sentence = [word.strip("$") for word in sentence]
		sentence = [word.strip("?") for word in sentence]
		sentence = [word.strip("¿") for word in sentence]
		sentence = [word.strip(")") for word in sentence]
		sentence = [word.strip("(") for word in sentence]
		sentence = [word for word in sentence if word.strip(" ") != ""]
		processed_data.append(sentence)
	return processed_data


def auto_token(sentence):
	txt = nltk.sent_tokenize(sentence)
	return [word_tokenize(word) for word in txt]

vocab = brown.words()
vo = []
[vo.append(word.lower()) for word in vocab if word not in vo]
corpus = brown.sents()
processed = preprocess(corpus)
matrix = models.CooCurrencyMatrix(vo)
matrix.words.save("word_ids.json")
matrix.load_matrix("mat.json")
model = models.AutoEncoder(len(vo), 500)
for _ in range(300):
	for x in range(500):
		model.train([matrix.get_vector("dog")], 1)
model.save("model.json")
reduced = model.reduce(matrix.get_vector("dog"))
reducides = [model.reduce(matrix.get_vector(word)) for word in ["car", "road", "fish", "girl", "kid", "man", "woman", "wife", "cat", "dog", "pet", "mine"]]
with open("reduceds.json", "w") as f:
	json.dump(reducides, f)
print("Dog antes de AutoEncoder → "+ str(matrix.get_vector("dog")))
print("Dog despues de AutoEncoder → "+str(reduced))
