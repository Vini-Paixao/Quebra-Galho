import re
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext

from utilidades import resource_path, ICONS


# As funções de geração de script agora recebem o widget de texto como argumento
def gerar_insert(text_widget):
    tabela = simpledialog.askstring("Nome da Tabela", "Informe o nome da tabela:")
    if not tabela or not re.match("^[A-Za-z_][A-Za-z0-9_]*$", tabela):
        if tabela is not None:
            messagebox.showerror("Erro", "Nome de tabela inválido.")
        return

    colunas, valores = [], []
    while True:
        coluna = simpledialog.askstring(
            "Coluna", "Informe o nome da coluna (ou deixe vazio para finalizar):"
        )
        if not coluna:
            break
        if not re.match("^[A-Za-z_][A-Za-z0-9_]*$", coluna):
            messagebox.showerror("Erro", "Nome de coluna inválido.")
            continue
        valor = simpledialog.askstring("Valor", f"Informe o valor para '{coluna}':")
        colunas.append(coluna)
        valores.append(valor if valor is not None else "")

    if not colunas:
        messagebox.showwarning("Aviso", "Nenhuma coluna informada. Operação cancelada.")
        return

    colunas_str = ", ".join(colunas)
    valores_str = ", ".join(f"'{v}'" for v in valores)
    insert_sql = f"INSERT INTO {tabela} ({colunas_str})\nVALUES ({valores_str});"
    text_widget.insert(tk.END, f"-- Script INSERT gerado:\n{insert_sql}\n\n")


def gerar_update(text_widget):
    tabela = simpledialog.askstring("Nome da Tabela", "Informe o nome da tabela:")
    if not tabela or not re.match("^[A-Za-z_][A-Za-z0-9_]*$", tabela):
        if tabela is not None:
            messagebox.showerror("Erro", "Nome de tabela inválido.")
        return

    colunas, valores = [], []
    while True:
        coluna = simpledialog.askstring(
            "Coluna", "Informe a coluna para atualizar (ou deixe vazio para finalizar):"
        )
        if not coluna:
            break
        if not re.match("^[A-Za-z_][A-Za-z0-9_]*$", coluna):
            messagebox.showerror("Erro", "Nome de coluna inválido.")
            continue
        valor = simpledialog.askstring(
            "Valor", f"Informe o novo valor para '{coluna}':"
        )
        colunas.append(coluna)
        valores.append(valor if valor is not None else "")

    if not colunas:
        messagebox.showwarning("Aviso", "Nenhuma coluna informada. Operação cancelada.")
        return

    set_clauses = ",\n  ".join(f"{col} = '{val}'" for col, val in zip(colunas, valores))
    condicao = simpledialog.askstring(
        "Condição", "Informe a condição WHERE (ex: id = 1):"
    )
    if not condicao:
        messagebox.showwarning("Aviso", "A condição WHERE é obrigatória para UPDATE.")
        return

    update_sql = f"UPDATE {tabela}\nSET {set_clauses}\nWHERE {condicao};"
    text_widget.insert(tk.END, f"-- Script UPDATE gerado:\n{update_sql}\n\n")


def gerar_delete(text_widget):
    tabela = simpledialog.askstring("Nome da Tabela", "Informe o nome da tabela:")
    if not tabela or not re.match("^[A-Za-z_][A-Za-z0-9_]*$", tabela):
        if tabela is not None:
            messagebox.showerror("Erro", "Nome de tabela inválido.")
        return

    condicao = simpledialog.askstring(
        "Condição", "Informe a condição WHERE (ex: id = 1):"
    )
    if not condicao:
        messagebox.showwarning("Aviso", "A condição WHERE é obrigatória para DELETE.")
        return

    delete_sql = f"DELETE FROM {tabela}\nWHERE {condicao};"
    text_widget.insert(tk.END, f"-- Script DELETE gerado:\n{delete_sql}\n\n")


def menu_gerador_scripts():
    janela = tk.Toplevel()
    janela.title("Gerador de Scripts SQL")
    janela.geometry("700x450")
    janela.minsize(600, 400)
    janela.iconbitmap(resource_path("icon.ico"))

    main_frame = ttk.Frame(janela, padding=20)
    main_frame.pack(expand=True, fill="both")

    # --- BOTÕES DE GERAÇÃO ---
    botoes_geracao_frame = ttk.Frame(main_frame)
    botoes_geracao_frame.pack(fill="x", pady=(0, 15))
    botoes_geracao_frame.columnconfigure((0, 1, 2), weight=1)

    # Passando `resultado_texto` como argumento para as funções
    ttk.Button(
        botoes_geracao_frame,
        text=" Gerar INSERT",
        image=ICONS.get("insert", tk.PhotoImage()),
        compound="left",
        command=lambda: gerar_insert(resultado_texto),
    ).grid(row=0, column=0, sticky="ew", padx=(0, 5))
    ttk.Button(
        botoes_geracao_frame,
        text=" Gerar UPDATE",
        image=ICONS.get("update", tk.PhotoImage()),
        compound="left",
        command=lambda: gerar_update(resultado_texto),
    ).grid(row=0, column=1, sticky="ew", padx=5)
    ttk.Button(
        botoes_geracao_frame,
        text=" Gerar DELETE",
        image=ICONS.get("delete", tk.PhotoImage()),
        compound="left",
        command=lambda: gerar_delete(resultado_texto),
    ).grid(row=0, column=2, sticky="ew", padx=(5, 0))

    # --- CAMPO DE RESULTADO ---
    ttk.Label(main_frame, text="Scripts Gerados:", font=("Segoe UI", 10, "bold")).pack(
        anchor="w"
    )
    resultado_texto = scrolledtext.ScrolledText(
        main_frame, height=12, width=60, relief="solid", borderwidth=1
    )
    resultado_texto.pack(expand=True, fill="both", pady=5)

    def limpar_entrada():
        resultado_texto.delete("1.0", tk.END)

    # --- BOTÕES DE AÇÃO ---
    botoes_acao_frame = ttk.Frame(main_frame)
    botoes_acao_frame.pack(side="bottom", fill="x", pady=(15, 0))

    ttk.Button(
        botoes_acao_frame,
        text="Fechar",
        image=ICONS.get("fechar", tk.PhotoImage()),
        compound="left",
        command=janela.destroy,
    ).pack(side="right")
    ttk.Button(
        botoes_acao_frame,
        text="Limpar",
        image=ICONS.get("limpar", tk.PhotoImage()),
        compound="left",
        command=limpar_entrada,
    ).pack(side="right", padx=10)

    return janela
