import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Estacionamento")
        self.estacionamento = None

        self.carregar_dados_iniciais()

        self.menu_principal()

    def carregar_dados_iniciais(self):
        total_vagas = simpledialog.askinteger("Configurar Estacionamento", "Digite o número total de vagas:")
        if total_vagas:
            self.estacionamento = Estacionamento(total_vagas)
        else:
            messagebox.showerror("Erro", "Número de vagas inválido!")
            self.root.quit()

    def menu_principal(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.estacionar_button = tk.Button(self.frame, text="Estacionar Veículo", command=self.estacionar_veiculo)
        self.estacionar_button.pack()

        self.registrar_saida_button = tk.Button(self.frame, text="Registrar Saída", command=self.registrar_saida)
        self.registrar_saida_button.pack()

        self.procurar_button = tk.Button(self.frame, text="Procurar Veículo", command=self.procurar_veiculo)
        self.procurar_button.pack()

        self.resumo_button = tk.Button(self.frame, text="Resumo de Ocupação", command=self.resumo_ocupacao)
        self.resumo_button.pack()

    def estacionar_veiculo(self):
        placa = simpledialog.askstring("Estacionar Veículo", "Digite a placa do veículo:")
        if placa:
            vaga = self.estacionamento.estacionar(placa)
            if vaga is not None:
                messagebox.showinfo("Sucesso", f"Veículo estacionado na vaga {vaga}.")
            else:
                messagebox.showerror("Erro", "Estacionamento lotado!")

    def registrar_saida(self):
        placa = simpledialog.askstring("Registrar Saída", "Digite a placa do veículo:")
        if placa:
            vaga, valor = self.estacionamento.registrar_saida(placa)
            if vaga:
                messagebox.showinfo("Sucesso", f"Veículo removido da vaga {vaga}.\nValor a pagar: R${valor:.2f}")
            else:
                messagebox.showerror("Erro", "Veículo não encontrado!")

    def procurar_veiculo(self):
        placa = simpledialog.askstring("Procurar Veículo", "Digite a placa do veículo:")
        if placa:
            vaga = self.estacionamento.procurar_veiculo(placa)
            if vaga:
                messagebox.showinfo("Veículo Encontrado", f"Veículo encontrado na vaga {vaga}.")
            else:
                messagebox.showerror("Erro", "Veículo não encontrado!")

    def resumo_ocupacao(self):
        resumo = self.estacionamento.resumo_ocupacao()
        messagebox.showinfo("Resumo de Ocupação", resumo)

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

    def procurar_veiculo(self, placa):
        if placa in self.entradas:
            return self.vagas.index(placa) + 1
        return None

    def resumo_ocupacao(self):
        vagas_ocupadas = sum(1 for vaga in self.vagas if vaga is not None)
        vagas_disponiveis = self.total_vagas - vagas_ocupadas
        return f"Vagas Totais: {self.total_vagas}\nVagas Ocupadas: {vagas_ocupadas}\nVagas Disponíveis: {vagas_disponiveis}"

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()