import re
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import font

from utilidades import resource_path

def converter_data_interface():
    def processar():
        data_input = entrada.get()
        try:
            data_convertida = converter_data(data_input)
            resultado_entry.configure(state="normal")  # Habilita edição para inserir o texto
            resultado_entry.delete(0, tk.END)  # Limpa qualquer texto existente
            resultado_entry.insert(0, data_convertida)  # Insere a data convertida
            resultado_entry.configure(state="readonly")  # Volta para somente leitura
        except ValueError as e:
            messagebox.showerror("Erro", f"Formato de data inválido: {e}")

    janela = tk.Toplevel()
    janela.title("Converter Data")
    janela.geometry("450x220")
    janela.minsize(450, 220)
    janela.iconbitmap(resource_path('icon.ico'))  # Caminho corrigido
    janela.configure(bg='#bc7ff6')
    
    bold = font.Font(family="Verdana", size=16, weight="bold")
    regular = font.Font(family="Verdana", size=10, weight="normal")

    tk.Label(janela, text="Informe a Data:", font=bold, bg='#bc7ff6').pack(pady=5)
    tk.Label(janela, text="Valores aceitos - DD/MM/YYYY, DD/MM, DDMMYYYY, DDMM", font=regular, bg='#bc7ff6').pack(pady=5)

    entrada = tk.Entry(janela, width=50, font=regular)
    entrada.pack(pady=5)

    btn_processar = tk.Button(janela, text="Processar", bg="#67d167", font=regular, command=processar)
    btn_processar.pack(pady=5)

    # Campo para exibir o resultado
    resultado_entry = tk.Entry(janela, width=50, state="readonly", font=regular, readonlybackground="white", fg="black")
    resultado_entry.pack(pady=5)
    
    # Botão para fechar a janela
    btn_encerrar = tk.Button(janela, text="Fechar", bg="#dc3545", font=regular, command=janela.destroy)
    btn_encerrar.pack(pady=5)

    janela.mainloop()

def converter_data(data_input):
    """
    Converte uma data fornecida em vários formatos para o padrão americano YYYY-MM-DD.
    Aceita os seguintes formatos de entrada:
    - DD/MM/YYYY
    - DD/MM
    - DDMMYYYY
    - DDMM
    """
    data_input = data_input.strip()
    ano_atual = datetime.now().year

    # Expressões regulares para diferentes formatos de data
    formatos = [
        (r'^(\d{2})/(\d{2})/(\d{4})$', '%d/%m/%Y'),  # DD/MM/YYYY
        (r'^(\d{2})/(\d{2})$', '%d/%m'),  # DD/MM
        (r'^(\d{2})(\d{2})(\d{4})$', '%d%m%Y'),  # DDMMYYYY
        (r'^(\d{2})(\d{2})$', '%d%m')  # DDMM
    ]

    for regex, date_format in formatos:
        match = re.match(regex, data_input)
        if match:
            try:
                data = datetime.strptime(data_input, date_format)
                # Se o formato não inclui o ano, adiciona o ano atual
                if '%Y' not in date_format:
                    data = data.replace(year=ano_atual)
                return data.strftime('%Y-%m-%d')
            except ValueError:
                continue

    raise ValueError(f"Formato de data inválido: {data_input}")
