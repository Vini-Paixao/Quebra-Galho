import re
import tkinter as tk
from tkinter import ttk, messagebox
from utilidades import resource_path, ICONS


def extrair_numeros(texto):
    """Remove todos os caracteres não numéricos de uma string."""
    return re.sub(r"\D", "", texto)


def limpar_formatacao():
    def processar():
        numero_formatado = entrada.get()
        if numero_formatado:
            numero_limpo = extrair_numeros(numero_formatado)
            resultado_entry.configure(state="normal")
            resultado_entry.delete(0, tk.END)
            resultado_entry.insert(0, numero_limpo)
            resultado_entry.configure(state="readonly")
        else:
            messagebox.showwarning("Aviso", "Nenhum valor fornecido.")

    def limpar_entrada():
        """Limpa o campo de entrada e o de resultado."""
        entrada.delete(0, tk.END)
        resultado_entry.configure(state="normal")
        resultado_entry.delete(0, tk.END)
        resultado_entry.configure(state="readonly")

    janela = tk.Toplevel()
    janela.title("Limpar Formatação")
    janela.geometry("400x250")
    janela.minsize(400, 250)
    janela.iconbitmap(resource_path("icon.ico"))

    main_frame = ttk.Frame(janela, padding=(20, 15))
    main_frame.pack(expand=True, fill="both")

    # --- ENTRADA DE DADOS ---
    ttk.Label(
        main_frame,
        text="Valor para limpar a formatação:",
        font=("Segoe UI", 12, "bold"),
    ).pack(fill="x", pady=(0, 5))
    entrada = ttk.Entry(main_frame, width=50)
    entrada.pack(fill="x")

    # --- RESULTADO ---
    ttk.Label(main_frame, text="Resultado:", font=("Segoe UI", 10, "bold")).pack(
        fill="x", pady=(15, 5)
    )
    resultado_entry = ttk.Entry(main_frame, width=50, state="readonly")
    resultado_entry.pack(fill="x")

    # --- BOTÕES DE AÇÃO ---
    botoes_frame = ttk.Frame(main_frame)
    botoes_frame.pack(side="bottom", fill="x", pady=(20, 0))

    ttk.Button(
        botoes_frame,
        text="Voltar",
        image=ICONS.get("voltar2", tk.PhotoImage()), 
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
        text="Processar",
        style="Accent.TButton",
        image=ICONS.get("executar", tk.PhotoImage()), 
        compound="left",
        command=processar,
    ).pack(side="right")

    return janela
