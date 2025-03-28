import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# Definición de la función compuesta
def f(x):
    return np.sin(2 * x) + np.sin(10 * x)

# Intervalo de tiempo
x = np.linspace(0, 10, 1000)
y = f(x)

# Encontrar los picos en la función
peaks, _ = find_peaks(y)

# Calcular todas las distancias entre picos
distances = np.diff(x[peaks])

# Gráfica de la función compuesta y los picos
plt.figure(figsize=(12, 8))

# Gráfica de la función compuesta
plt.subplot(2, 1, 1)
plt.plot(x, y, label='f(x) = sin(2x) + sin(10x)', color='b')
plt.plot(x[peaks], y[peaks], "x", label='Picos', color='r')
plt.title('Función Compuesta f(x) y Picos')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.grid()
plt.legend()

# Gráfica de las distancias entre picos
plt.subplot(2, 1, 2)
plt.plot(peaks[1:], distances, label='Distancias entre Picos', color='g', marker='o')
plt.title('Distancias entre Picos')
plt.xlabel('Índice de Pico')
plt.ylabel('Distancia')
plt.grid()
plt.legend()

plt.tight_layout()
plt.show()

# Imprimir distancias entre picos
print("Distancias entre picos:", distances)
