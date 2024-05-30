import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np


class QueueModelsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Modelos de Línea de Espera")
        self.geometry("700x600")
        self.create_widgets()
        self.configure_grid()

    def configure_grid(self):
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def create_widgets(self):
        # Create frames for better layout
        input_frame = tk.Frame(self)
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        model_frame = tk.Frame(self)
        model_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        button_frame = tk.Frame(self)
        button_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        result_frame = tk.Frame(self)
        result_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        # Configure grid weights for frames
        for i in range(4):
            self.grid_rowconfigure(i, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Font configuration
        default_font = ("Arial", 12)
        title_font = ("Arial", 14, "bold")

        # Input for number of states
        tk.Label(input_frame, text="Tasa de llegada (λ):", font=default_font).grid(row=0, column=0, padx=5, pady=5,
                                                                                   sticky="e")
        self.lambda_entry = tk.Entry(input_frame, font=default_font)
        self.lambda_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(input_frame, text="Tasa de servicio (μ):", font=default_font).grid(row=1, column=0, padx=5, pady=5,
                                                                                    sticky="e")
        self.mu_entry = tk.Entry(input_frame, font=default_font)
        self.mu_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(input_frame, text="Número de servidores (k):", font=default_font).grid(row=2, column=0, padx=5, pady=5,
                                                                                        sticky="e")
        self.k_entry = tk.Entry(input_frame, font=default_font)
        self.k_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(input_frame, text="Población total (N):", font=default_font).grid(row=3, column=0, padx=5, pady=5,
                                                                                   sticky="e")
        self.N_entry = tk.Entry(input_frame, font=default_font)
        self.N_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Configure grid weights for input frame
        input_frame.grid_columnconfigure(1, weight=1)

        # Model selection
        tk.Label(model_frame, text="Seleccione el modelo:", font=default_font).grid(row=0, column=0, padx=5, pady=5,
                                                                                    sticky="w")
        self.model_var = tk.StringVar()
        models = ["M/M/1", "M/M/k", "M/G/1", "M/D/1", "M/G/k (clientes bloqueados eliminados)",
                  "M/M/1 (fuente finita)", "M/M/k (fuente finita)"]
        self.model_menu = ttk.Combobox(model_frame, textvariable=self.model_var, values=models, font=default_font)
        self.model_menu.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

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

    def calculate(self):
        try:
            lambda_rate = float(self.lambda_entry.get())
            mu_rate = float(self.mu_entry.get())
            k = int(self.k_entry.get()) if self.k_entry.get() else None
            N = int(self.N_entry.get()) if self.N_entry.get() else None
            model = self.model_var.get()

            if model == "M/M/1":
                result = self.mm1(lambda_rate, mu_rate)
            elif model == "M/M/k":
                result = self.mmk(lambda_rate, mu_rate, k)
            elif model == "M/G/1":
                result = self.mg1(lambda_rate, mu_rate)
            elif model == "M/D/1":
                result = self.md1(lambda_rate, mu_rate)
            elif model == "M/G/k (clientes bloqueados eliminados)":
                result = self.mgk_blocked(lambda_rate, mu_rate, k)
            elif model == "M/M/1 (fuente finita)":
                result = self.mm1_finite(lambda_rate, mu_rate, N)
            elif model == "M/M/k (fuente finita)":
                result = self.mmk_finite(lambda_rate, mu_rate, k, N)
            else:
                result = "Modelo no implementado aún."

            self.results.delete("1.0", tk.END)
            self.results.insert(tk.END, result)
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores válidos.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def mm1(self, lambda_rate, mu_rate):
        rho = lambda_rate / mu_rate
        L = rho / (1 - rho)
        Lq = rho ** 2 / (1 - rho)
        W = 1 / (mu_rate - lambda_rate)
        Wq = rho / (mu_rate - lambda_rate)
        result = f"M/M/1 Model:\nL: {L:.2f}\nLq: {Lq:.2f}\nW: {W:.2f}\nWq: {Wq:.2f}\n"
        return result

    def mmk(self, lambda_rate, mu_rate, k):
        rho = lambda_rate / (k * mu_rate)
        # Additional calculations needed for M/M/k
        result = f"M/M/k Model:\nRho: {rho:.2f}\n"
        return result

    def mg1(self, lambda_rate, mu_rate):
        rho = lambda_rate / mu_rate
        Lq = (lambda_rate ** 2) / (2 * mu_rate * (mu_rate - lambda_rate))
        L = Lq + rho
        Wq = Lq / lambda_rate
        W = Wq + 1 / mu_rate
        result = f"M/G/1 Model:\nL: {L:.2f}\nLq: {Lq:.2f}\nW: {W:.2f}\nWq: {Wq:.2f}\n"
        return result

    def md1(self, lambda_rate, mu_rate):
        rho = lambda_rate / mu_rate
        Lq = (rho ** 2) / (2 * (1 - rho))
        L = Lq + rho
        Wq = Lq / lambda_rate
        W = Wq + 1 / mu_rate
        result = f"M/D/1 Model:\nL: {L:.2f}\nLq: {Lq:.2f}\nW: {W:.2f}\nWq: {Wq:.2f}\n"
        return result

    def mgk_blocked(self, lambda_rate, mu_rate, k):
        # Placeholder implementation for M/G/k with blocked customers eliminated
        result = "M/G/k with blocked customers eliminated: Not implemented yet."
        return result

    def mm1_finite(self, lambda_rate, mu_rate, N):
        # Placeholder implementation for M/M/1 with finite population
        result = "M/M/1 with finite population: Not implemented yet."
        return result

    def mmk_finite(self, lambda_rate, mu_rate, k, N):
        # Placeholder implementation for M/M/k with finite population
        result = "M/M/k with finite population: Not implemented yet."
        return result


if __name__ == "__main__":
    app = QueueModelsApp()
    app.mainloop()
