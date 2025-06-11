import re
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

from utilidades import resource_path, ICONS


def converter_data_interface():
    def processar():
        data_input = entrada.get()
        if not data_input:
            messagebox.showwarning("Aviso", "Por favor, informe uma data.")
            return
        try:
            data_convertida = converter_data(data_input)
            resultado_entry.configure(state="normal")
            resultado_entry.delete(0, tk.END)
            resultado_entry.insert(0, data_convertida)
            resultado_entry.configure(state="readonly")
        except ValueError as e:
            messagebox.showerror("Erro de Formato", str(e))

    def limpar_campos():
        entrada.delete(0, tk.END)
        resultado_entry.configure(state="normal")
        resultado_entry.delete(0, tk.END)
        resultado_entry.configure(state="readonly")

    janela = tk.Toplevel()
    janela.title("Converter Data")
    janela.geometry("420x350")
    janela.minsize(420, 350)
    janela.iconbitmap(resource_path("icon.ico"))

    main_frame = ttk.Frame(janela, padding=20)
    main_frame.pack(expand=True, fill="both")

    # --- Título e Descrição ---
    ttk.Label(main_frame, text="Converter Data", font=("Segoe UI", 14, "bold")).pack(
        fill="x"
    )
    ttk.Label(
        main_frame,
        text="Valores aceitos: DD/MM/YYYY, DD/MM, DDMMYYYY, DDMM",
        wraplength=380,
    ).pack(fill="x", pady=(0, 15))

    # --- Entrada de Dados ---
    ttk.Label(main_frame, text="Informe a data:", font=("Segoe UI", 10, "bold")).pack(
        fill="x", pady=(5, 5)
    )
    entrada = ttk.Entry(main_frame, width=50)
    entrada.pack(fill="x")

    # --- Resultado ---
    ttk.Label(
        main_frame, text="Resultado (YYYY-MM-DD):", font=("Segoe UI", 10, "bold")
    ).pack(fill="x", pady=(15, 5))
    resultado_entry = ttk.Entry(main_frame, width=50, state="readonly")
    resultado_entry.pack(fill="x")

    # --- Botões de Ação ---
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
        command=limpar_campos,
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


def converter_data(data_input):
    """
    Converte uma data fornecida em vários formatos para o padrão americano YYYY-MM-DD.
    Aceita os seguintes formatos de entrada: DD/MM/YYYY, DD/MM, DDMMYYYY, DDMM.
    """
    data_input = data_input.strip()
    ano_atual = datetime.now().year

    formatos = [
        (r"^\d{2}/\d{2}/\d{4}$", "%d/%m/%Y"),
        (r"^\d{2}/\d{2}$", "%d/%m"),
        (r"^\d{8}$", "%d%m%Y"),
        (r"^\d{4}$", "%d%m"),
    ]

    for regex, date_format in formatos:
        if re.match(regex, data_input):
            try:
                # Trata o caso de DDMMYY sem separador, que pode ser confundido com DDMMYYYY
                if date_format == "%d%m%Y" and len(data_input) == 6:
                    data = datetime.strptime(data_input, "%d%m%y")
                else:
                    data = datetime.strptime(data_input, date_format)

                if "%Y" not in date_format and "%y" not in date_format:
                    data = data.replace(year=ano_atual)

                return data.strftime("%Y-%m-%d")
            except ValueError:
                continue  # Tenta o próximo formato

    raise ValueError(f"Formato de data '{data_input}' não reconhecido.")
