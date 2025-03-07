import tkinter as tk
from tkinter import ttk, messagebox, filedialog, font
import pandas as pd
from io import StringIO

from utilidades import resource_path

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
        if num_registros > 500000:
            messagebox.showwarning("Aviso", f"O número de registros ({num_registros}) excede o limite de 500.000!")
            return

        formato = formato_var.get()
        if formato == "CSV":
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Arquivos CSV", "*.csv")])
            if file_path:
                try:
                    df.to_csv(file_path, index=False)
                    messagebox.showinfo("Sucesso", f"Dados exportados com sucesso para {file_path}")
                except Exception as e:
                    messagebox.showerror("Erro", f"Falha ao exportar para CSV: {e}")
        elif formato == "XML":
            file_path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("Arquivos XML", "*.xml")])
            if file_path:
                try:
                    df.to_xml(file_path, index=False)
                    messagebox.showinfo("Sucesso", f"Dados exportados com sucesso para {file_path}")
                except Exception as e:
                    messagebox.showerror("Erro", f"Falha ao exportar para XML: {e}")
        elif formato == "XLSX":
            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Arquivos Excel", "*.xlsx")])
            if file_path:
                try:
                    df.to_excel(file_path, index=False)
                    messagebox.showinfo("Sucesso", f"Dados exportados com sucesso para {file_path}")
                except Exception as e:
                    messagebox.showerror("Erro", f"Falha ao exportar para Excel: {e}")
        else:
            messagebox.showwarning("Aviso", "Formato de exportação não selecionado.")
    
    def limpar_entrada():
        """Limpa o conteúdo do campo de entrada."""
        text_area.delete("1.0", tk.END)

    janela = tk.Toplevel()
    janela.title("Exportar Dados")
    janela.geometry("600x520")
    janela.minsize(600, 520)
    janela.iconbitmap(resource_path('icon.ico'))  # Caminho corrigido
    janela.configure(bg='#67d167')

    # Fontes
    bold = font.Font(family="Verdana", size=12, weight="bold")
    bold_b = font.Font(family="Verdana", size=10, weight="bold")
    regular = font.Font(family="Verdana", size=10, weight="normal")

    instrucao_label = tk.Label(janela, text="Cole os resultados da consulta SQL (incluindo cabeçalhos):", font=bold, bg='#67d167')
    instrucao_label.pack(pady=5)
    
    limite_label = tk.Label(janela, text="* Limite de 500.000 registros para exportação.", font=regular, bg='#67d167')
    limite_label.pack(pady=5)

    text_area = tk.Text(janela, wrap="none", width=70, height=13, font=regular)
    text_area.pack(pady=5)
    
    # Botão para limpar o campo de entrada
    tk.Button(janela, text="Limpar Entrada", bg="#f0ad4e", font=regular, command=limpar_entrada).pack(padx=5)

    formato_label = tk.Label(janela, text="Selecione o formato de exportação:", font=regular, bg='#67d167')
    formato_label.pack(pady=5)

    formato_var = tk.StringVar(value="CSV")
    formatos = [("CSV", "CSV"), ("XML", "XML"), ("Excel (XLSX)", "XLSX")]
    for text, mode in formatos:
        tk.Radiobutton(janela, text=text, variable=formato_var, value=mode, font=regular, bg='#67d167').pack(anchor="center", pady=2)

    exportar_button = tk.Button(janela, text="Exportar", bg="#7acbe6", foreground="black", font=regular, command=exportar)
    exportar_button.pack(padx=5)
    
    # Botão para fechar a janela
    tk.Button(janela, text="Fechar", bg="#dc3545", font=regular, command=janela.destroy).pack(pady=10)

    return janela
