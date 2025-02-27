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
    
    def limpar_entrada():
        """Limpa o conteúdo do campo de entrada."""
        text_area.delete("1.0", tk.END)

    janela = tk.Toplevel()
    janela.title("Validador de Sintaxe SQL")
    janela.geometry("530x325")
    janela.minsize(530, 325)
    janela.iconbitmap(resource_path('icon.ico'))  # Caminho corrigido
    janela.configure(bg='#67d167')
    
    # Fontes
    bold = font.Font(family="Verdana", size=12, weight="bold")
    regular = font.Font(family="Verdana", size=11, weight="normal")

    label = tk.Label(janela, text="Insira sua consulta SQL:", font=bold, bg='#67d167')
    label.pack(pady=5)

    text_area = scrolledtext.ScrolledText(janela, width=48, height=10, font=regular)
    text_area.pack(pady=5)
    
    frame = tk.Frame(janela, bg='#67d167')
    frame.pack(pady=5)

    btn_validar = tk.Button(frame, text="Validar Sintaxe", bg="#bc7ff6", foreground="black", font=regular, command=validar)
    btn_validar.pack(side=tk.LEFT, padx=5)
    
    # Botão para limpar o campo de entrada
    tk.Button(frame, text="Limpar Entrada", bg="#f0ad4e", font=regular, command=limpar_entrada).pack(side=tk.LEFT, padx=5)

    btn_fechar = tk.Button(janela, text="Fechar", bg="#dc3545", font=regular, command=janela.destroy)
    btn_fechar.pack(pady=5)
    
    return janela
