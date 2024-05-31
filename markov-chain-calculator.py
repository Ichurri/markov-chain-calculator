import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np


class MarkovChainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Investigacion Operativa II : Cadenas de Markov")
        self.geometry("700x600")
        self.create_widgets()
        self.configure_grid()

    def configure_grid(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def create_widgets(self):
        # Create frames for better layout
        title_frame = tk.Frame(self)
        title_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        input_frame = tk.Frame(self)
        input_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        matrix_frame = tk.Frame(self)
        matrix_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        button_frame = tk.Frame(self)
        button_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        result_frame = tk.Frame(self)
        result_frame.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

        # Configure grid weights for frames
        for i in range(5):
            self.grid_rowconfigure(i, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Font configuration
        default_font = ("Arial", 12)
        title_font = ("Arial", 14, "bold")

        # Title
        tk.Label(title_frame, text="Cálculo de Cadenas de Markov", font=title_font).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        title_frame.grid_columnconfigure(0, weight=1)

        # Input for number of states
        tk.Label(input_frame, text="Número de estados:", font=default_font).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.num_states_entry = tk.Entry(input_frame, font=default_font)
        self.num_states_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.set_matrix_button = tk.Button(input_frame, text="Establecer Matriz", command=self.set_matrix, font=default_font)
        self.set_matrix_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        # Input for number of steps
        tk.Label(input_frame, text="Número de etapas (n):", font=default_font).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.num_steps_entry = tk.Entry(input_frame, font=default_font)
        self.num_steps_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Configure grid weights for input frame
        input_frame.grid_columnconfigure(1, weight=1)

        # Matrix input frame
        self.matrix_frame = matrix_frame
        matrix_frame.grid_rowconfigure(0, weight=1)
        matrix_frame.grid_columnconfigure(0, weight=1)

        # Calculate button
        self.calculate_button = tk.Button(button_frame, text="Calcular", command=self.calculate, font=title_font)
        self.calculate_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Centering the button_frame
        button_frame.grid_columnconfigure(0, weight=1)

        # Result display
        self.results = tk.Text(result_frame, height=20, width=80, font=default_font)
        self.results.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        result_frame.grid_rowconfigure(0, weight=1)
        result_frame.grid_columnconfigure(0, weight=1)

    def set_matrix(self):
        num_states = int(self.num_states_entry.get())
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()

        self.matrix_entries = []
        for i in range(num_states):
            row_entries = []
            for j in range(num_states):
                entry = tk.Entry(self.matrix_frame, width=5, font=("Arial", 10))
                entry.grid(row=i, column=j, padx=5, pady=5, sticky="ew")
                row_entries.append(entry)
            self.matrix_entries.append(row_entries)

        for i in range(num_states):
            self.matrix_frame.grid_rowconfigure(i, weight=1)
            self.matrix_frame.grid_columnconfigure(i, weight=1)

    def calculate(self):
        try:
            matrix = np.array([[float(entry.get()) for entry in row] for row in self.matrix_entries])
            if not self.validate_matrix(matrix):
                messagebox.showerror("Error", "La suma de las filas debe ser 1.")
                return

            num_steps = int(self.num_steps_entry.get())

            steady_state_matrix, steady_state_vector = self.markov_chain(matrix)
            n_step_probabilities = self.n_step_probabilities(matrix, num_steps)
            steady_state_probabilities = self.steady_state_probabilities(matrix)

            #result_text = "Matriz de transición de estado estacionario:\n"
            #result_text += np.array2string(steady_state_matrix, precision=2, separator=',')
            result_text = "Vector de distribución de probabilidad:\n"
            result_text += np.array2string(steady_state_vector, precision=2, separator=',')
            result_text += f"\n\nProbabilidades de estado en la etapa {num_steps}:\n"
            result_text += np.array2string(n_step_probabilities, precision=2, separator=',')
            result_text += "\n\nProbabilidades de estado estable (π):\n"
            result_text += np.array2string(steady_state_probabilities, precision=2, separator=',')

            self.results.delete("1.0", tk.END)
            self.results.insert(tk.END, result_text)
        except ValueError:
            messagebox.showerror("Error", "Todos los valores en la matriz deben ser números.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def validate_matrix(self, matrix):
        return np.allclose(matrix.sum(axis=1), 1)

    def markov_chain(self, matrix):
        n = len(matrix)
        q = np.zeros_like(matrix)
        q[:-1, :-1] = matrix[:-1, :-1]
        q[:-1, -1] = 1 - q[:-1, :-1].sum(axis=1)
        q[-1, -1] = 1

        eigvals, eigvecs = np.linalg.eig(q.T)
        stationary = eigvecs[:, np.isclose(eigvals, 1)]
        stationary = stationary[:, 0]
        stationary = stationary / stationary.sum()

        return q, stationary

    def n_step_probabilities(self, matrix, n):
        prob_matrix = np.linalg.matrix_power(matrix, n)
        return prob_matrix

    def steady_state_probabilities(self, matrix):
        n = len(matrix)
        A = np.vstack([matrix.T - np.eye(n), np.ones(n)])
        b = np.zeros(n + 1)
        b[-1] = 1
        steady_state_vector = np.linalg.lstsq(A, b, rcond=None)[0]
        return steady_state_vector


if __name__ == "__main__":
    app = MarkovChainApp()
    app.mainloop()
