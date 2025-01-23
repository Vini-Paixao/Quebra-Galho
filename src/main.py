import sys
import os
from termcolor import colored
from alinhar_valores import alinhar_valores
from converter_data import converter_data
from menu_sql import menu_sql
import re
import colorama
colorama.init()


if sys.platform == "win32":
    os.system('chcp 65001 > nul')  # Define o terminal para UTF-8


def extrair_numeros(texto):
    return re.sub(r'\D', '', texto)


def menu():
    titulo = "Quebra Galho"
    largura = 30
    paddingTitulo = (largura - len(titulo)) // 2

    while True:
        # Início do menu com bordas e título
        print(colored("\n\t╔", "blue"), end="")
        print(colored("═" * largura, "blue"), end="")
        print(colored("╗", "blue"))

        print(colored("\t║", "blue"), end="")
        print(" " * paddingTitulo, end="")
        print(colored(titulo, "blue"), end="")
        print(" " * (largura - paddingTitulo - len(titulo)), end="")
        print(colored("║", "blue"))

        print(colored("\t╠", "blue"), end="")
        print(colored("═" * largura, "blue"), end="")
        print(colored("╣", "blue"))

        # Opções do menu
        print(colored("\t║     1 - Valores em Linha     ║", "blue"))
        print(colored("\t║     2 - Limpar Formatação    ║", "blue"))
        print(colored("\t║     3 - Converter Data       ║", "blue"))
        print(colored("\t║     4 - Funções SQL          ║", "blue"))
        print(colored("\t║     0 - Encerrar             ║", "blue"))

        print(colored("\t╚", "blue"), end="")
        print(colored("═" * largura, "blue"), end="")
        print(colored("╝", "blue"))

        # Entrada do usuário
        escolha = input("\nSelecione uma opção: ")

        if escolha == "1":
            alinhar_valores()

        elif escolha == "2":
            print(
                colored(
                    "\nUse as teclas de atalho 'CTRL + SHIFT + C' para copiar e/ou 'CTRL + SHIFT + V' para colar",
                    "green"))
            print("\nInforme o valor a retirar a formatação: ")
            numero_formatado = input()
            if numero_formatado == "":
                print(colored("Nenhum valor foi fornecido.", "red"))
            else:
                numero_limpo = extrair_numeros(numero_formatado)
                print("\nNúmero sem formatação: " + numero_limpo)
            extrair_numeros(numero_formatado)

        elif escolha == "3":
            print(colored("As datas serão convertidas no modelo americano, para datas sem ano estipulado, será adicionado o ano atual automaticamente.","green"))
            data_input = input(
                "\nInforme a data (formatos aceitos: DD/MM/YYYY, DD/MM, DDMMYYYY, DDMM): "
            )
            try:
                data_convertida = converter_data(data_input)
                print(
                    colored(
                        f"\nData convertida para o padrão americano: {data_convertida}",
                        "green"))
            except ValueError as e:
                print(colored(f"\nErro: {e}", "red"))

        elif escolha == "4":
            menu_sql()

        elif escolha == "0":
            print(
                colored(
                    "\nPrograma desenvolvido por Marcus Paixão, obrigado por usar! :)",
                    "green"))
            print(colored("\nEncerrado.", "red"))
            sys.exit()
        else:
            print(colored("\nOpção inválida. Tente novamente.", "red"))


if __name__ == "__main__":
    menu()
