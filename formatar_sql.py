from tkinter import font
import sqlparse
import tkinter as tk
from tkinter import scrolledtext, messagebox

from utilidades import resource_path


def formatar_sql():
    print("Insira as consultas SQL a serem formatadas (pressione Enter em uma linha vazia para finalizar):")
    linhas = []
    while True:
        linha = input()
        if linha.strip() == "":
            break
        linhas.append(linha)

    consultas = "\n".join(linhas)
    if not consultas.strip():
        print("Nenhuma consulta SQL foi fornecida.")
        return

    # Divide as consultas em instruções individuais
    instrucoes = sqlparse.split(consultas)

    consultas_formatadas = []
    for instrucao in instrucoes:
        consulta_formatada = sqlparse.format(instrucao, reindent=True, keyword_case='upper')
        consultas_formatadas.append(consulta_formatada)

    print("\nConsultas SQL formatadas:")
    for consulta in consultas_formatadas:
        print(consulta)
        print('-' * 50)  # Separador entre consultas formatadas
        

def formatar_sql_interface():
    def formatar():
        consultas = entrada_texto.get("1.0", tk.END).strip()
        if not consultas:
            messagebox.showwarning("Aviso", "Nenhuma consulta SQL foi fornecida.")
            return

        # Divide as consultas em instruções individuais
        instrucoes = sqlparse.split(consultas)

        consultas_formatadas = []
        for instrucao in instrucoes:
            consulta_formatada = sqlparse.format(instrucao, reindent=True, keyword_case='upper')
            consultas_formatadas.append(consulta_formatada)

        resultado_texto.config(state=tk.NORMAL)
        resultado_texto.delete("1.0", tk.END)
        for consulta in consultas_formatadas:
            resultado_texto.insert(tk.END, consulta + "\n" + "-" * 50 + "\n")
        resultado_texto.config(state=tk.DISABLED)

    # Cria a janela principal
    janela = tk.Tk()
    janela.title("Formatador de SQL")
    janela.configure(bg='lightgreen')
    janela.geometry('600x510')
    janela.minsize(600, 510)
    janela.iconbitmap(resource_path('icon.ico'))  # Caminho corrigido
    
    # Fontes
    bold = font.Font(family="Verdana", size=12, weight="bold")
    regular = font.Font(family="Verdana", size=8, weight="normal")

    # Campo de entrada para as consultas SQL
    tk.Label(janela, text="Insira as consultas SQL:", font=bold, bg='lightgreen').pack(pady=5)
    entrada_texto = scrolledtext.ScrolledText(janela, width=60, height=10)
    entrada_texto.pack(pady=5)

    # Botão para formatar as consultas
    tk.Button(janela, text="Formatar SQL", bg="green", foreground="white", font=regular, command=formatar).pack(pady=5)

    # Campo de saída para as consultas formatadas
    tk.Label(janela, text="Consultas SQL formatadas:", font=bold, bg='lightgreen').pack(pady=5)
    resultado_texto = scrolledtext.ScrolledText(janela, width=60, height=10, state=tk.DISABLED)
    resultado_texto.pack(pady=5)

    # Botão para fechar a janela
    tk.Button(janela, text="Fechar", bg="#dc3545", font=regular, command=janela.destroy).pack(pady=5)

    janela.mainloop()
