import re
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import font

from utilidades import resource_path

def obter_nome_tabela():
    while True:
        tabela = simpledialog.askstring("Nome da Tabela", "Informe o nome da tabela:")
        if not tabela:
            return None
        if re.match("^[A-Za-z_][A-Za-z0-9_]*$", tabela):
            return tabela
        else:
            messagebox.showerror("Erro", "Nome de tabela inválido. Tente novamente.")

def obter_colunas_valores():
    colunas = []
    valores = []
    while True:
        coluna = simpledialog.askstring("Nome da Coluna", "Informe o nome da coluna (ou deixe vazio para finalizar):")
        if not coluna:
            break
        if not re.match("^[A-Za-z_][A-Za-z0-9_]*$", coluna):
            messagebox.showerror("Erro", "Nome de coluna inválido. Tente novamente.")
            continue
        valor = simpledialog.askstring("Valor da Coluna", f"Informe o valor para '{coluna}':")
        colunas.append(coluna)
        valores.append(valor)
    return colunas, valores

def gerar_insert():
    tabela = obter_nome_tabela()
    if not tabela:
        return
    colunas, valores = obter_colunas_valores()
    if not colunas:
        messagebox.showwarning("Aviso", "Nenhuma coluna informada. Operação cancelada.")
        return
    colunas_str = ", ".join(colunas)
    valores_str = ", ".join(f"'{v}'" for v in valores)
    insert_sql = f"INSERT INTO {tabela} ({colunas_str}) VALUES ({valores_str})"
    resultado_texto.insert(tk.END, f"\nScript INSERT gerado:\n\n{insert_sql}\n")

def gerar_update():
    tabela = obter_nome_tabela()
    if not tabela:
        return
    colunas, valores = obter_colunas_valores()
    if not colunas:
        messagebox.showwarning("Aviso", "Nenhuma coluna informada. Operação cancelada.")
        return
    set_clauses = ", ".join(f"{colunas[i]} = '{valores[i]}'" for i in range(len(colunas)))
    condicao = simpledialog.askstring("Condição WHERE", "Informe a condição WHERE para o UPDATE (e.g., id = 1):")
    if not condicao:
        messagebox.showwarning("Aviso", "Condição WHERE não informada. Operação cancelada.")
        return
    update_sql = f"UPDATE {tabela} SET {set_clauses} WHERE {condicao}"
    resultado_texto.insert(tk.END, f"\nScript UPDATE gerado:\n\n{update_sql}\n")

def gerar_delete():
    tabela = obter_nome_tabela()
    if not tabela:
        return
    condicao = simpledialog.askstring("Condição WHERE", "Informe a condição WHERE para o DELETE (e.g., id = 1):")
    if not condicao:
        messagebox.showwarning("Aviso", "Condição WHERE não informada. Operação cancelada.")
        return
    delete_sql = f"DELETE FROM {tabela} WHERE {condicao}"
    resultado_texto.insert(tk.END, f"\nScript DELETE gerado:\n\n{delete_sql}\n")

def menu_gerador_scripts():
    def limpar_entrada():
        """Limpa o conteúdo do campo de entrada."""
        resultado_texto.delete("1.0", tk.END)
    
    janela = tk.Toplevel()
    janela.title("Gerador de Scripts SQL")
    janela.configure(bg='#67d167')
    janela.geometry('700x330')
    janela.minsize(700, 330)
    janela.iconbitmap(resource_path('icon.ico'))  # Caminho corrigido
    
    regular = font.Font(family="Verdana", size=11, weight="normal")

    frame_botoes = tk.Frame(janela, bg='#67d167')
    frame_botoes.pack(pady=10)

    btn_insert = tk.Button(frame_botoes, text="Gerar script INSERT", bg="#7acbe6", foreground="black", font=regular, command=gerar_insert)
    btn_insert.grid(row=0, column=0, padx=5)

    btn_update = tk.Button(frame_botoes, text="Gerar script UPDATE", bg="#bc7ff6", foreground="black", font=regular, command=gerar_update)
    btn_update.grid(row=0, column=1, padx=5)

    btn_delete = tk.Button(frame_botoes, text="Gerar script DELETE", bg="#dc3545", foreground="black", font=regular, command=gerar_delete)
    btn_delete.grid(row=0, column=2, padx=5)

    global resultado_texto
    resultado_texto = tk.Text(janela, height=12, font=regular, width=60)
    resultado_texto.pack(pady=5)
    
    frame = tk.Frame(janela, bg='#67d167')
    frame.pack(pady=5)

    btn_sair = tk.Button(frame, text="Fechar", bg="#dc3545", font=regular, command=janela.destroy)
    btn_sair.pack(side=tk.LEFT, padx=5)
    
    # Botão para limpar o campo de entrada
    tk.Button(frame, text="Limpar Entrada", bg="#f0ad4e", font=regular, command=limpar_entrada).pack(side=tk.LEFT, padx=5)

    return janela