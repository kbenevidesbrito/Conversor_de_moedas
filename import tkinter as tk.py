import tkinter as tk
from tkinter import ttk, messagebox
import requests

class ConversorMoedas:
    def __init__(self, janela):
        self.janela = janela
        janela.title("Conversor de Moedas")
        
        # Frame principal
        frame = ttk.Frame(janela, padding="20")
        frame.grid(row=0, column=0)
        
        # Entrada do valor
        ttk.Label(frame, text="Valor:").grid(column=0, row=0, sticky=tk.W)
        self.entrada_valor = ttk.Entry(frame, width=20)
        self.entrada_valor.grid(column=1, row=0, padx=5, pady=5)
        
        # Combobox de moedas
        ttk.Label(frame, text="De:").grid(column=0, row=1, sticky=tk.W)
        self.moeda_origem = ttk.Combobox(frame, values=['BRL', 'USD', 'EUR', 'GBP'], width=17)
        self.moeda_origem.grid(column=1, row=1, padx=5, pady=5)
        self.moeda_origem.set('BRL')
        
        ttk.Label(frame, text="Para:").grid(column=0, row=2, sticky=tk.W)
        self.moeda_destino = ttk.Combobox(frame, values=['BRL', 'USD', 'EUR', 'GBP'], width=17)
        self.moeda_destino.grid(column=1, row=2, padx=5, pady=5)
        self.moeda_destino.set('USD')
        
        # Botão de conversão
        self.botao = ttk.Button(frame, text="Converter", command=self.converter)
        self.botao.grid(column=0, row=3, columnspan=2, pady=10)
        
        # Resultado
        self.label_resultado = ttk.Label(frame, text="", font=('Arial', 12, 'bold'))
        self.label_resultado.grid(column=0, row=4, columnspan=2)
        
    def converter(self):
        try:
            valor = float(self.entrada_valor.get())
            origem = self.moeda_origem.get()
            destino = self.moeda_destino.get()
            
            # API KEY - Cadastre-se em https://www.exchangerate-api.com/
            API_KEY = 'SUA_CHAVE_API_AQUI'
            taxas = self.get_taxas(API_KEY, origem)
            
            if taxas and destino in taxas:
                resultado = valor * taxas[destino]
                self.label_resultado.config(text=f"{valor:.2f} {origem} = {resultado:.2f} {destino}")
            else:
                messagebox.showerror("Erro", "Não foi possível obter as taxas de câmbio.")
                
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor numérico válido.")
    
    def get_taxas(self, api_key, moeda_base):
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{moeda_base}"
        try:
            resposta = requests.get(url)
            dados = resposta.json()
            if dados['result'] == 'success':
                return dados['conversion_rates']
        except:
            return None

# Cria e roda a interface
if __name__ == "__main__":
    janela = tk.Tk()
    app = ConversorMoedas(janela)
    janela.mainloop()