import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime

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

        self.saida_entry = tk.Entry(self.frame)
        self.saida_entry.pack()

        self.registrar_saida_button = tk.Button(self.frame, text="Registrar Saída", command=self.registrar_saida)
        self.registrar_saida_button.pack()

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

    def registrar_saida(self):
        placa = self.saida_entry.get()
        if placa:
            vaga, valor = self.estacionamento.registrar_saida(placa)
            if vaga:
                messagebox.showinfo("Sucesso", f"Veículo removido da vaga {vaga}.\nValor a pagar: R${valor:.2f}")
            else:
                messagebox.showerror("Erro", "Veículo não encontrado!")

class Estacionamento:
    def __init__(self, total_vagas):
        self.total_vagas = total_vagas
        self.vagas = [None] * total_vagas
        self.entradas = {}

    def estacionar(self, placa):
        for i, vaga in enumerate(self.vagas):
            if vaga is None:
                self.vagas[i] = placa
                self.entradas[placa] = datetime.now()
                return i + 1
        return None

    def registrar_saida(self, placa):
        if placa in self.entradas:
            vaga = self.vagas.index(placa)
            self.vagas[vaga] = None
            entrada = self.entradas.pop(placa)
            tempo = (datetime.now() - entrada).total_seconds() / 3600
            valor = tempo * 5  # R$5 por hora
            return vaga + 1, valor
        return None, None

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()