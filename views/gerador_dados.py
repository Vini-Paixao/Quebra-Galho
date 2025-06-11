import tkinter as tk
from tkinter import ttk, messagebox, filedialog, font
import pandas as pd
from faker import Faker
from utilidades import resource_path, ICONS


def gerador_dados_interface():
    fake = Faker("pt_BR")
    campos_disponiveis = {
        "Nome": "name",
        "Email": "email",
        "Endereço": "address",
        "Telefone": "phone_number",
        "CPF": "cpf",
        "CNPJ": "cnpj",
        "Data": "date",
        "Texto Aleatório": "text",
        "Cidade": "city",
        "Estado": "estado",
    }
    campos_adicionados = []

    def mostrar_ajuda_regras():
        ajuda_janela = tk.Toplevel()
        ajuda_janela.title("Ajuda - Regras Personalizadas")
        ajuda_janela.geometry("450x480")
        ajuda_janela.minsize(450, 480)
        ajuda_janela.iconbitmap(resource_path("icon.ico"))

        main_frame = ttk.Frame(ajuda_janela, padding=20)
        main_frame.pack(expand=True, fill="both")

        texto_ajuda = """
1. Data:
   Formato: YYYY-MM-DD-YYYY-MM-DD
   Exemplo: 2020-01-01-2023-12-31

2. Texto Aleatório:
   Número máximo de caracteres.
   Exemplo: 200

3. Email:
   Domínio personalizado, sem o "@".
   Exemplo: empresa.com.br

4. Telefone / CPF / CNPJ:
   Não requerem regras, são gerados automaticamente.
"""

        ttk.Label(
            main_frame, text="Regras Opcionais", font=("Segoe UI", 14, "bold")
        ).pack(pady=(0, 15))

        # CORREÇÃO: Usando ttk.Label para garantir a visibilidade do texto
        help_label = ttk.Label(main_frame, text=texto_ajuda, justify=tk.LEFT)
        help_label.pack(expand=True, fill="both")

        ttk.Button(
            main_frame,
            text="Fechar",
            style="Accent.TButton",
            command=ajuda_janela.destroy,
        ).pack(side="bottom", pady=(15, 0))

    def adicionar_campo():
        nome = campo_var.get()
        if not nome:
            messagebox.showwarning("Aviso", "Selecione um tipo de campo.")
            return

        tipo = campos_disponiveis[nome]
        regra = regra_entry.get().strip()

        campos_adicionados.append({"nome": nome, "tipo": tipo, "regra": regra or None})
        atualizar_lista_campos()
        regra_entry.delete(0, tk.END)

    def remover_campo_selecionado():
        selecionados = lista_campos.curselection()
        if not selecionados:
            messagebox.showwarning("Aviso", "Selecione um campo da lista para remover.")
            return

        # Remove os itens em ordem reversa para não bagunçar os índices
        for index in sorted(selecionados, reverse=True):
            campos_adicionados.pop(index)

        atualizar_lista_campos()

    def atualizar_lista_campos():
        lista_campos.delete(0, tk.END)
        for campo in campos_adicionados:
            display = f"{campo['nome']}"
            if campo["regra"]:
                display += f"  |  Regra: {campo['regra']}"
            lista_campos.insert(tk.END, display)

    def gerar_e_salvar_dados():
        try:
            num_linhas = int(linhas_entry.get())
            if not 0 < num_linhas <= 500000:
                raise ValueError
        except ValueError:
            messagebox.showwarning(
                "Aviso", "Número de linhas inválido! (deve ser entre 1 e 500.000)"
            )
            return

        if not campos_adicionados:
            messagebox.showwarning("Aviso", "Adicione pelo menos um campo!")
            return

        dados = []
        for _ in range(num_linhas):
            linha = {}
            for campo in campos_adicionados:
                try:
                    valor = getattr(fake, campo["tipo"])()  # Gera um valor padrão
                    if campo["regra"]:
                        if campo["tipo"] == "date":
                            inicio, fim = campo["regra"].split("-", 1)
                            valor = fake.date_between(start_date=inicio, end_date=fim)
                        elif campo["tipo"] == "email":
                            valor = f"{fake.user_name().lower().replace(' ', '.')}@{campo['regra']}"
                        elif campo["tipo"] == "text":
                            valor = fake.text(max_nb_chars=int(campo["regra"]))
                    linha[campo["nome"]] = valor
                except Exception:
                    linha[campo["nome"]] = "ERRO"
            dados.append(linha)

        df = pd.DataFrame(dados)
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel", "*.xlsx"), ("CSV", "*.csv"), ("XML", "*.xml")],
        )
        if file_path:
            try:
                if file_path.endswith(".csv"):
                    df.to_csv(file_path, index=False, sep=";", decimal=",")
                elif file_path.endswith(".xml"):
                    df.to_xml(
                        file_path,
                        index=False,
                        root_name="registros",
                        row_name="registro",
                    )
                else:
                    df.to_excel(file_path, index=False)
                messagebox.showinfo("Sucesso", f"Dados salvos em:\n{file_path}")
            except Exception as e:
                messagebox.showerror(
                    "Erro ao Salvar", f"Falha ao salvar o arquivo:\n{e}"
                )

    # --- JANELA PRINCIPAL ---
    janela = tk.Toplevel()
    janela.title("Gerador de Dados Fictícios")
    janela.geometry("600x550")
    janela.minsize(600, 550)
    janela.iconbitmap(resource_path("icon.ico"))

    main_frame = ttk.Frame(janela, padding=20)
    main_frame.pack(expand=True, fill="both")

    config_frame = ttk.Labelframe(main_frame, text="Configurações", padding=15)
    config_frame.pack(fill="x")
    config_frame.columnconfigure(1, weight=1)

    ttk.Label(config_frame, text="Linhas:").grid(
        row=0, column=0, sticky="w", padx=(0, 5), pady=5
    )
    linhas_entry = ttk.Entry(config_frame, width=12)
    linhas_entry.grid(row=0, column=1, sticky="w", pady=5)
    linhas_entry.insert(0, "100")

    ttk.Label(config_frame, text="Campo:").grid(
        row=1, column=0, sticky="w", padx=(0, 5), pady=5
    )
    campo_var = tk.StringVar()
    campos_combo = ttk.Combobox(
        config_frame,
        textvariable=campo_var,
        values=list(campos_disponiveis.keys()),
        state="readonly",
    )
    campos_combo.grid(row=1, column=1, sticky="ew", pady=5)

    ttk.Label(config_frame, text="Regra (Opcional):").grid(
        row=2, column=0, sticky="w", padx=(0, 5), pady=5
    )
    regra_entry = ttk.Entry(config_frame)
    regra_entry.grid(row=2, column=1, sticky="ew", pady=5)
    btn_ajuda = ttk.Button(
        config_frame,
        image=ICONS.get("ajuda", tk.PhotoImage()),
        command=mostrar_ajuda_regras,
    )
    btn_ajuda.grid(row=2, column=2, padx=5)

    add_remove_frame = ttk.Frame(main_frame)
    add_remove_frame.pack(fill="x", pady=10)
    ttk.Button(
        add_remove_frame,
        text="Adicionar Campo",
        image=ICONS.get("add", tk.PhotoImage()),
        compound="left",
        command=adicionar_campo,
    ).pack(side="left", expand=True, fill="x", padx=(0, 5))
    ttk.Button(
        add_remove_frame,
        text="Remover",
        image=ICONS.get("limpar", tk.PhotoImage()),
        compound="left",
        command=remover_campo_selecionado,
    ).pack(side="left", expand=True, fill="x", padx=(5, 0))

    ttk.Label(
        main_frame, text="Campos Adicionados:", font=("Segoe UI", 10, "bold")
    ).pack(fill="x", pady=(10, 5))
    lista_campos = tk.Listbox(
        main_frame, height=8, relief="solid", borderwidth=1, selectmode="extended"
    )
    lista_campos.pack(expand=True, fill="both")

    botoes_finais_frame = ttk.Frame(main_frame)
    botoes_finais_frame.pack(side="bottom", fill="x", pady=(20, 0))
    ttk.Button(
        botoes_finais_frame,
        text="Voltar",
        image=ICONS.get("voltar2", tk.PhotoImage()),
        compound="left",
        command=janela.destroy,
    ).pack(side="right")
    ttk.Button(
        botoes_finais_frame,
        text="Gerar Dados e Salvar",
        style="Accent.TButton",
        image=ICONS.get("executar", tk.PhotoImage()),
        compound="left",
        command=gerar_e_salvar_dados,
    ).pack(side="right", padx=10)

    return janela
