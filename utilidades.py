import os
import sys
import webbrowser
import tkinter as tk
from tkinter import messagebox

def resource_path(relative_path):
    """Retorna o caminho absoluto para o recurso, necessário para PyInstaller."""
    try:
        base_path = sys._MEIPASS  # Pasta temporária do PyInstaller
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def abrir_url(url):
    webbrowser.open_new(url)
    

# Dicionário global para armazenar referências às janelas abertas
telas_abertas = {}

def open_tela(chave, criar_func):
    """
    Abre uma tela se ela não estiver aberta.
    
    :param chave: Identificador único para a tela.
    :param criar_func: Função que cria e retorna a nova janela.
    :return: A janela criada ou já existente.
    """
    if chave in telas_abertas and telas_abertas[chave].winfo_exists():
        if chave == 'menu_datas' or chave == 'menu_sql':
            messagebox.showinfo("Aviso", f"O sub-menu '{chave}' já está aberto.")
            telas_abertas[chave].lift()  # Traz a janela para frente
            return telas_abertas[chave]
        else:
            messagebox.showinfo("Aviso", f"A tela '{chave}' já está aberta.")
            telas_abertas[chave].lift()  # Traz a janela para frente
            return telas_abertas[chave]
    
    # Cria a nova janela
    nova_tela = criar_func()
    telas_abertas[chave] = nova_tela

    # Quando a janela for fechada, remova sua referência do dicionário
    nova_tela.protocol("WM_DELETE_WINDOW", lambda chave=chave: fechar_tela(chave))
    return nova_tela

def fechar_tela(chave):
    """
    Fecha a tela e remove sua referência do dicionário.
    
    :param chave: Identificador da tela a ser fechada.
    """
    if chave in telas_abertas:
        telas_abertas[chave].destroy()
        del telas_abertas[chave]
