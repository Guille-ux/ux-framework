import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from matplotlib.widgets import TextBox

# Función para calcular la integral acumulada
def integral_acumulada(func, x_vals):
    integral_vals = np.zeros_like(x_vals)
    for i, x in enumerate(x_vals):
        integral_vals[i], _ = quad(func, x_vals[0], x)
    return integral_vals

# Función para actualizar el gráfico
def actualizar_grafico(val):
    try:
        # Obtener los valores de los límites de integración
        a = float(textbox_a.text)
        b = float(textbox_b.text)

        # Obtener la función definida por el usuario
        func_text = textbox_func.text

        # Crear la función dinámica a partir del texto ingresado
        def f(x):
            return eval(func_text)

        # Limpiar los gráficos anteriores
        ax_func.cla()
        ax_integral.cla()

        # Graficar la función en el intervalo [a, b]
        x = np.linspace(a, b, 1000)
        y = f(x)
        ax_func.plot(x, y, label=f'f(x) = {func_text}', color='blue')
        ax_func.set_title(f'Función: f(x) = {func_text}')
        ax_func.legend()

        # Calcular y graficar la integral acumulada
        integral_vals = integral_acumulada(f, x)
        ax_integral.plot(x, integral_vals, label=f'Integral acumulada de f(x)', color='green')
        ax_integral.set_title('Integral acumulada')
        ax_integral.legend()

        # Redibujar las gráficas
        plt.draw()
    except Exception as e:
        print(f"Error: {e}. Asegúrate de que la función y los límites sean correctos.")

# Crear la figura con dos gráficos
fig, (ax_func, ax_integral) = plt.subplots(2, 1, figsize=(6, 8))
plt.subplots_adjust(bottom=0.4)

# Crear las cajas de texto para los límites de integración y la función
axbox_func = plt.axes([0.2, 0.25, 0.6, 0.075])  # Caja para la función
axbox_a = plt.axes([0.2, 0.1, 0.2, 0.075])      # Caja para el límite inferior
axbox_b = plt.axes([0.6, 0.1, 0.2, 0.075])      # Caja para el límite superior
textbox_func = TextBox(axbox_func, 'Función f(x)', initial="np.sin(x)")
textbox_a = TextBox(axbox_a, 'Límite inferior', initial="0")
textbox_b = TextBox(axbox_b, 'Límite superior', initial="np.pi")

# Conectar las cajas de texto con la función de actualización
textbox_func.on_submit(actualizar_grafico)
textbox_a.on_submit(actualizar_grafico)
textbox_b.on_submit(actualizar_grafico)

# Mostrar el gráfico inicial con los valores por defecto
actualizar_grafico(None)

# Mostrar la interfaz
plt.show()
