import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from utilidades import resource_path, ICONS


def alinhar_valores_interface():
    def alinhar():
        conteudo = text_area.get("1.0", tk.END).strip()
        if not conteudo:
            messagebox.showwarning("Aviso", "Nenhum valor foi fornecido.")
            return

        linhas = [linha.strip() for linha in conteudo.split("\n") if linha.strip()]
        if not linhas:
            messagebox.showwarning("Aviso", "Nenhum valor válido foi fornecido.")
            return

        if remover_duplicatas_var.get():
            linhas = sorted(list(set(linhas)), key=linhas.index)

        delimitador = delimitador_combo.get()
        resultado = delimitador.join(linhas)

        resultado_entry.configure(state="normal")
        resultado_entry.delete(0, tk.END)
        resultado_entry.insert(0, resultado)
        resultado_entry.configure(state="readonly")

    def limpar_entrada():
        text_area.delete("1.0", tk.END)
        resultado_entry.configure(state="normal")
        resultado_entry.delete(0, tk.END)
        resultado_entry.configure(state="readonly")

    janela = tk.Toplevel()
    janela.title("Alinhar Valores")
    janela.geometry("550x450")
    janela.minsize(550, 450)
    janela.iconbitmap(resource_path("icon.ico"))

    main_frame = ttk.Frame(janela, padding=(20, 10))
    main_frame.pack(expand=True, fill="both")

    # --- ENTRADA DE DADOS ---
    ttk.Label(
        main_frame,
        text="Informe os valores, um por linha:",
        font=("Segoe UI", 12, "bold"),
    ).pack(fill="x", pady=(0, 5))
    text_area = scrolledtext.ScrolledText(
        main_frame, width=60, height=10, relief="solid", borderwidth=1
    )
    text_area.pack(expand=True, fill="both")

    # --- OPÇÕES ---
    opcoes_frame = ttk.Frame(main_frame)
    opcoes_frame.pack(fill="x", pady=10)

    ttk.Label(opcoes_frame, text="Delimitador:").pack(side="left", padx=(0, 5))
    delimitador_var = tk.StringVar(value=",")
    delimitadores = [",", ";", "|", "/", "\\", "-"]
    delimitador_combo = ttk.Combobox(
        opcoes_frame,
        textvariable=delimitador_var,
        values=delimitadores,
        state="readonly",
        width=5,
    )
    delimitador_combo.pack(side="left", padx=5)

    remover_duplicatas_var = tk.BooleanVar()
    check_duplicatas = ttk.Checkbutton(
        opcoes_frame,
        text="Remover duplicatas",
        variable=remover_duplicatas_var,
        style="Switch.TCheckbutton",
    )
    check_duplicatas.pack(side="left", padx=20)

    # --- RESULTADO ---
    ttk.Label(main_frame, text="Resultado:", font=("Segoe UI", 10, "bold")).pack(
        fill="x", pady=(10, 5)
    )
    resultado_entry = ttk.Entry(main_frame, width=60, state="readonly")
    resultado_entry.pack(fill="x")

    # --- BOTÕES DE AÇÃO ---
    botoes_frame = ttk.Frame(main_frame)
    botoes_frame.pack(side="bottom", fill="x", pady=(20, 10))

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
        text="Alinhar",
        style="Accent.TButton",
        image=ICONS.get("executar", tk.PhotoImage()), 
        compound="left",
        command=alinhar,
    ).pack(side="right")

    return janela
