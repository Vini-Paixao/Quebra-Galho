import os
import sys
import webbrowser


def resource_path(relative_path):
    """Retorna o caminho absoluto para o recurso, necessário para PyInstaller."""
    try:
        base_path = sys._MEIPASS  # Pasta temporária do PyInstaller
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def abrir_url(url):
    webbrowser.open_new(url)