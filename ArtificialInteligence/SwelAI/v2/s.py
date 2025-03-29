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
import numpy as np
import random
from nltk.corpus import brown
import json

# 🔹 Red Neuronal con backpropagation
class NeuralNetwork:
    def __init__(self, in_layer, hidden_layer, out_layer, lr=0.01):
        self.hidden_w = np.random.uniform(-0.5, 0.5, (hidden_layer, in_layer))
        self.out_w = np.random.uniform(-0.5, 0.5, (out_layer, hidden_layer))
        self.lr = lr

    def relu(self, x):
        return np.maximum(0, x)

    def relud(self, x):
        return (x > 0).astype(float)

    def forward(self, inputs):
        hidden_out = self.relu(np.dot(self.hidden_w, inputs))
        out_out = self.relu(np.dot(self.out_w, hidden_out))
        return out_out

    def backward(self, expected, inputs):
        out_error = (expected - self.forward(inputs)) * self.relud(self.forward(inputs))
        hidden_error = np.dot(self.out_w.T, out_error) * self.relud(self.forward(inputs))

        self.out_w += self.lr * np.outer(out_error, self.forward(inputs))
        self.hidden_w += self.lr * np.outer(hidden_error, inputs)

    def train(self, input_data, out_data, epochs=300):
        for _ in range(epochs):
            for i in range(len(input_data)):
                self.forward(input_data[i])
                self.backward(out_data[i], input_data[i])

# 🔹 Matriz de Coocurrencia
class CooCurrencyMatrix:
    def __init__(self, vocab, context_window=5):
        self.vocab = vocab
        self.context_window = context_window
        self.matrix = {word: np.zeros(len(vocab)) for word in vocab}
        self.word_to_id = {word: i for i, word in enumerate(vocab)}

    def build_matrix(self, corpus):
        for sentence in corpus:
            for i, word in enumerate(sentence):
                if word not in self.vocab:
                    continue
                word_id = self.word_to_id[word]
                for j in range(max(0, i - self.context_window), min(len(sentence), i + self.context_window + 1)):
                    if i != j and sentence[j] in self.vocab:
                        context_id = self.word_to_id[sentence[j]]
                        self.matrix[word][context_id] += 1

    def get_vector(self, word):
        return self.matrix.get(word, np.zeros(len(self.vocab)))

# 🔹 Multi-Head Attention
class MultiHeadAttention:
    def __init__(self, emb_len, num_heads=8):
        self.num_heads = num_heads
        self.attention_heads = [NeuralNetwork(emb_len, emb_len * 2, emb_len) for _ in range(num_heads)]

    def forward(self, k, q):
        outputs = np.array([head.forward(q) for head in self.attention_heads])
        return np.mean(outputs, axis=0)

# 🔹 Transformer Encoder
class TransformerEncoder:
    def __init__(self, emb_len, num_heads=8):
        self.multi_head_attention = MultiHeadAttention(emb_len, num_heads)
        self.feed_forward = NeuralNetwork(emb_len, emb_len * 2, emb_len)

    def forward(self, k, q):
        attn_output = self.multi_head_attention.forward(k, q)
        norm1 = (q + attn_output) / 2
        ff_output = self.feed_forward.forward(norm1)
        return (norm1 + ff_output) / 2

# 🔹 Transformer Completo
class Transformer:
    def __init__(self, emb_len, num_layers=6, num_heads=8):
        self.encoders = [TransformerEncoder(emb_len, num_heads) for _ in range(num_layers)]

    def forward(self, k, q):
        for encoder in self.encoders:
            q = encoder.forward(k, q)
        return q

# 🔹 Softmax y Top-K Sampling
def softmax(x, temperature=1.0):
    x = np.array(x) / temperature
    exp_x = np.exp(x - np.max(x))
    return exp_x / np.sum(exp_x)

def top_k_sampling(probs, k=5, diversity_factor=0.1):
    sorted_indices = np.argsort(probs)[::-1]  # Ordenamos de mayor a menor
    top_k_indices = sorted_indices[:k]  # Tomamos las `k` mejores opciones
    top_k_probs = probs[top_k_indices] / np.sum(probs[top_k_indices])  # Normalizamos

    # 🔹 Introducimos aleatoriedad en la selección con `diversity_factor`
    top_k_probs = (top_k_probs + diversity_factor) / np.sum(top_k_probs + diversity_factor)

    return np.random.choice(top_k_indices, p=top_k_probs)

# 🔹 Generador de Texto con Embeddings de Coocurrencia
class TextGenerator:
    def __init__(self, transformer, vocab, cooc_matrix):
        self.transformer = transformer
        self.vocab = vocab
        self.cooc_matrix = cooc_matrix
        self.word_to_id = {word: i for i, word in enumerate(vocab)}
        self.id_to_word = {i: word for i, word in enumerate(vocab)}

    def generate(self, seed_text, max_length=20, temperature=0.8, top_k=5):
        generated_text = seed_text.split()
        for i in range(max_length):
            context_words = generated_text[-10:]
            context_vectors = [self.cooc_matrix.get_vector(word) for word in context_words]
            query_vector = self.cooc_matrix.get_vector(generated_text[-1])

            output = self.transformer.forward(context_vectors, query_vector)
            probs = softmax(output, temperature)
            next_word_id = top_k_sampling(probs, top_k)
            next_word = self.id_to_word.get(next_word_id, "UNKNOWN")

            generated_text.append(next_word)

        return " ".join(generated_text)

# 🔹 Cargar vocabulario del corpus Brown
vocab = list(set(word.lower() for word in brown.words()[:5000] if word.isalpha()))

# 🔹 Crear matriz de coocurrencia
cooc_matrix = CooCurrencyMatrix(vocab, context_window=5)
cooc_matrix.build_matrix(brown.sents())

# 🔹 Crear el Transformer y Generador de Texto
transformer = Transformer(emb_len=len(vocab))

# 🔹 Generar texto con una semilla inicial
# 🔹 Implementación del chatbot generativo usando tu código

class Chatbot:
    def __init__(self, transformer, vocab, cooc_matrix):
        self.transformer = transformer
        self.vocab = vocab
        self.cooc_matrix = cooc_matrix
        self.word_to_id = {word: i for i, word in enumerate(vocab)}
        self.id_to_word = {i: word for i, word in enumerate(vocab)}

    def preprocess(self, text):
        """ Convierte el texto de entrada en tokens válidos """
        words = text.lower().split()
        return [word for word in words if word in self.vocab]

    def respond(self, user_input, max_length=20, temperature=0.8, top_k=5):
        context_words = self.preprocess(user_input)
        if not context_words:
            return "I don't understand."

        # 🔹 Obtener vectores de contexto
        context_vectors = [self.cooc_matrix.get_vector(word) for word in context_words]
        
        # 🔹 Crear una consulta para predecir la siguiente palabra
        query_vector = self.cooc_matrix.get_vector(context_words[-1]) + np.random.rand(len(self.vocab)) * 0.01

        # 🔹 Generar respuesta con el Transformer
        output = self.transformer.forward(context_vectors, query_vector)
        probs = softmax(output, temperature)
        next_word_id = top_k_sampling(probs, top_k, diversity_factor=0.05)
        next_word = self.id_to_word.get(next_word_id, "UNKNOWN")

        return f"{user_input} {next_word}"
# 🔹 Chatbot Generativo con `SingleAttention`
class GenerativeChatbot:
    def __init__(self, attention, vocab, cooc_matrix):
        self.attention = attention
        self.vocab = vocab
        self.cooc_matrix = cooc_matrix
        self.word_to_id = {word: i for i, word in enumerate(vocab)}
        self.id_to_word = {i: word for i, word in enumerate(vocab)}

    def preprocess(self, text):
        """ Convierte el texto en tokens válidos """
        words = text.lower().split()
        return [word for word in words if word in self.vocab]

    def generate_response(self, user_input, max_length=20, temperature=0.8, top_k=5):
        """ Genera una respuesta completa en lugar de una sola palabra """
        context_words = self.preprocess(user_input)
        if not context_words:
            return "I don't understand."

        response = context_words.copy()  # 🔹 Comenzamos con la entrada del usuario
        generated_words = set(response)  # 🔹 Para evitar repeticiones

        for _ in range(max_length):
            context_vectors = [self.cooc_matrix.get_vector(word) for word in response[-10:]]
            query_vector = self.cooc_matrix.get_vector(response[-1]) + np.random.rand(len(self.vocab)) * 0.01

            output = self.attention.forward(context_vectors, query_vector)
            probs = softmax(output, temperature)
            next_word_id = top_k_sampling(probs, top_k, diversity_factor=0.05)
            next_word = self.id_to_word.get(next_word_id, "UNKNOWN")

            # 🔹 Si la palabra ya fue generada antes, reducimos su probabilidad
            if next_word in generated_words:
                temperature *= 1.1  # 🔥 Aumentamos la temperatura para mayor aleatoriedad
                continue

            generated_words.add(next_word)
            response.append(next_word)

            # 🔹 Terminamos si la frase parece completa (detectar signos de puntuación o verbos clave)
            if next_word in [".", "!", "?", "thank", "bye"]:
                break

        return " ".join(response)

# 🔹 Entrenamiento del chatbot con datos de conversación

class TrainableChatbot(GenerativeChatbot):
    def __init__(self, attention, vocab, cooc_matrix):
        super().__init__(attention, vocab, cooc_matrix)

    def train(self, conversation_pairs, epochs=300):
        """ Entrena el modelo usando pares de conversación """
        for epoch in range(epochs):
            print(f"Epoch {epoch+1}/{epochs}...")
            for question, answer in conversation_pairs:
                q_tokens = self.preprocess(question)
                a_tokens = self.preprocess(answer)
                if not q_tokens or not a_tokens:
                    continue

                # 🔹 Obtener vectores de contexto y salida esperada
                context_vectors = [self.cooc_matrix.get_vector(word) for word in q_tokens]
                query_vector = self.cooc_matrix.get_vector(q_tokens[-1])  # 🔹 Ahora se pasa `q` correctamente
                expected_output = np.mean([self.cooc_matrix.get_vector(word) for word in a_tokens], axis=0)

                # 🔹 Forward y Backpropagation
                output = self.attention.forward(query_vector)  # 🔥 Ahora forward() tiene `q`
                self.attention.backward(expected_output, query_vector)  # 🔥 Backward ahora usa `query_vector`

        print("🔹 Entrenamiento completado.")
class SingleAttention(NeuralNetwork):
    """ Implementación de una única cabeza de atención """
    def __init__(self, emb_len, lr=0.01):
        super().__init__(emb_len, emb_len * 2, emb_len, lr)

    def forward(self, q):
        """ Procesa la atención con una sola cabeza """
        return super().forward(q)  # 🔹 Solo se usa `q`, sin combinaciones múltiple



# 🔹 Dataset de entrenamiento (Ejemplo con frases simples)
conversation_data = [
    ("hello", "hi there"),
    ("how are you", "I'm fine, thanks"),
    ("what's your name", "I'm a chatbot"),
    ("tell me a joke", "Why did the chicken cross the road?"),
    ("bye", "Goodbye! Have a great day!")
]
single_attention = SingleAttention(emb_len=len(vocab))
# 🔹 Crear y entrenar el chatbot
trainable_chatbot = TrainableChatbot(single_attention, vocab, cooc_matrix)
trainable_chatbot.train(conversation_data, epochs=500)

# 🔹 Probar el chatbot después del entrenamiento
while True:
	user_input = input("Ask: ")
	response = trainable_chatbot.generate_response(user_input)
	print("Chatbot:", response)




