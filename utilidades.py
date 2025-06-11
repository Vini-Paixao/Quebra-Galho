import os
import sys
import webbrowser
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# --- DICIONÁRIO GLOBAL E FUNÇÃO PARA CARREGAR ÍCONES ---
ICONS = {}


def resource_path(relative_path):
    """Retorna o caminho absoluto para o recurso, necessário para PyInstaller."""
    try:
        base_path = getattr(
            sys, "_MEIPASS", os.path.abspath(".")
        )  # Pasta temporária do PyInstaller ou diretório atual
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def load_icons():
    """Carrega todos os ícones da aplicação."""
    if ICONS:  # Não recarregar se já foram carregados
        return

    icon_names = {
        "valores": "btnicon_valores.png",
        "formatacao": "btnicon_formatacao.png",
        "dados": "btnicon_dados.png",
        "json_xml": "btnicon_json_xml.png",
        "datas": "btnicon_datas.png",
        "sql": "btnicon_sql.png",
        "site": "btnicon_site.png",
        "github": "btnicon_github.png",
        "sintaxe": "btnicon_sintaxe.png",
        "scripts": "btnicon_scripts.png",
        "formatar_sql": "btnicon_formatar_sql.png",
        "exportar": "btnicon_exportar.png",
        "exportar2": "btnicon_exportar2.png",
        "voltar": "btnicon_voltar.png",
        "voltar2": "btnicon_voltar2.png",
        "converter_data": "btnicon_converter_data.png",
        "dias_uteis": "btnicon_dias_uteis.png",
        "executar": "btnicon_executar.png",
        "limpar": "btnicon_limpar.png",
        "add": "btnicon_add.png",
        "ajuda": "btnicon_ajuda.png",
        "separador": "btnicon_separador.png",
        "fechar": "btnicon_fechar.png",
        "insert": "btnicon_insert.png",
        "update": "btnicon_update.png",
        "delete": "btnicon_delete.png",
    }
    try:
        for name, filename in icon_names.items():
            path = resource_path(f"icons/{filename}")
            img = Image.open(path).resize((25, 25), Image.Resampling.LANCZOS)
            ICONS[name] = ImageTk.PhotoImage(img)
    except Exception as e:
        messagebox.showwarning(
            "Ícones não encontrados", f"Erro ao carregar ícones: {e}"
        )


def abrir_url(url):
    webbrowser.open_new(url)


# Dicionário global para armazenar referências às janelas abertas
telas_abertas = {}


def open_tela(chave, criar_func):
    """Abre uma tela se ela não estiver aberta."""
    if chave in telas_abertas and telas_abertas[chave].winfo_exists():
        telas_abertas[chave].lift()
        return telas_abertas[chave]

    nova_tela = criar_func()
    telas_abertas[chave] = nova_tela
    nova_tela.protocol("WM_DELETE_WINDOW", lambda c=chave: fechar_tela(c))
    return nova_tela


def fechar_tela(chave):
    """Fecha a tela e remove sua referência do dicionário."""
    if chave in telas_abertas:
        telas_abertas[chave].destroy()
        del telas_abertas[chave]
