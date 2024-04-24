import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from algorithm import genetic_algorithm
import sympy as sp
import os
import moviepy.editor as mpy
from natsort import natsorted
from tkinter.ttk import Treeview



def evaluate_function(func, values):
    x = sp.symbols("x")
    results = np.array([])
    for value in values:
        expression = sp.sympify(func)
        result = expression.subs(x, value)
        results = np.append(results, result)

    return results


def generate_video():
    images = natsorted(
        [
            os.path.join("graphs", fn)
            for fn in os.listdir("graphs")
            if fn.endswith((".png", ".jpg", ".jpeg"))
        ]
    )
    video = mpy.ImageSequenceClip(images, fps=1)
    video.write_videofile("graphs/video.mp4")


def plot_function(
    usage_1,
    usage_2,
    generations,
    initial_population,
    max_population,
    crossover_probability,
    individual_mutation_probability,
    gen_mutation_probability,
    minimize,
):
    statistics, population = genetic_algorithm(
        usage_1,
        usage_2,
        generations,
        initial_population,
        max_population,
        crossover_probability,
        individual_mutation_probability,
        gen_mutation_probability,
        minimize,
    )
    statistics = np.array(statistics)

    for widget in frame_plot.winfo_children():
        widget.destroy()

    try:
        fig, ax = plt.subplots(figsize=(6, 4))
        plt.grid(True)
        ax.set_title("Aptitud")
        ax.set_xlabel("Generación")
        ax.set_ylabel("Fitness")

        generations = np.arange(0, generations + 1, 1)
        best = np.array([])
        worst = np.array([])
        average = np.array([])

        for i in range(len(statistics)):
            best = np.append(best, statistics[i]["best"][1])
            worst = np.append(worst, statistics[i]["worst"][1])
            average = np.append(average, statistics[i]["average"])

        ax.plot(generations, best, label="Mejor", color="blue")
        ax.plot(generations, average, label="Promedio", color="green")
        ax.plot(generations, worst, label="Peor", color="red")

        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=frame_plot)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    except Exception as e:
        print("Error al graficar la función:", e)

    result_frame = tk.LabelFrame(frame_plot, text="Parámetros")

    result_label = tk.Label(result_frame, text="Mejor individuo: ")
    result_label.pack()

    columns = ["Lenguaje", "Uso 1", "Uso 2", "Dificultad"]
    tree = Treeview(result_frame, columns=columns, show="headings")

    tree.heading("Lenguaje", text="Lenguaje")
    tree.heading("Uso 1", text="Uso 1")
    tree.heading("Uso 2", text="Uso 2")
    tree.heading("Dificultad", text="Dificultad")

    for lang in population[0][0]:
        print(lang)
        tree.insert("", "end", values=(lang[1], lang[usage_1], lang[usage_2], lang[11]))

    for col in columns:
        tree.column(col, anchor="center")

    tree.pack()

    result_frame.pack()
    plt.show()


window = tk.Tk()
window.title("Algoritmo Genético Lenguajes de Programación")
window.geometry("1200x720")
window.resizable(False, False)

left_frame = tk.Frame(window)
left_frame.pack(side=tk.LEFT, padx=10)

frame1 = tk.LabelFrame(left_frame, text="Parámetros")
frame1.grid(row=0, column=0, padx=20, pady=30, sticky="ew")

usage_1_label = tk.Label(frame1, text="Usos:")
usage_1_label.grid(row=1, column=0, sticky="w")

usage_1 = tk.StringVar()
usage_1.set("artificial_intelligence")
usage_1_entry = tk.OptionMenu(
    frame1,
    usage_1,
    "artificial_intelligence",
    "machine_learning",
    "data_science",
    "web_dev",
    "enterprise_dev",
    "mobile_dev",
    "game_dev",
    "embedded_system",
    "virtual_reality",
)
usage_1_entry.grid(row=2, column=0, padx=10, sticky="w")

usage_2 = tk.StringVar()
usage_2.set("machine_learning")
usage_2_entry = tk.OptionMenu(
    frame1,
    usage_2,
    "artificial_intelligence",
    "machine_learning",
    "data_science",
    "web_dev",
    "enterprise_dev",
    "mobile_dev",
    "game_dev",
    "embedded_system",
    "virtual_reality",
)
usage_2_entry.grid(row=2, column=1, padx=10, sticky="w")

generations_label = tk.Label(frame1, text="Numero de generaciones:")
generations_label.grid(row=4, column=0, sticky="w")
generations_entry = tk.Entry(frame1)
generations_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")
generations_entry.insert(0, "20")

initial_population_label = tk.Label(frame1, text="Poblacion inicial:")
initial_population_label.grid(row=5, column=0, sticky="w")
initial_population_entry = tk.Entry(frame1)
initial_population_entry.grid(row=5, column=1, padx=10, pady=10, sticky="w")
initial_population_entry.insert(0, "4")

max_population_label = tk.Label(frame1, text="Poblacion maxima:")
max_population_label.grid(row=6, column=0, sticky="w")
max_population_entry = tk.Entry(frame1)
max_population_entry.grid(row=6, column=1, padx=10, pady=10, sticky="w")
max_population_entry.insert(0, "10")

crossover_prob_label = tk.Label(frame1, text="Probabilidad de cruza:")
crossover_prob_label.grid(row=7, column=0, sticky="w")
crossover_prob_entry = tk.Entry(frame1)
crossover_prob_entry.grid(row=7, column=1, padx=10, pady=10, sticky="w")
crossover_prob_entry.insert(0, "0.5")

mutation_prob_label = tk.Label(frame1, text="Probabilidad de mutación:")
mutation_prob_label.grid(row=8, column=0, sticky="w")
mutation_prob_entry = tk.Entry(frame1)
mutation_prob_entry.grid(row=8, column=1, padx=10, pady=10, sticky="w")
mutation_prob_entry.insert(0, "0.5")

mutation_per_gene_prob_label = tk.Label(
    frame1, text="Probabilidad de mutación por Gen:"
)
mutation_per_gene_prob_label.grid(row=9, column=0, sticky="w")
mutation_per_gene_prob_entry = tk.Entry(frame1)
mutation_per_gene_prob_entry.grid(row=9, column=1, padx=10, pady=10, sticky="w")
mutation_per_gene_prob_entry.insert(0, "0.5")

method_label = tk.Label(frame1, text="Metodo:")
method_label.grid(row=10, column=0, sticky="w")
method = tk.StringVar()
method.set("Maximizar")
method_menu = tk.OptionMenu(frame1, method, "Minimizar", "Maximizar")
method_menu.grid(row=10, column=1, padx=10, sticky="w")


def execute():
    def map_usage(usage):
        usages = [
            "artificial_intelligence",
            "machine_learning",
            "data_science",
            "web_dev",
            "enterprise_dev",
            "mobile_dev",
            "game_dev",
            "embedded_system",
            "virtual_reality",
        ]
        return usages.index(usage) + 2
    usage_1_s = map_usage(usage_1.get())
    usage_2_s = map_usage(usage_2.get())

    generations = int(generations_entry.get())
    initial_population = int(initial_population_entry.get())
    max_population = int(max_population_entry.get())
    crossover_probability = float(crossover_prob_entry.get())
    individual_mutation_probability = float(mutation_prob_entry.get())
    gen_mutation_probability = float(mutation_per_gene_prob_entry.get())
    minimize = method.get() == "Minimizar"

    plot_function(
        usage_1_s,
        usage_2_s,
        generations,
        initial_population,
        max_population,
        crossover_probability,
        individual_mutation_probability,
        gen_mutation_probability,
        minimize,
    )


execute_button = tk.Button(frame1, text="Ejecutar", command=execute)
execute_button.grid(row=11, column=0, padx=10, pady=10, sticky="w")

right_frame = tk.Frame(window)
right_frame.pack(side=tk.RIGHT, padx=10)

frame_plot = tk.Frame(right_frame)
frame_plot.pack()

window.mainloop()
