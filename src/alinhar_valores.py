from termcolor import colored


def alinhar_valores():
    print(colored(
        "\nUse as teclas de atalho 'CTRL + SHIFT + C' para copiar e/ou 'CTRL + SHIFT + V' para colar","green"
    ))
    print(
        "\nInforme os valores um em baixo do outro e aperte 'Enter' em uma linha vazia para alinhar os valores."
    )
    valores = []

    while True:
        entrada = input()
        if entrada.strip() == "":
            break
        valores.append(entrada.strip())

    if valores:
        print("Valores em linha: " + ",".join(valores))
    else:
        print(colored("Nenhum valor foi fornecido.","red"))
