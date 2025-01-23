import re
from termcolor import colored

def obter_nome_tabela():
    while True:
        tabela = input("Informe o nome da tabela: ").strip()
        if re.match("^[A-Za-z_][A-Za-z0-9_]*$", tabela):
            return tabela
        else:
            print(colored("Nome de tabela inválido. Tente novamente.", "red"))

def obter_colunas_valores():
    colunas = []
    valores = []
    while True:
        coluna = input("Informe o nome da coluna (ou deixe vazio para finalizar): ").strip()
        if not coluna:
            break
        if not re.match("^[A-Za-z_][A-Za-z0-9_]*$", coluna):
            print(colored("Nome de coluna inválido. Tente novamente.", "red"))
            continue
        valor = input(f"Informe o valor para '{coluna}': ").strip()
        colunas.append(coluna)
        valores.append(valor)
    return colunas, valores

def gerar_insert():
    tabela = obter_nome_tabela()
    colunas, valores = obter_colunas_valores()
    if not colunas:
        print(colored("Nenhuma coluna informada. Operação cancelada.", "red"))
        return
    colunas_str = ", ".join(colunas)
    valores_str = ", ".join(f"'{v}'" for v in valores)
    insert_sql = f"INSERT INTO {tabela} ({colunas_str}) VALUES ({valores_str});"
    print(colored("\nScript INSERT gerado:", "green"))
    print(insert_sql)

def gerar_update():
    tabela = obter_nome_tabela()
    colunas, valores = obter_colunas_valores()
    if not colunas:
        print(colored("Nenhuma coluna informada. Operação cancelada.", "red"))
        return
    set_clauses = ", ".join(f"{colunas[i]} = '{valores[i]}'" for i in range(len(colunas)))
    condicao = input("Informe a condição WHERE para o UPDATE (e.g., id = 1): ").strip()
    if not condicao:
        print(colored("Condição WHERE não informada. Operação cancelada.", "red"))
        return
    update_sql = f"UPDATE {tabela} SET {set_clauses} WHERE {condicao};"
    print(colored("\nScript UPDATE gerado:", "green"))
    print(update_sql)

def gerar_delete():
    tabela = obter_nome_tabela()
    condicao = input("Informe a condição WHERE para o DELETE (e.g., id = 1): ").strip()
    if not condicao:
        print(colored("Condição WHERE não informada. Operação cancelada.", "red"))
        return
    delete_sql = f"DELETE FROM {tabela} WHERE {condicao};"
    print(colored("\nScript DELETE gerado:", "green"))
    print(delete_sql)

def menu_gerador_scripts():
    while True:
        print(colored("\nGerador de Scripts SQL", "cyan"))
        print("1. Gerar script INSERT")
        print("2. Gerar script UPDATE")
        print("3. Gerar script DELETE")
        print("0. Voltar ao menu anterior")
        escolha = input("Selecione uma opção: ").strip()
        if escolha == "1":
            gerar_insert()
        elif escolha == "2":
            gerar_update()
        elif escolha == "3":
            gerar_delete()
        elif escolha == "0":
            break
        else:
            print(colored("Opção inválida. Tente novamente.", "red"))

# Para integrar este menu ao seu programa principal, chame a função menu_gerador_scripts()
# no ponto apropriado do seu código.