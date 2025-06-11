import subprocess
import tempfile
import os
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

from utilidades import resource_path, ICONS


def validar_sintaxe_sql(consulta_sql):
    """
    Valida a sintaxe da consulta SQL usando o SQLFluff.
    """
    # Cria um arquivo temporário para armazenar a consulta SQL
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=".sql", mode="w", encoding="utf-8"
    ) as temp_file:
        temp_file.write(consulta_sql)
        temp_file_path = temp_file.name

    try:
        # Executa o SQLFluff para validar a sintaxe
        resultado = subprocess.run(
            ["sqlfluff", "lint", temp_file_path, "--dialect", "tsql"],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

        # Verifica o código de retorno e analisa as saídas
        if resultado.returncode == 0:
            return "Sintaxe válida."
        else:
            # Retorna a saída de erro ou a saída padrão, que contém os erros de lint.
            return f"Erros encontrados:\n{resultado.stderr or resultado.stdout}"
    except FileNotFoundError:
        return "Erro: 'sqlfluff' não encontrado. Verifique se ele está instalado e no PATH do sistema."
    except Exception as e:
        return f"Ocorreu um erro inesperado: {e}"
    finally:
        # Garante que o arquivo temporário seja removido
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


def validador_sintaxe_interface():
    def validar():
        consulta = text_area.get("1.0", tk.END).strip()
        if consulta:
            # Mostra uma mensagem de "Aguarde"
            resultado_label.config(text="Validando, aguarde...")
            janela.update_idletasks()  # Força a atualização da UI

            resultado = validar_sintaxe_sql(consulta)

            # Limpa a mensagem de "Aguarde"
            resultado_label.config(text="")
            messagebox.showinfo("Resultado da Validação", resultado)
        else:
            messagebox.showwarning("Aviso", "Por favor, insira uma consulta SQL.")

    def limpar_entrada():
        """Limpa o conteúdo do campo de entrada."""
        text_area.delete("1.0", tk.END)

    janela = tk.Toplevel()
    janela.title("Validador de Sintaxe SQL")
    janela.geometry("530x400")
    janela.minsize(530, 400)
    janela.iconbitmap(resource_path("icon.ico"))

    main_frame = ttk.Frame(janela, padding=20)
    main_frame.pack(expand=True, fill="both")

    ttk.Label(
        main_frame, text="Insira sua consulta SQL:", font=("Segoe UI", 12, "bold")
    ).pack(anchor="w")

    text_area = scrolledtext.ScrolledText(
        main_frame, width=48, height=10, relief="solid", borderwidth=1
    )
    text_area.pack(expand=True, fill="both", pady=5)

    # Label para feedback de "Aguarde"
    resultado_label = ttk.Label(main_frame, text="", font=("Segoe UI", 9, "italic"))
    resultado_label.pack(anchor="w")

    # --- BOTÕES DE AÇÃO ---
    botoes_frame = ttk.Frame(main_frame)
    botoes_frame.pack(side="bottom", fill="x", pady=(15, 0))

    ttk.Button(
        botoes_frame,
        text="Fechar",
        image=ICONS.get("fechar", tk.PhotoImage()),
        compound="left",
        command=janela.destroy,
    ).pack(side="right")
    ttk.Button(
        botoes_frame,
        text="Limpar",
        image=ICONS.get("limpar", tk.PhotoImage()),
        compound="left",
        command=limpar_entrada,
    ).pack(side="right", padx=10)
    ttk.Button(
        botoes_frame,
        text="Validar Sintaxe",
        style="Accent.TButton",
        image=ICONS.get("executar", tk.PhotoImage()),
        compound="left",
        command=validar,
    ).pack(side="right")

    return janela
