import tkinter as tk
from tkinter import messagebox, simpledialog

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Estacionamento")
        self.estacionamento = None

        self.carregar_dados_iniciais()

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.placa_entry = tk.Entry(self.frame)
        self.placa_entry.pack()

        self.estacionar_button = tk.Button(self.frame, text="Estacionar", command=self.estacionar_veiculo)
        self.estacionar_button.pack()

    def carregar_dados_iniciais(self):
        total_vagas = simpledialog.askinteger("Configurar Estacionamento", "Digite o número total de vagas:")
        if total_vagas:
            self.estacionamento = Estacionamento(total_vagas)
        else:
            messagebox.showerror("Erro", "Número de vagas inválido!")
            self.root.quit()

    def estacionar_veiculo(self):
        placa = self.placa_entry.get()
        if placa:
            vaga = self.estacionamento.estacionar(placa)
            if vaga is not None:
                messagebox.showinfo("Sucesso", f"Veículo estacionado na vaga {vaga}.")
            else:
                messagebox.showerror("Erro", "Estacionamento lotado!")

class Estacionamento:
    def __init__(self, total_vagas):
        self.total_vagas = total_vagas
        self.vagas = [None] * total_vagas

    def estacionar(self, placa):
        for i, vaga in enumerate(self.vagas):
            if vaga is None:
                self.vagas[i] = placa
                return i + 1
        return None

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()