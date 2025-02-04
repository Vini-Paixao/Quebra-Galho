import tkinter as tk
from tkinter import ttk, messagebox, filedialog, font
import pandas as pd
from faker import Faker

from utilidades import resource_path

def mostrar_ajuda_regras():
    ajuda_janela = tk.Toplevel()
    ajuda_janela.title("Ajuda - Regras Personalizadas")
    ajuda_janela.geometry("450x530")
    ajuda_janela.minsize(450, 530)
    ajuda_janela.iconbitmap(resource_path('icon.ico'))  # Caminho corrigido

    
    texto_ajuda = """
    Como usar as regras opcionais para cada campo:

    1. Data:
       Formato: data_inicial-data_final
       Exemplo: 2020-01-01-2023-12-31

    2. Texto Aleatório:
       Número de caracteres ou frases
       Exemplo: 200 (200 caracteres) ou 5 (5 frases)

    3. Email:
       Domínio personalizado
       Exemplo: @empresa.com.br

    4. Telefone:
       Máscara personalizada
       Exemplo: (##) 9####-####

    5. Campos numéricos (CPF/CNPJ):
       Não requerem regras - geram automaticamente

    Dica: Deixe em branco para usar valores padrão!
    """
    
    tk.Label(ajuda_janela, text="Instruções para Regras Personalizadas", font=("Verdana", 14, "bold")).pack(pady=10)
    tk.Message(ajuda_janela, text=texto_ajuda, width=550, font=("Verdana", 10)).pack(padx=20, pady=10)
    tk.Button(ajuda_janela, text="Fechar", bg="red", command=ajuda_janela.destroy).pack(pady=10)

def gerador_dados_interface():
    fake = Faker('pt_BR')
    campos_disponiveis = {
        'Nome': 'name',
        'Email': 'email',
        'Endereço': 'address',
        'Telefone': 'phone_number',
        'CPF': 'cpf',
        'CNPJ': 'cnpj',
        'Data': 'date',
        'Texto Aleatório': 'text',
        'Cidade': 'city',
        'Estado': 'estado'
    }

    campos_adicionados = []

    def adicionar_campo():
        nome = campo_var.get()
        tipo = campos_disponiveis[nome]
        regra = regra_entry.get().strip()
        
        if nome and tipo:
            campos_adicionados.append({
                'nome': nome,
                'tipo': tipo,
                'regra': regra if regra else None
            })
            atualizar_lista_campos()
            regra_entry.delete(0, tk.END)

    def remover_campo():
        selecionado = lista_campos.curselection()
        if selecionado:
            campos_adicionados.pop(selecionado[0])
            atualizar_lista_campos()

    def atualizar_lista_campos():
        lista_campos.delete(0, tk.END)
        for campo in campos_adicionados:
            display = f"{campo['nome']} ({campo['tipo']})"
            if campo['regra']:
                display += f" | Regra: {campo['regra']}"
            lista_campos.insert(tk.END, display)

    def gerar_dados():
        try:
            num_linhas = int(linhas_entry.get())
            if num_linhas <= 0:
                raise ValueError
        except:
            messagebox.showwarning("Aviso", "Número de linhas inválido!")
            return

        if not campos_adicionados:
            messagebox.showwarning("Aviso", "Adicione pelo menos um campo!")
            return

        dados = []
        for _ in range(num_linhas):
            linha = {}
            for campo in campos_adicionados:
                try:
                    if campo['regra']:
                        if campo['tipo'] == 'date':
                            linha[campo['nome']] = fake.date_between(start_date=campo['regra'].split('-')[0], end_date=campo['regra'].split('-')[1])
                        else:
                            linha[campo['nome']] = getattr(fake, campo['tipo'])(campo['regra'])
                    else:
                        linha[campo['nome']] = getattr(fake, campo['tipo'])()
                except:
                    linha[campo['nome']] = "ERRO NA GERAÇÃO"
            dados.append(linha)

        df = pd.DataFrame(dados)
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel", "*.xlsx"), ("CSV", "*.csv"), ("XML", "*.xml")]
        )
        
        if file_path:
            try:
                if file_path.endswith('.csv'):
                    df.to_csv(file_path, index=False)
                elif file_path.endswith('.xml'):
                    df.to_xml(file_path, index=False)
                else:
                    df.to_excel(file_path, index=False)
                
                messagebox.showinfo("Sucesso", f"Dados gerados e salvos em:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao salvar arquivo:\n{str(e)}")

    # Janela principal
    janela = tk.Toplevel()
    janela.title("Gerador de Dados Fictícios")
    janela.geometry("700x530")
    janela.minsize(700, 530)
    janela.iconbitmap(resource_path('icon.ico'))  # Caminho corrigido
    janela.configure(bg='lightblue')

    # Fontes
    bold = font.Font(family="Verdana", size=12, weight="bold")
    regular = font.Font(family="Verdana", size=10, weight="normal")

    # Widgets
    tk.Label(janela, text="Quantidade de Linhas:", font=bold, bg='lightblue').pack(pady=5)
    linhas_entry = tk.Entry(janela, font=regular, width=10)
    linhas_entry.pack()
    linhas_entry.insert(0, "100")

    tk.Label(janela, text="Selecione o Campo:", font=bold, bg='lightblue').pack(pady=5)
    campo_var = tk.StringVar()
    campos_combo = ttk.Combobox(janela, textvariable=campo_var, values=list(campos_disponiveis.keys()), font=regular)
    campos_combo.pack()
    campos_combo.current(0)

    regra_frame = tk.Frame(janela, bg='lightblue')
    regra_frame.pack(pady=5)
    
    tk.Label(regra_frame, text="Regra Opcional (ex: para datas use '2020-01-01-2023-12-31'):", 
             font=regular, bg='lightblue').pack(side=tk.LEFT)
    
    # Botão de ajuda
    help_canvas = tk.Canvas(regra_frame, width=22, height=22, bg='lightblue', highlightthickness=0)
    help_canvas.pack(side=tk.LEFT, padx=3)

    # Desenhar o círculo com borda
    help_canvas.create_oval(
        1, 1, 21, 21,  # Coordenadas do círculo (x0, y0, x1, y1)
        outline="black", 
        fill="yellow", 
        width=1
    )

    # Texto de interrogação
    help_canvas.create_text(
        11, 11,  # Centro do canvas
        text="?", 
        font=("Verdana", 10, "bold"),
        fill="black"
    )

    # Evento de clique
    help_canvas.bind("<Button-1>", lambda e: mostrar_ajuda_regras())

    # Efeito hover básico
    def on_enter(e):
        help_canvas.itemconfig(1, fill="#ffff00")  # Amarelo mais forte

    def on_leave(e):
        help_canvas.itemconfig(1, fill="yellow")

    help_canvas.bind("<Enter>", on_enter)
    help_canvas.bind("<Leave>", on_leave)
    
    regra_entry = tk.Entry(janela, font=regular, width=50)
    regra_entry.pack()
    
    tk.Button(janela, text="Adicionar Campo", font=regular, command=adicionar_campo).pack(pady=5)
    tk.Button(janela, text="Remover Campo Selecionado", font=regular, command=remover_campo).pack(pady=5)

    tk.Label(janela, text="Campos Adicionados:", font=bold, bg='lightblue').pack(pady=5)
    lista_campos = tk.Listbox(janela, width=80, height=8, font=regular)
    lista_campos.pack()

    tk.Button(janela, text="Gerar Dados e Salvar", font=bold, bg="lightgreen", command=gerar_dados).pack(pady=15)
    tk.Button(janela, text="Fechar", font=regular, bg="#dc3545", command=janela.destroy).pack(pady=5)

    janela.mainloop()