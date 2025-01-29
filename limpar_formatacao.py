import re
import tkinter as tk
from tkinter import font

from utilidades import resource_path

def extrair_numeros(texto):
    return re.sub(r'\D', '', texto)

def limpar_formatacao():
    def processar():
        numero_formatado = entrada.get()
        if numero_formatado:
            numero_limpo = extrair_numeros(numero_formatado)
            resultado_entry.configure(state="normal")  # Habilita edição para inserir o texto
            resultado_entry.delete(0, tk.END)  # Limpa qualquer texto existente
            resultado_entry.insert(0, numero_limpo)  # Insere o número limpo
            resultado_entry.configure(state="readonly")  # Volta para somente leitura
        else:
            resultado_entry.configure(state="normal")  # Habilita para exibir mensagem
            resultado_entry.delete(0, tk.END)
            resultado_entry.insert(0, "Nenhum valor fornecido.")
            resultado_entry.configure(state="readonly")  # Volta para somente leitura

    janela = tk.Toplevel()
    janela.title("Limpar Formatação")
    janela.geometry("360x170")
    janela.minsize(360, 170)
    janela.iconbitmap(resource_path('icon.ico'))  # Caminho corrigido
    janela.configure(bg='lightblue')
    
    # Fontes
    bold = font.Font(family="Verdana", size=12, weight="bold")
    regular = font.Font(family="Verdana", size=10, weight="normal")

    tk.Label(janela, text="Informe o valor a retirar a formatação:", font=bold, bg='lightblue').pack(pady=5)

    entrada = tk.Entry(janela, width=50)
    entrada.pack(pady=5)

    btn_processar = tk.Button(janela, text="Processar", bg="lightgreen", font=regular, command=processar)
    btn_processar.pack(pady=5)

    # Campo para exibir o resultado
    resultado_entry = tk.Entry(janela, width=40, state="readonly", font=regular, readonlybackground="white", fg="black")
    resultado_entry.pack(pady=5)
    
    # Botão para fechar a janela
    tk.Button(janela, text="Fechar", bg="#dc3545", font=regular, command=janela.destroy).pack(pady=5)

    janela.mainloop()