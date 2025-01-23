from termcolor import colored
from validar_sintaxe import capturar_entrada_sql, validar_sintaxe_sql
from gerador_scripts import menu_gerador_scripts
from formatar_sql import formatar_sql


def menu_sql():
    titulo = "Scripts SQL"
    largura = 32
    paddingTitulo = (largura - len(titulo)) // 2

    while True:
        # Início do menu com bordas e título
        print(colored("\n\t╔", "green"), end="")
        print(colored("═" * largura, "green"), end="")
        print(colored("╗", "green"))

        print(colored("\t║", "green"), end="")
        print(" " * paddingTitulo, end="")
        print(colored(titulo, "green"), end="")
        print(" " * (largura - paddingTitulo - len(titulo)), end="")
        print(colored("║", "green"))

        print(colored("\t╠", "green"), end="")
        print(colored("═" * largura, "green"), end="")
        print(colored("╣", "green"))

        # Opções do menu
        print(colored("\t║   1 - Validador de Sintaxe     ║", "green"))
        print(colored("\t║   2 - Gerador de Scripts       ║", "green"))
        print(colored("\t║   3 - Formatação de Consultas  ║", "green"))
        print(colored("\t║   0 - Voltar                   ║", "green"))

        print(colored("\t╚", "green"), end="")
        print(colored("═" * largura, "green"), end="")
        print(colored("╝", "green"))

        # Entrada do usuário
        escolha = input("\nSelecione uma opção: ")

        if escolha == "1":
            consulta = capturar_entrada_sql()
            if consulta.strip():
                resultado_validacao = validar_sintaxe_sql(consulta)
                print(resultado_validacao)
            else:
                print(colored("Nenhuma consulta SQL foi fornecida.","red"))

        elif escolha == "2":
            menu_gerador_scripts()

        elif escolha == "3":
            formatar_sql()

        elif escolha == "4":
            print("Em Desenvolvimento")

        elif escolha == "0":
            print(colored("\nVoltando ao menu principal...", "cyan"))
            return  # Sai do menu_sql para o menu principal
        else:
            print(colored("\nOpção inválida. Tente novamente.", "red"))
