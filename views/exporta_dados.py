import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import pandas as pd
from io import StringIO

from utilidades import resource_path, ICONS


def exportar_dados_interface():
    def exportar():
        conteudo = text_area.get("1.0", tk.END).strip()
        if not conteudo:
            messagebox.showwarning(
                "Aviso", "Nenhum dado foi fornecido para exportação."
            )
            return

        # Lê os dados da área de texto, tratando o tabulador como separador
        data = StringIO(conteudo)
        try:
            df = pd.read_csv(data, sep="\t")
        except Exception as e:
            messagebox.showerror(
                "Erro de Leitura", f"Falha ao processar os dados de entrada:\n{e}"
            )
            return

        num_registros = len(df)
        if num_registros > 500000:
            messagebox.showwarning(
                "Aviso",
                f"O número de registros ({num_registros}) excede o limite de 500.000.",
            )
            if not messagebox.askyesno(
                "Continuar?",
                "A exportação pode ser lenta e consumir muita memória. Deseja continuar mesmo assim?",
            ):
                return

        formato = formato_var.get()
        file_types = {
            "CSV": [("Arquivos CSV", "*.csv")],
            "XML": [("Arquivos XML", "*.xml")],
            "XLSX": [("Arquivos Excel", "*.xlsx")],
        }

        file_path = filedialog.asksaveasfilename(
            defaultextension=f".{formato.lower()}", filetypes=file_types[formato]
        )

        if not file_path:
            return  # Usuário cancelou a caixa de diálogo

        try:
            if formato == "CSV":
                df.to_csv(file_path, index=False, sep=";", decimal=",")
            elif formato == "XML":
                df.to_xml(
                    file_path, index=False, root_name="registros", row_name="registro"
                )
            elif formato == "XLSX":
                df.to_excel(file_path, index=False)

            messagebox.showinfo(
                "Sucesso", f"Dados exportados com sucesso para\n{file_path}"
            )
        except Exception as e:
            messagebox.showerror(
                "Erro na Exportação", f"Falha ao salvar o arquivo:\n{e}"
            )

    def limpar_entrada():
        """Limpa o conteúdo do campo de entrada."""
        text_area.delete("1.0", tk.END)

    janela = tk.Toplevel()
    janela.title("Exportar Dados de Consulta")
    janela.geometry("600x520")
    janela.minsize(600, 520)
    janela.iconbitmap(resource_path("icon.ico"))

    main_frame = ttk.Frame(janela, padding=20)
    main_frame.pack(expand=True, fill="both")

    # --- ENTRADA DE DADOS ---
    ttk.Label(
        main_frame,
        text="Cole os resultados da consulta SQL (com cabeçalhos):",
        font=("Segoe UI", 12, "bold"),
    ).pack(anchor="w")
    ttk.Label(
        main_frame,
        text="* Limite de 500.000 registros. Use tabulação como separador.",
        font=("Segoe UI", 8),
    ).pack(anchor="w", pady=(0, 5))

    text_area = scrolledtext.ScrolledText(
        main_frame, wrap="none", height=13, relief="solid", borderwidth=1
    )
    text_area.pack(expand=True, fill="both", pady=5)

    # --- OPÇÕES DE FORMATO ---
    formato_frame = ttk.Labelframe(main_frame, text="Formato de Exportação", padding=10)
    formato_frame.pack(fill="x", pady=15)

    formato_var = tk.StringVar(value="XLSX")  # Padrão para Excel
    formatos = [("CSV", "CSV"), ("XML", "XML"), ("Excel (XLSX)", "XLSX")]

    # Distribui os Radiobuttons horizontalmente
    for i, (text, mode) in enumerate(formatos):
        ttk.Radiobutton(
            formato_frame, text=text, variable=formato_var, value=mode
        ).pack(side="left", padx=15, expand=True)

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
        command=limpar_entrada,
    ).pack(side="right", padx=10)
    ttk.Button(
        botoes_frame,
        text="Exportar",
        style="Accent.TButton",
        image=ICONS.get("exportar", tk.PhotoImage()),
        compound="left",
        command=exportar,
    ).pack(side="right")

    return janela
