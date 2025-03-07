import tkinter as tk
from tkinter import messagebox
from tkinter import font

from utilidades import resource_path

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
            linhas = list(dict.fromkeys(linhas))  # Remove duplicatas mantendo a ordem

        delimitador = delimitador_var.get()
        resultado = delimitador.join(linhas)
        resultado_entry.configure(state="normal")  # Habilita edição para inserir o texto
        resultado_entry.delete(0, tk.END)  # Limpa qualquer texto existente
        resultado_entry.insert(0, resultado)  # Insere o texto formatado
        resultado_entry.configure(state="readonly")  # Volta para somente leitura
    
    def limpar_entrada():
        """Limpa o conteúdo do campo de entrada."""
        text_area.delete("1.0", tk.END)

    janela = tk.Toplevel()
    janela.title("Alinhar Valores")
    janela.geometry("550x440")
    janela.minsize(550, 440)
    janela.iconbitmap(resource_path('icon.ico'))
    janela.configure(bg='#7acbe6')
    
    # Fontes
    bold = font.Font(family="Verdana", size=12, weight="bold")
    regular = font.Font(family="Verdana", size=10, weight="normal")

    instrucao_label = tk.Label(janela, text="Informe os valores, um por linha, e clique em 'Alinhar':", font=bold, bg='#7acbe6')
    instrucao_label.pack(pady=5)

    text_area = tk.Text(janela, width=60, height=10, font=regular)
    text_area.pack(pady=5)

    # Opções de delimitador
    delimitador_label = tk.Label(janela, text="Escolha o delimitador:", font=regular, bg='#7acbe6')
    delimitador_label.pack(pady=5)

    delimitador_var = tk.StringVar(value=",")  # Valor padrão é vírgula
    delimitadores = [",", ";", "|", "/", "\\", "-"]
    delimitador_menu = tk.OptionMenu(janela, delimitador_var, *delimitadores)
    delimitador_menu.config(font=regular)
    delimitador_menu.pack(pady=5)

    # Checkbox para remover duplicatas
    remover_duplicatas_var = tk.BooleanVar()
    remover_duplicatas_check = tk.Checkbutton(janela, text="Remover duplicatas", variable=remover_duplicatas_var, font=regular, bg='#7acbe6')
    remover_duplicatas_check.pack(pady=5)
    
    frame = tk.Frame(janela, bg='#7acbe6')
    frame.pack(pady=5)
    
    alinhar_button = tk.Button(frame, text="Alinhar", bg="#67d167", font=regular, command=alinhar)
    alinhar_button.pack(side=tk.LEFT, pady=5)
    
    # Botão para limpar o campo de entrada
    tk.Button(frame, text="Limpar Entrada", bg="#f0ad4e", font=regular, command=limpar_entrada).pack(side=tk.LEFT, padx=5)

    # Campo de entrada para o resultado
    resultado_entry = tk.Entry(janela, width=60, state="readonly", font=regular, readonlybackground="white", fg="black")
    resultado_entry.pack(pady=5)
    
    # Botão para fechar a janela
    tk.Button(janela, text="Fechar", bg="#dc3545", font=regular, command=janela.destroy).pack(pady=5)
    
    return janela