import tkinter as tk
from tkinter import messagebox
from tkinter import font

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

        resultado = ",".join(linhas)
        resultado_entry.configure(state="normal")  # Habilita edição para inserir o texto
        resultado_entry.delete(0, tk.END)  # Limpa qualquer texto existente
        resultado_entry.insert(0, resultado)  # Insere o texto formatado
        resultado_entry.configure(state="readonly")  # Volta para somente leitura

    janela = tk.Toplevel()
    janela.title("Alinhar Valores")
    janela.geometry("550x320")
    janela.configure(bg='lightblue')
    
    # Fontes
    bold = font.Font(family="Verdana", size=12, weight="bold")
    regular = font.Font(family="Verdana", size=10, weight="normal")

    instrucao_label = tk.Label(janela, text="Informe os valores, um por linha, e clique em 'Alinhar':", font=bold, bg='lightblue')
    instrucao_label.pack(pady=5)

    text_area = tk.Text(janela, width=60, height=10,font=regular)
    text_area.pack(pady=5)

    alinhar_button = tk.Button(janela, text="Alinhar", font=regular, command=alinhar)
    alinhar_button.pack(pady=5)

    # Campo de entrada para o resultado
    resultado_entry = tk.Entry(janela, width=60, state="readonly", font=regular, readonlybackground="white", fg="black")
    resultado_entry.pack(pady=5)
    
    # Botão para fechar a janela
    tk.Button(janela, text="Fechar", font=regular, command=janela.destroy).pack(pady=5)

    janela.mainloop()