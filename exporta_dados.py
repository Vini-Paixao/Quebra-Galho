import tkinter as tk
from tkinter import ttk, messagebox, filedialog, font
import pandas as pd
from io import StringIO

def exportar_dados_interface():
    def exportar():
        conteudo = text_area.get("1.0", tk.END).strip()
        if not conteudo:
            messagebox.showwarning("Aviso", "Nenhum dado foi fornecido.")
            return

        # Lê os dados da área de texto
        data = StringIO(conteudo)
        try:
            df = pd.read_csv(data, sep="\t")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao ler os dados: {e}")
            return

        # Verifica o número de registros
        num_registros = len(df)
        if num_registros > 5000:
            messagebox.showwarning("Aviso", f"O número de registros ({num_registros}) excede o limite de 5.000.")
            return

        formato = formato_var.get()
        if formato == "CSV":
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if file_path:
                try:
                    df.to_csv(file_path, index=False)
                    messagebox.showinfo("Sucesso", f"Dados exportados com sucesso para {file_path}")
                except Exception as e:
                    messagebox.showerror("Erro", f"Falha ao exportar para CSV: {e}")
        elif formato == "JSON":
            try:
                json_data = df.to_json(orient="records", lines=True)
                json_window = tk.Toplevel(janela)
                json_window.title("Dados JSON")
                json_text = tk.Text(json_window, wrap="none")
                json_text.insert("1.0", json_data)
                json_text.configure(state="disabled")
                json_text.pack(expand=True, fill="both")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao converter para JSON: {e}")
        elif formato == "XLSX":
            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
            if file_path:
                try:
                    df.to_excel(file_path, index=False)
                    messagebox.showinfo("Sucesso", f"Dados exportados com sucesso para {file_path}")
                except Exception as e:
                    messagebox.showerror("Erro", f"Falha ao exportar para Excel: {e}")
        else:
            messagebox.showwarning("Aviso", "Formato de exportação não selecionado.")

    janela = tk.Toplevel()
    janela.title("Exportar Dados")
    janela.geometry("600x530")
    janela.configure(bg='lightgreen')

    # Fontes
    bold = font.Font(family="Verdana", size=12, weight="bold")
    regular = font.Font(family="Verdana", size=10, weight="normal")

    instrucao_label = tk.Label(janela, text="Cole os resultados da consulta SQL (incluindo cabeçalhos):", font=bold, bg='lightgreen')
    instrucao_label.pack(pady=5)
    
    limite_label = tk.Label(janela, text="* Limite de 5.000 registros para exportação.", font=regular, bg='lightgreen')
    limite_label.pack(pady=5)

    text_area = tk.Text(janela, wrap="none", width=70, height=15, font=regular)
    text_area.pack(pady=5)

    formato_label = tk.Label(janela, text="Selecione o formato de exportação:", font=regular, bg='lightgreen')
    formato_label.pack(pady=5)

    formato_var = tk.StringVar(value="CSV")
    formatos = [("CSV", "CSV"), ("JSON", "JSON"), ("Excel (XLSX)", "XLSX")]
    for text, mode in formatos:
        tk.Radiobutton(janela, text=text, variable=formato_var, value=mode, font=regular, bg='lightgreen').pack(anchor="w")

    exportar_button = tk.Button(janela, text="Exportar", font=regular, command=exportar)
    exportar_button.pack(pady=10)
    
    # Botão para fechar a janela
    tk.Button(janela, text="Fechar", font=regular, command=janela.destroy).pack(pady=5)

    janela.mainloop()

