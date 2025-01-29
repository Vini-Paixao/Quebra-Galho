import subprocess
import tempfile
import os
from tkinter import font, messagebox, scrolledtext
import tkinter as tk

from utilidades import resource_path

def capturar_entrada_sql():
    """
    Captura múltiplas linhas de entrada do usuário até uma linha vazia ser inserida.
    """
    print("Insira a consulta SQL (pressione Enter em uma linha vazia para finalizar):")
    linhas = []
    while True:
        linha = input()
        if linha.strip() == "":
            break
        linhas.append(linha)
    return "\n".join(linhas)

def validar_sintaxe_sql(consulta_sql):
    """
    Valida a sintaxe da consulta SQL usando o SQLFluff.
    """
    # Cria um arquivo temporário para armazenar a consulta SQL
    with tempfile.NamedTemporaryFile(delete=False, suffix='.sql', mode='w') as temp_file:
        temp_file.write(consulta_sql)
        temp_file_path = temp_file.name
    
    try:
        # Executa o SQLFluff para validar a sintaxe
        resultado = subprocess.run(
            ['sqlfluff', 'lint', temp_file_path, '--dialect', 'tsql'],
            capture_output=True,
            text=True
        )
        
        # Verifica o código de retorno e analisa as saídas
        if resultado.returncode == 0:
            return "Sintaxe válida."
        else:
            return f"Erros encontrados:\n{resultado.stderr or resultado.stdout}"
    finally:
        # Remove o arquivo temporário
        os.remove(temp_file_path)
        
def validador_sintaxe_interface():
    def validar():
        consulta = text_area.get("1.0", tk.END).strip()
        if consulta:
            resultado = validar_sintaxe_sql(consulta)
            messagebox.showinfo("Resultado da Validação", resultado)
        else:
            messagebox.showwarning("Aviso", "Por favor, insira uma consulta SQL.")

    janela = tk.Toplevel()
    janela.title("Validador de Sintaxe SQL")
    janela.geometry("500x300")
    janela.minsize(500, 300)
    janela.iconbitmap(resource_path('icon.ico'))  # Caminho corrigido
    janela.configure(bg='lightgreen')
    
    # Fontes
    bold = font.Font(family="Verdana", size=12, weight="bold")
    regular = font.Font(family="Verdana", size=10, weight="normal")

    label = tk.Label(janela, text="Insira sua consulta SQL:", font=bold, bg='lightgreen')
    label.pack(pady=5)

    text_area = scrolledtext.ScrolledText(janela, width=55, height=10, font=regular)
    text_area.pack(pady=5)

    btn_validar = tk.Button(janela, text="Validar Sintaxe", bg="green", foreground="white", font=regular, command=validar)
    btn_validar.pack(pady=5)

    btn_fechar = tk.Button(janela, text="Fechar", bg="#dc3545", font=regular, command=janela.destroy)
    btn_fechar.pack(pady=5)
