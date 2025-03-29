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
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.decomposition import PCA
import json
import v2  # Asumiendo que 'v2' contiene tus clases WordVectorizer y WordId

# Cargar el vocabulario y el mapeo de palabras a IDs
with open("vocab.json", "r") as f:
    vocab = json.load(f)

word_ids = v2.models.WordId()
word_ids.load("word_ids.json")

# Crear una instancia de WordVectorizer
vectorizer = v2.WordVectorizer(vocab, word_ids)

# Cargar los pesos de las neuronas (si los guardaste)
with open("word_vectors.json", "r") as f:
    vectorizer.neurons = json.load(f)

words_100 = ["car", "road", "fish", "girl", "kid", "man", "woman", "wife", "cat", "dog", "pet", "mine"]

def reduce_to_3D(vectorizer, words):
    vectors = [vectorizer.get_vector(word) for word in words if word in vectorizer.vocab]
    vectors = [v for v in vectors if v is not None]

    pca = PCA(n_components=3)
    reduced = pca.fit_transform(vectors)

    # 🔹 Graficar en 3D
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    valid_words = [word for word in words if word in vectorizer.vocab and vectorizer.get_vector(word) is not None]

    for i, word in enumerate(valid_words):
        ax.scatter(reduced[i, 0], reduced[i, 1], reduced[i, 2])
        ax.text(reduced[i, 0], reduced[i, 1], reduced[i, 2], word, fontsize=12)

    ax.set_title("Embeddings en 3D (PCA)")
    ax.set_xlabel("Componente 1")
    ax.set_ylabel("Componente 2")
    ax.set_zlabel("Componente 3")
    plt.show()

# 🔹 Prueba con algunas palabras
reduce_to_3D(vectorizer, words_100)
