from alinhar_valores import alinhar_valores_interface
from converter_data import converter_data_interface
from exporta_dados import exportar_dados_interface
from gerador_dados import gerador_dados_interface
from limpar_formatacao import limpar_formatacao
from utilidades import abrir_url, resource_path
from validar_sintaxe import validador_sintaxe_interface
from gerador_scripts import menu_gerador_scripts
from formatar_sql import formatar_sql_interface
from tkinter import font
import tkinter as tk

def menu_principal():
    janela = tk.Tk()
    janela.title("Quebra Galho")
    janela.geometry("360x500")
    janela.minsize(360, 500)
    janela.iconbitmap(resource_path('icon.ico'))  # Caminho corrigido
    janela.configure(bg='lightblue')
    
    # Fontes
    global bold
    bold = font.Font(family="Verdana", size=20, weight="bold")
    
    global regular
    regular = font.Font(family="Verdana", size=10, weight="normal")
    
    global autor
    autor = font.Font(family="Verdana", size=8, weight="bold")
    
    global descricao
    descricao = font.Font(family="Verdana", size=9, weight="normal")

    # Título
    titulo = tk.Label(janela, text="Quebra Galho", font=bold, bg='lightblue')
    titulo.pack(pady=5)
    
    # Descrição
    desc = tk.Label(
        janela, 
        text="Bem-vindo ao Quebra Galho! Esse programa automatiza tarefas repetitivas e facilita seu dia a dia. Ele ainda está em desenvolvimento, então se encontrar bugs ou tiver sugestões, entre em contato. Aproveite!", 
        font=descricao,
        bg='lightblue',
        wraplength=340
        )
    desc.pack(pady=5)

    # Botões do menu principal
    btn_valores_linha = tk.Button(janela, text="Valores em Linha", font=regular, command=alinhar_valores_interface)
    btn_valores_linha.pack(pady=5)

    btn_limpar_formatacao = tk.Button(janela, text="Limpar Formatação", font=regular, command=limpar_formatacao)
    btn_limpar_formatacao.pack(pady=5)

    btn_converter_data = tk.Button(janela, text="Converter Data", font=regular, command=converter_data_interface)
    btn_converter_data.pack(pady=5)
    
    btn_gerar_dados = tk.Button(janela, text="Gerar Dados Fictícios", font=regular, command=gerador_dados_interface)
    btn_gerar_dados.pack(pady=5)

    btn_funcoes_sql = tk.Button(janela, text="Funções SQL", bg="lightgreen", font=regular, command=menu_sql)
    btn_funcoes_sql.pack(pady=5)
    
    btn_codigo_fonte = tk.Button(
        janela, 
        text="Código Fonte do Programa", 
        font=regular, 
        command=lambda: abrir_url("https://github.com/Vini-Paixao/Quebra-Galho"),
        bg="#6c757d",  # Cinza
        fg="white"
    )
    btn_codigo_fonte.pack(pady=5)

    btn_encerrar = tk.Button(
        janela, 
        text="Encerrar", 
        bg="#dc3545",  # Vermelho
        fg="white",
        font=regular, 
        command=janela.quit
    )
    btn_encerrar.pack(pady=5)
    
    txt_autor = tk.Label(janela, text="Desenvolvido por Marcus Paixão!", font=autor, bg='lightblue')
    txt_autor.pack(pady=10)
    
    rede_social_frame = tk.Frame(janela, bg='lightblue')
    rede_social_frame.pack(pady=5)

    btn_site = tk.Button(
        rede_social_frame, 
        text="Meu Site Pessoal/Portfólio", 
        font=regular,
        command=lambda: abrir_url("https://marcuspaixao.com.br"),
        bg="#167ee4",  # Azul Site
        fg="white"
    )
    btn_site.pack(side=tk.LEFT, padx=5)

    btn_github_perfil = tk.Button(
        rede_social_frame, 
        text="Meu GitHub", 
        font=regular,
        command=lambda: abrir_url("https://github.com/Vini-Paixao"),
        bg="#181717",  # Preto GitHub
        fg="white"
    )
    btn_github_perfil.pack(side=tk.LEFT, padx=5)

    janela.mainloop()

def menu_sql():
    janela = tk.Toplevel()
    janela.title("Scripts SQL")
    janela.geometry("300x250")
    janela.iconbitmap(resource_path('icon.ico'))  # Caminho corrigido
    janela.minsize(300, 250)
    janela.configure(bg='lightgreen')

    # Título
    titulo = tk.Label(janela, text="Scripts SQL", font=bold,bg='lightgreen')
    titulo.pack(pady=10)

    # Botões do menu SQL
    btn_validador_sintaxe = tk.Button(janela, text="Validador de Sintaxe", font=regular, command=validador_sintaxe_interface)
    btn_validador_sintaxe.pack(pady=5)

    btn_gerador_scripts = tk.Button(janela, text="Gerador de Scripts", font=regular, command=menu_gerador_scripts)
    btn_gerador_scripts.pack(pady=5)

    btn_formatacao_consultas = tk.Button(janela, text="Formatação de Consultas", font=regular, command=formatar_sql_interface)
    btn_formatacao_consultas.pack(pady=5)
    
    btn_exporta = tk.Button(janela, text="Exportar Consultas SQL", font=regular, command=exportar_dados_interface)
    btn_exporta.pack(pady=5)

    btn_voltar = tk.Button(janela, text="Voltar", bg="lightblue", font=regular, command=janela.destroy)
    btn_voltar.pack(pady=5)
