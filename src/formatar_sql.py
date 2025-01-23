import sqlparse
from termcolor import colored

def formatar_sql():
    print("Insira as consultas SQL a serem formatadas (pressione Enter em uma linha vazia para finalizar):")
    linhas = []
    while True:
        linha = input()
        if linha.strip() == "":
            break
        linhas.append(linha)

    consultas = "\n".join(linhas)
    if not consultas.strip():
        print(colored("Nenhuma consulta SQL foi fornecida.", "red"))
        return

    # Divide as consultas em instruções individuais
    instrucoes = sqlparse.split(consultas)

    consultas_formatadas = []
    for instrucao in instrucoes:
        consulta_formatada = sqlparse.format(instrucao, reindent=True, keyword_case='upper')
        consultas_formatadas.append(consulta_formatada)

    print(colored("\nConsultas SQL formatadas:", "green"))
    for consulta in consultas_formatadas:
        print(consulta)
        print('-' * 50)  # Separador entre consultas formatadas