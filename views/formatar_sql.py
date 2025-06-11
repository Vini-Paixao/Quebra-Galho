import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sqlparse
from utilidades import resource_path, ICONS


def formatar_sql_interface():
    def formatar():
        consultas = entrada_texto.get("1.0", tk.END).strip()
        if not consultas:
            messagebox.showwarning("Aviso", "Nenhuma consulta SQL foi fornecida.")
            return

        try:
            instrucoes = sqlparse.split(consultas)
            consultas_formatadas = [
                sqlparse.format(
                    instrucao,
                    reindent=True,
                    keyword_case="upper",
                    identifier_case="lower",
                )
                for instrucao in instrucoes
                if instrucao.strip()
            ]

            resultado_texto.config(state=tk.NORMAL)
            resultado_texto.delete("1.0", tk.END)
            resultado_texto.insert(
                tk.END, "\n\n-- --------\n\n".join(consultas_formatadas)
            )
            resultado_texto.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror(
                "Erro ao Formatar", f"Ocorreu um erro inesperado:\n{e}"
            )

    def limpar_campos():
        """Limpa ambos os campos de texto."""
        entrada_texto.delete("1.0", tk.END)
        resultado_texto.config(state=tk.NORMAL)
        resultado_texto.delete("1.0", tk.END)
        resultado_texto.config(state=tk.DISABLED)

    janela = tk.Toplevel()
    janela.title("Formatador de SQL")
    janela.geometry("600x700")
    janela.minsize(600, 700)
    janela.iconbitmap(resource_path("icon.ico"))
    janela.state("zoomed")

    main_frame = ttk.Frame(janela, padding=20)
    main_frame.pack(expand=True, fill="both")

    # --- ENTRADA ---
    ttk.Label(
        main_frame, text="Insira o Script SQL:", font=("Segoe UI", 12, "bold")
    ).pack(anchor="w")
    entrada_texto = scrolledtext.ScrolledText(
        main_frame, width=60, height=10, relief="solid", borderwidth=1
    )
    entrada_texto.pack(expand=True, fill="both", pady=5)

    # --- SAÍDA ---
    ttk.Label(
        main_frame, text="Script SQL Formatado:", font=("Segoe UI", 12, "bold")
    ).pack(anchor="w", pady=(10, 0))
    resultado_texto = scrolledtext.ScrolledText(
        main_frame,
        width=60,
        height=10,
        state=tk.DISABLED,
        relief="solid",
        borderwidth=1,
    )
    resultado_texto.pack(expand=True, fill="both", pady=5)

    # --- BOTÕES DE AÇÃO ---
    botoes_frame = ttk.Frame(main_frame)
    botoes_frame.pack(side="bottom", fill="x", pady=(15, 0))

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
        command=limpar_campos,
    ).pack(side="right", padx=10)
    ttk.Button(
        botoes_frame,
        text="Formatar SQL",
        style="Accent.TButton",
        image=ICONS.get("executar", tk.PhotoImage()),
        compound="left",
        command=formatar,
    ).pack(side="right")

    return janela
