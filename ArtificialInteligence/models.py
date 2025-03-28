import random
import math
import json

class MarkovChain:
	def __init__(self, corpus):
		self.corpus = corpus
		self.vocablo = []
		self.ret = ""
		self.count = 0
	def train(self, h):
		if h:
			self.vocablo = []
		esekas = []
		for sentence in self.corpus:
			keys = []
			sp = sentence.split(" ")
			sk = []
			for k in sp:
				if k in sk:
					pass
				else:
					sk.append(k)
			for i in sk:
				key = []
				for x in sp:
					if (i + " " + x) in sentence:
						key.append(x)
				keys.append((i, key)) #estructura datos : ("palabra", ["siguiente 1".....])
			esekas.append(keys)
		claves = []
		for x in esekas:
			for y in x:
				clave = y[0]
				valor = y[1]
				if clave in claves:
					for z in self.vocablo:
						if clave == z[0]:
							z[1].extend(valor)
				else:
					claves.append(clave)
					self.vocablo.append((clave, valor))
		print(str(self.vocablo))
	def gen(self, seed):
		self.counted -= 1
		for i in self.vocablo:
			if i[0] == seed:
				self.ret += " " + seed
				if self.counted == 0:
					return seed
				try:
					current = self.gen(random.choice(i[1]))
				except Exception:
					current = seed
				return current
	def ultigen(self, seed, counted):
		self.counted = counted
		self.ret = ""
		self.gen(seed)
		return self.ret
import csv

class Regression:
	def __init__(self, data, model):
		self.data = data
		self.model = model
		self.l = 0
		self.a = 0
		self.b = 0
		self.c = 0
		self.ra = []
		self.rs = []
	def predict(self):
		print(self.l)
		b = self.data * self.l + self.a
		return b
	def train(self):
		self.mod()
		n = 0
		for i in self.ra:
			self.c += i[0]
			n += 1
		self.b = self.c / n
		n = 0
		self.c = 0
		for i in self.ra:
			self.c += i[0]
		n += 1
		self.l = (self.b - self.a) / self.ra[0][1]
		print("TRAINED")
	def mod(self):
		with open("models/" + self.model, "r") as f:
			read = csv.reader(f)
			r = "PATATA"
			for row in read:
				if r == "PATATA":
					r = float(row[1])
				row[0] = float(row[0])  # Elimina esta línea si no es intenc
				row[1] = float(row[1])
				if row[1] == r:
					self.rs.append(row)
				else:
					self.ra.append(row)

import csv

class DecissionTree:
	def __init__(self, data, model):
		self.model = model
		self.data = data
		self.rs = []
		self.cut = 0
		self.tope = int(input("TOPE DEL CORTE:\t"))
		self.maxerror = 20000000000000000000000

	def predict(self):
		print(f"porcentaje de acierto {1 - self.maxerror / len(self.rs)}")
		if self.cut < self.data:
			return 1
		else:
			return 0

	def train(self):
		self.mod()
		for i in range(1, self.tope):
			error = 0
			for r in self.rs:
				if r[0] > i and r[1] == 1 or r[0] < i and r[1] == 0:
					pass
				else:
					error += 1
			if error < self.maxerror:
				self.maxerror = error
				self.cut = i

	def mod(self):
		with open("models/" + self.model, "r") as f:
			read = csv.reader(f)
			r = "PATATA"
			for row in read:
				row[0] = float(row[0])
				row[1] = float(row[1])
				self.rs.append(row)
class Neurone:
	def __init__(self, umbral):
		self.w11 = random.uniform(-0.5, 0.5)
		self.w22 = random.uniform(-0.5, 0.5)
		self.input1 = 0
		self.input2 = 0
		self.need = umbral
		self.out = 0
	def input(self, input1, input2):
		self.input1 = input1
		self.input2 = input2
	def act(self):
		self.out = (abs(self.out) / (abs(self.out) +1))
	def life(self, max_epochs):
		for _ in range(max_epochs):
			self.out = self.w11 * self.input1 + self.w22 * self.input2
			self.act()
			error = self.need - self.out
			adjuster = error
			self.w11 += 0.001 * adjuster * self.input1 * -1
			self.w22 += 0.001 * adjuster * self.input2 * -1
		return self.out
	def use(self, input1, input2):
		self.input(input1, input2)
		self.out = self.w11 * self.input1 + self.w22 * self.input2
		self.act()
		return self.out
class WordId:
	def __init__(self):
		self.word_to_id = {}
		self.next_id = 1
	def get_id(self, word):
		if word in self.word_to_id:
			return self.word_to_id[word]
		self.word_to_id[word]=self.next_id
		self.next_id+=1
		return self.word_to_id[word]
	def load(self, filename):
		with open(filename, "r") as f:
			self.word_to_id = json.load(f)
	def save(self, filename):
		with open(filename, "w") as f:
			json.dump(self.word_to_id, f)
class WordVectorizer:
	def __init__(self, vocab, words=WordId(), embedding_size=20, context_window=10):
		self.vocab = vocab
		self.words = words
		self.neurons = {word: [Neurone(0.5) for _ in range(embedding_size)] for word in vocab}
		self.context_window = context_window
	def train(self, data, epochs=300):
		for z in range(epochs):
			print("Epoch: "+str(z))
			for sentence in data:
				for i in range(len(sentence)):
					word = sentence[i]
					print("Word: " + word)
					context_sum = 0
					for h in range(max(0, i-self.context_window), min(len(sentence), i+self.context_window)):
						context_sum += self.words.get_id(sentence[h])
						context_sum *= h+1
					for j in range(max(0, i - self.context_window), min(len(sentence), i+self.context_window)):
						if j==i:
							continue
						context_word = sentence[j]
						for k, neuron in enumerate(self.neurons[word]):
							input1 = self.words.get_id(word)
							input2 = self.words.get_id(context_word)
							distance = abs(i-j)
							penalty = 1 / (distance+1)
							neuron.need = penalty*(context_sum)
							neuron.input(input1, input2)
							neuron.life(1)
	def get_vector(self, word):
		if word in self.neurons:
			return [neuron.use(self.words.get_id(word), 1) for neuron in self.neurons[word]]
		else:
			return None 
	def save_dict(self, filename):
		data = {}
		for word in self.vocab:
			data[word] = self.get_vector(word)
		with open(filename, "w") as f:
			json.dump(data, f)
class NeuralNetwork:
	def __init__(self, in_layer, hidden_layer, out_layer, lr=0.01):
		self.in_size = in_layer
		self.hidden_size = hidden_layer
		self.out_size = out_layer
		self.hidden_b = [1 for _ in range(hidden_layer)]
		self.out_b = [1 for _ in range(out_layer)]
		self.hidden_w = [[random.uniform(0.1, 1.0) for _ in range(in_layer)] for _ in range(hidden_layer)]
		self.out_w = [[random.uniform(0.1, 1.0) for _ in range(hidden_layer)] for _ in range(out_layer)]
		self.hidden_out = [0] * hidden_layer
		self.out_out = [0] * out_layer
		self.lr = lr
	def relu(self, x):
		return max(x, 0)
	def relud(self, x):
		return 1 if x > 0 else 0
	def forward(self, inputs):
		#hidden layer
		for i in range(self.hidden_size):
			self.hidden_out[i] = 0
			for j in range(self.in_size):
				self.hidden_out[i] += inputs[j]*self.hidden_w[i][j]
			self.hidden_out[i] += self.hidden_b[i]
			self.hidden_out[i] = self.relu(self.hidden_out[i])
		#out layer
		for i in range(self.out_size):
			self.out_out[i] = 0
			for j in range(self.hidden_size):
				self.out_out[i] += self.hidden_out[j]*self.out_w[i][j]
			self.out_out[i] += self.out_b[i]
			self.out_out[i] = self.relu(self.out_out[i])
		return self.out_out
	def backward(self, inputs, expected):
		out_error = [(expected[i]-self.out_out[i])*self.relud(self.out_out[i]) for i in range(self.out_size)]
		hidden_error = [0]*self.hidden_size
		for i in range(self.hidden_size):
			for j in range(self.out_size):
				hidden_error[i] += out_error[j]*self.out_w[j][i]
			hidden_error[i] *= self.relud(self.hidden_out[i])
		for i in range(self.out_size):
			for j in range(self.hidden_size):
				self.out_w[i][j] += self.lr * out_error[i] * self.hidden_out[j]
			self.out_b[i] += self.lr*out_error[i]
		for i in range(self.hidden_size):
			for j in range(self.in_size):
				self.hidden_w[i][j] += self.lr * hidden_error[i] * inputs[j]
			self.hidden_b[i] += self.lr*hidden_error[i]
	def train(self, input_data, out_data, epochs=300):
		print("Starting Training....")
		for e in range(epochs):
			print("Epoch: " + str(e+1) + "/" + str(epochs))
			for i in range(len(input_data)):
				self.forward(input_data[i])
				self.backward(input_data[i], out_data[i])
	def save_model(self, filename):
		data = {"hidden":self.hidden_w, "out":self.out_w, "out_b":self.out_b, "hidden_b": self.hidden_b}
		with open(filename, "w") as f:
			json.dump(data, f)
	def load_model(self, filename):
		with open(filename, "r") as f:
			data = json.load(f)
			self.hidden_w = data["hidden"]
			self.out_w = data["out"]
			self.hidden_b = data["hidden_b"]
			self.out_b = data["out_b"]
class DisperseMatrix: #experimental, only for the CooCurrencyMatrix
	def __init__(self, l1, l2):
		self.len1 = l1
		self.len2 = l2
		self.data = {}
	def add_value(self, value, x, y):
		if value != 0:
			self.data[(x, y)] = value
		elif (x, y) in self.data:
			del self.data[(x, y)]
	def get_value(self, x, y):
		if (x, y) in self.data:
			return self.data[(x, y)]
		else:
			return 0
	def get_x(self, x):
		ret = []
		for y in range(self.len2):
			if (x, y) in self.data:
				ret.append(self.get_value(x, y))
			else:
				ret.append(0)
		return ret
	def load(self, filename):
		with open(filename, "r") as f:
			load = json.load(f)
			self.len1 = load["l1"]
			self.len2 = load["l2"]
			self.data = {tuple(k): v for k, v in load["data"]}
	def save(self, filename):
		save = {"l1":self.len1, "l2":self.len2, "data":[[[list(k)], v] for k, v in self.data.items()]}
		with open(filename, "w") as f:
			json.dump(save, f)
class CooCurrencyMatrix:
	def __init__(self, vocab, context_window=5):
		self.vocab = vocab
		self.context_window = context_window
		self.matrix = DisperseMatrix(len(vocab), len(vocab))
		self.words = WordId()
		[self.words.get_id(word) for word in vocab]
	def build_matrix(self, corpus, i=False):
		if i == True:
			corpus = [[word.lower() for word in sentence.split(" ") if word in self.vocab] for sentence in corpus]
		else:
			pass
		for sentence in corpus:
			for i in range(len(sentence)):
				word = sentence[i]
				for j in range(max(0, i-self.context_window), min(len(sentence), i+self.context_window)):					
					if j==i:
						continue
					context_word = sentence[j]
					self.matrix.add_value(self.matrix.get_value(self.words.get_id(word), self.words.get_id(context_word))+1, self.words.get_id(word), self.words.get_id(context_word))
	def reset_matrix(self):
		self.matrix.data = {}
	def get_matrix(self):
		return self.matrix
	def get_vector(self, word):
		return self.matrix.get_x(self.words.get_id(word))
	def save_matrix(self, filename):
		self.matrix.save(filename)
	def load_matrix(self, filename):
		self.matrix.load(filename)
class AutoEncoder(NeuralNetwork):
	def __init__(self, in_size, reduction_factor, lr=0.01):
		super().__init__(in_size, int(in_size//reduction_factor), in_size, lr)
	def train(self, input_data, epochs=300):
		super().train(input_data, input_data, epochs)
	def reduce(self, inputs):
		super().forward(inputs)
		return self.hidden_out
	def load(self, filename):
		super().load_model(filename)
	def save(self, filename):
		super().save_model(filename)
class Attention(NeuralNetwork):
	def __init__(self, emb_len, nwords=10, lr=0.01):
		super().__init__(emb_len*(nwords+1), emb_len*nwords, nwords, lr)
		self.embedding_size = emb_len
		self.context = nwords
	def train(self, train_data, epochs=300):
		questions = train_data["k"]
		keys = train_data["q"]
		outs = train_data["o"]
		inputs = []
		for i in range(len(keys)):
			inputs.append(self.process_input(questions[i], outs[i]))
		super().train(inputs, outs, epochs)
	def process_input(self, k, q):
		d = sum(q, [])
		k.extend(d)
		return  k
	def forward(self, k, q):
		inputs = self.process_input(k, q)
		return super().forward(inputs)
	def save(self, filename):
		super().save_model(filename)
	def load(self, filename):
		super().load_model(filename)
class PosEncoding:
	def __init__(self, max_pos=100):
		self.max_pos = max_pos
	def encode(self, encoded, pos):
		encoded.insert(1, pos/self.max_pos)
		return encoded
class MultiHeadAttention:
	def __init__(self, emb_len, num_heads=8, nwords=10, lr=0.01):
		self.emb_len = emb_len
		self.num_heads = num_heads
		self.context = nwords
		self.lr = lr
		self.heads = [Attention(emb_len, nwords, lr) for _ in range(num_heads)]
	#finnish MultiHeadAttention is important for the Model
	def select(self, querys, keys):
		out = []
		for i in range(self.num_heads):
			query = querys[i]
			head = self.heads[i]
			out.append(head.forward(query, keys))
		detout = [0]*len(out[0])
		for i in range(len(out)):
			for j in range(len(detout)):
				detout[j] += out[i][j]
		return detout
class TransformerEncoder:
	def __init__(self, emb_len, num_heads=8, nwords=10, lr=0.01):
		self.multi_head = MultiHeadAttention(emb_len, num_heads, nwords, lr)
		self.feed_forward = NeuralNetwork(emb_len, emb_len*2, emb_len)
		self.embeddings_size = emb_len
		self.num_heads = num_heads
		self.context = nwords
		self.lr = lr
	def forward(self, querys, keys):
		attn_out = self.multi_head.forward(querys, keys)
		norm1 = [[0]*len(attn_out) for _ in range(self.num_heads)]
		for i in range(self.num_heads):
			for j in range(len(attn_out)):
				norm1[i][j]
	#Finish Transformer Encoder
#I think that first i'm going to make a chatbot tha uses Attention Mechanism to choose a better answer of the predefined ones
class PreChatBot: #chatbot with attention mechanism
	def __init__(self, vfile, l_emb, nheads=1, tokens=10, lr=0.01): # when using coocurrencymatrix l_emb=len(vocab)
		self.vfile = vfile
		with open(self.vfile, "r") as f:
			self.vocab = json.load(f)
		self.len_embs = l_emb
		self.num_heads = nheads
		self.tokens = tokens
		self.lr = lr
		self.word_to_id = WordId()
		[self.word_to_id.get_id(i) for i in self.vocab]
		self.vectors = CooCurrencyMatrix(self.vocab)
		self.in_size = l_emb*nheads
		self.hidden_size = l_emb*nheads*2
		self.out_size = 1
		self.nn = NeuralNetwork(self.in_size, self.hidden_size, self.out_size, lr)
		self.attention = MultiHeadAttention(l_emb, nheads, tokens, lr)
	def build(self, corpus, i=False):
		self.vectors.build_matrix(corpus, i)
	def train_attention(self, train_data, epochs=300): #structure of train data → {"inputs":[[{"k":[], "q":[]}...]], "outs":[[], []....]}
		print("Starting Attention Training...")
		inputs = train_data["inputs"]
		outs = train_data["outs"]
		querys = [[0.0]*self.len_embs for _ in range(len(outs[0]))]
		for e in range(epochs):
			print("Epoch: " + str(e+1) + "/"+str(epochs))
			for i in range(len(outs)):
				for h in range(self.num_heads):
					data = {"k":querys, "q":inputs[h][i]["q"], "o":outs[i][h]}
					self.attention.heads[h].train(data, 1)
	def train_predicter(self, train_data, epochs=300):
		inputs = train_data["inputs"]
		outs = train_data["outs"]
		self.nn.train(inputs, outs, epochs)
	def train(self, at_data, pred_data, epochs=300):
		self.train_attention(at_data, epochs)
		self.train_predicter(pred_data, epochs)
		print("Training Finished")
	def predict_answer(self, question, null="<null>"):
		question.strip("¿")
		question.strip("?")
		question.strip("!")
		question.strip("¡")
		question.strip("-")
		question.strip(";")
		question.replace("á", "a")
		question.replace("ú", "u")
		question.replace("ó", "o")
		question.replace("é", "e")
		question.replace("í", "i")
		formatted = question.split(" ")
		len_r = len(rules)
		len_q = len(formatted)
		if len_q > self.tokens:
			return "Error, the question is too long"
		while len(formatted)<self.tokens:
			formatted.append(null)
		formatted = [self.word_to_id.get_id(word) for word in formatted]
		formatted = [self.matrix.get_x(ider) for ider in formatted]
		querys = [[0.0]*self.len_embs for _ in range(self.num_heads)]
		selected = self.attention.select(querys, formatted)
		selec = [formatted[h] for h in len(selected) if selected[h] > 0]
		lista_limpia = []
		for element in selected:
			if element != 0:
				lista_limpia.append(element)
		final = []
		pv = list(zip(lista_limpia, selec))
		pv.sort()
		final = [valor for _, valor in pv]
		id_respuesta = self.nn.forward(final)
		return int(id_respuesta)
	def save_model(self, filenames): # struct {"attention"["name1", "name2"....], "predicter":"name", "matrix":"name", "id":"name"}
		matrix = filenames["matrix"]
		neural = filenames["predicter"]
		id_f = filenames["id"]
		attention = filenames["attention"]
		self.word_to_id.save(id_f)
		self.vectors.save_matrix(matrix)
		self.nn.save_model(neural)
		for n in range(self.num_heads):
			self.attention.heads[n].save(attention[n])
	def load_model(self, filenames): # struct {"attention"["name1", "name2"....], "predicter":"name", "matrix":"name", "id":"name"}
		matrix = filenames["matrix"]
		neural = filenames["predicter"]
		id_f = filenames["id"]
		attention = filenames["attention"]
		self.word_to_id.load(id_f)
		self.vectors.load_matrix(matrix)
		self.nn.load_model(neural)
		for n in range(self.num_heads):
			self.attention.heads[n].load(attention[n])
class PreChatBotV2: #chatbot with attention mechanism
	def __init__(self, vfile, l_emb, embs, nheads=1, tokens=10, lr=0.01): # when using coocurrencymatrix l_emb=len(vocab)
		self.vfile = vfile
		with open(self.vfile, "r") as f:
			self.vocab = json.load(f)
		self.len_embs = l_emb
		self.num_heads = nheads
		self.tokens = tokens
		self.lr = lr
		self.word_to_id = WordId()
		[self.word_to_id.get_id(i) for i in self.vocab]
		with open(embs, "r") as f:
			self.ember = json.load(f)
		self.in_size = l_emb*nheads
		self.hidden_size = l_emb*nheads*2
		self.out_size = 1
		self.nn = NeuralNetwork(self.in_size, self.hidden_size, self.out_size, lr)
		self.attention = MultiHeadAttention(l_emb, nheads, tokens, lr)
	def build(self, corpus, i=False):
		self.vectors.build_matrix(corpus, i)
	def train_attention(self, train_data, epochs=300): #structure of train data → {"inputs":[[{"k":[], "q":[]}...]], "outs":[[], []....]}
		print("Starting Attention Training...")
		inputs = train_data["inputs"]
		outs = train_data["outs"]
		querys = [[0.0]*self.len_embs for _ in range(len(outs[0]))]
		for e in range(epochs):
			print("Epoch: " + str(e+1) + "/"+str(epochs))
			for i in range(len(outs)):
				for h in range(self.num_heads):
					data = {"k":querys, "q":inputs[h][i]["q"], "o":outs[i][h]}
					self.attention.heads[h].train(data, 1)
	def train_predicter(self, train_data, epochs=300):
		inputs = train_data["inputs"]
		outs = train_data["outs"]
		self.nn.train(inputs, outs, epochs)
	def train(self, at_data, pred_data, epochs=300):
		self.train_attention(at_data, epochs)
		self.train_predicter(pred_data, epochs)
		print("Training Finished")
	def predict_answer(self, question, null="<null>"):
		question.strip("¿")
		question.strip("?")
		question.strip("!")
		question.strip("¡")
		question.strip("-")
		question.strip(";")
		question.replace("á", "a")
		question.replace("ú", "u")
		question.replace("ó", "o")
		question.replace("é", "e")
		question.replace("í", "i")
		formatted = question.split(" ")
		len_r = len(rules)
		len_q = len(formatted)
		if len_q > self.tokens:
			return "Error, the question is too long"
		while len(formatted)<self.tokens:
			formatted.append(null)
		formatted = [self.word_to_id.get_id(word) for word in formatted]
		formatted = [self.ember[ider] for ider in formatted]
		querys = [[0.0]*self.len_embs for _ in range(self.num_heads)]
		selected = self.attention.select(querys, formatted)
		selec = [formatted[h] for h in len(selected) if selected[h] > 0]
		lista_limpia = []
		for element in selected:
			if element != 0:
				lista_limpia.append(element)
		final = []
		pv = list(zip(lista_limpia, selec))
		pv.sort()
		final = [valor for _, valor in pv]
		id_respuesta = self.nn.forward(final)
		return int(id_respuesta)
	def save_model(self, filenames): # struct {"attention"["name1", "name2"....], "predicter":"name", "matrix":"name", "id":"name"}
		neural = filenames["predicter"]
		id_f = filenames["id"]
		attention = filenames["attention"]
		self.word_to_id.save(id_f)
		self.nn.save_model(neural)
		for n in range(self.num_heads):
			self.attention.heads[n].save(attention[n])
	def load_model(self, filenames): # struct {"attention"["name1", "name2"....], "predicter":"name", "matrix":"name", "id":"name"}
		neural = filenames["predicter"]
		id_f = filenames["id"]
		attention = filenames["attention"]
		self.word_to_id.load(id_f)
		self.nn.load_model(neural)
		for n in range(self.num_heads):
			self.attention.heads[n].load(attention[n])
