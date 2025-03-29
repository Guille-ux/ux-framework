import tkinter as tk
from tkinter import messagebox
import threading
import os

root = tk.Tk()
root.title("Voice Synthesizer")
root.geometry("600x400")  # Reducir un poco la ventana

canvas = tk.Canvas(root, width=600, height=400, bg="#f0f0f0")  # Fondo más claro
canvas.pack(fill=tk.BOTH, expand=True)  # Hacer que el canvas se expanda


filename = "script.txt"

def synther():
    canvas.itemconfig(status_text_id, text="Synthesizing...", fill="blue")
    texto_a_sintetizar = text_entry.get()
    print(f"[*] Synthesizing Text: {texto_a_sintetizar} [*]")
    with open(filename, "w") as f:
        f.write(texto_a_sintetizar)
    print(f"[*] Text Written to script.txt [*]")
    thread = threading.Thread(target=do, args=(status_text_id,), daemon=True)
    thread.start()

def do(status_text_id):
    try:
        os.system("python3 main.py script.txt 1 out")
        canvas.itemconfig(status_text_id, text="Synthesis Successful!", fill="green")
        messagebox.showinfo("Success", "The file was synthesized at exports/")
    except Exception as e:
        canvas.itemconfig(status_text_id, text=f"Error: {e}", fill="red")
        messagebox.showerror("Error", f"There was a problem synthesizing: {e}")


# Título
title_label = canvas.create_text(
    300, 50,  # Centrar horizontalmente, bajar un poco
    text="Voice Synthesizer",
    fill="#333",  # Texto más oscuro
    font=("Arial", 24, "bold")
)

# Etiqueta para la entrada de texto
text_label = canvas.create_text(
    100, 150,  # Posicionar más arriba
    text="Enter text to synthesize:",
    fill="#555",
    anchor=tk.W,
    font=("Arial", 12)
)

# Campo de entrada de texto
text_entry = tk.Entry(canvas, font=("Arial", 12))
canvas.create_window(
    300, 180,  # Centrar horizontalmente, debajo de la etiqueta
    window=text_entry,
    width=400,
    height=30
)

# Botón de sintetizar
submit_button = tk.Button(
    canvas,
    text="Synthesize",
    command=synther,
    bg="#4CAF50",  # Verde atractivo
    fg="white",
    padx=20,
    pady=10,
    font=("Arial", 12, "bold"),
    relief=tk.RAISED,
    borderwidth=2
)
canvas.create_window(
    300, 250,  # Centrar horizontalmente, debajo del campo de texto
    window=submit_button
)

# Etiqueta para mostrar el estado de sintetización
status_text_id = canvas.create_text(
    300, 320,  # Centrar horizontalmente, debajo del botón
    text="",
    fill="blue",
    font=("Arial", 11)
)

filename = "script.txt"

def synther():
    canvas.itemconfig(status_text_id, text="Synthesizing...", fill="blue")
    texto_a_sintetizar = text_entry.get()
    print(f"[*] Synthesizing Text: {texto_a_sintetizar} [*]")
    with open(filename, "w") as f:
        f.write(texto_a_sintetizar)
    print(f"[*] Text Written to script.txt [*]")
    thread = threading.Thread(target=do, args=(status_text_id,), daemon=True)
    thread.start()

def do(status_text_id):
    try:
        os.system("python3 main.py script.txt 2 out")
        canvas.itemconfig(status_text_id, text="Synthesis Successful!", fill="green")
        messagebox.showinfo("Success", "The file was synthesized at exports/")
    except Exception as e:
        canvas.itemconfig(status_text_id, text=f"Error: {e}", fill="red")
        messagebox.showerror("Error", f"There was a problem synthesizing: {e}")

root.mainloop()
import tkinter as tk
from tkinter import messagebox
import threading
import os

root = tk.Tk()
root.title("Voice Synthesizer")
root.geometry("600x400")  # Reducir un poco la ventana

canvas = tk.Canvas(root, width=600, height=400, bg="#f0f0f0")  # Fondo más claro
canvas.pack(fill=tk.BOTH, expand=True)  # Hacer que el canvas se expanda

# Título
title_label = canvas.create_text(
    300, 50,  # Centrar horizontalmente, bajar un poco
    text="Voice Synthesizer",
    fill="#333",  # Texto más oscuro
    font=("Arial", 24, "bold")
)

# Etiqueta para la entrada de texto
text_label = canvas.create_text(
    100, 150,  # Posicionar más arriba
    text="Enter text to synthesize:",
    fill="#555",
    anchor=tk.W,
    font=("Arial", 12)
)

# Campo de entrada de texto
text_entry = tk.Entry(canvas, font=("Arial", 12))
canvas.create_window(
    300, 180,  # Centrar horizontalmente, debajo de la etiqueta
    window=text_entry,
    width=400,
    height=30
)

# Botón de sintetizar
submit_button = tk.Button(
    canvas,
    text="Synthesize",
    command=synther,
    bg="#4CAF50",  # Verde atractivo
    fg="white",
    padx=20,
    pady=10,
    font=("Arial", 12, "bold"),
    relief=tk.RAISED,
    borderwidth=2
)
canvas.create_window(
    300, 250,  # Centrar horizontalmente, debajo del campo de texto
    window=submit_button
)

# Etiqueta para mostrar el estado de sintetización
status_text_id = canvas.create_text(
    300, 320,  # Centrar horizontalmente, debajo del botón
    text="",
    fill="blue",
    font=("Arial", 11)
)

root.mainloop()
