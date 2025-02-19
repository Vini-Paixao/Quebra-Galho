from alinhar_valores import alinhar_valores_interface
from caulcular_dias_uteis import calcular_dias_uteis_interface
from converter_data import converter_data_interface
from exporta_dados import exportar_dados_interface
from formatar_xml import validar_formatar_json_xml_interface
from gerador_dados import gerador_dados_interface
from limpar_formatacao import limpar_formatacao
from utilidades import abrir_url, resource_path
from validar_sintaxe import validador_sintaxe_interface
from gerador_scripts import menu_gerador_scripts
from formatar_sql import formatar_sql_interface
from tkinter import font, ttk
import tkinter as tk

def menu_principal():
    janela = tk.Tk()
    janela.title("Quebra Galho")
    janela.geometry("370x470")
    janela.minsize(370, 470)
    janela.iconbitmap(resource_path('icon.ico'))  # Caminho corrigido
    janela.configure(bg='#7acbe6')
    
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
    titulo = tk.Label(janela, text="Quebra Galho", font=bold, bg='#7acbe6')
    titulo.pack(pady=5)
    
    # Descrição
    desc = tk.Label(
        janela, 
        text="Bem-vindo ao Quebra Galho! Esse programa automatiza tarefas repetitivas e facilita seu dia a dia. Ele ainda está em desenvolvimento, então se encontrar bugs ou tiver sugestões, entre em contato. Aproveite!", 
        font=descricao,
        bg='#7acbe6',
        wraplength=340
        )
    desc.pack(pady=5)

    # Botões do menu principal
    btn_valores_linha = tk.Button(janela, text="Valores em Linha", font=regular, command=alinhar_valores_interface)
    btn_valores_linha.pack(pady=5)

    btn_limpar_formatacao = tk.Button(janela, text="Limpar Formatação", font=regular, command=limpar_formatacao)
    btn_limpar_formatacao.pack(pady=5)
    
    btn_gerar_dados = tk.Button(janela, text="Gerar Dados Fictícios", font=regular, command=gerador_dados_interface)
    btn_gerar_dados.pack(pady=5)
    
    btn_json_xml = tk.Button(janela, text="Validador de JSON/XML", font=regular, command=validar_formatar_json_xml_interface)
    btn_json_xml.pack(pady=5)
    
    btn_frame = tk.Frame(janela, bg='#7acbe6')
    btn_frame.pack(pady=5)
    
    btn_menu_datas = tk.Button(btn_frame, text="Funções Datas", bg= "#bc7ff6", font=regular, command=menu_datas)
    btn_menu_datas.pack(side=tk.LEFT, padx=5)

    btn_funcoes_sql = tk.Button(btn_frame, text="Funções SQL", bg="#67d167", font=regular, command=menu_sql)
    btn_funcoes_sql.pack(side=tk.LEFT, padx=5)
    
    separator = tk.Label(janela, text="_________________________________________", font=autor, bg='#7acbe6')
    separator.pack(pady=0)
    
    txt_autor = tk.Label(janela, text="Desenvolvido por Marcus Paixão!", font=autor, bg='#7acbe6')
    txt_autor.pack(pady=10)
    
    rede_social_frame = tk.Frame(janela, bg='#7acbe6')
    rede_social_frame.pack(pady=5)

    btn_site = tk.Button(
        rede_social_frame, 
        text="Meu Site", 
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
    
    btn_codigo_fonte = tk.Button(
        janela, 
        text="Código Fonte do Programa", 
        font=regular, 
        command=lambda: abrir_url("https://github.com/Vini-Paixao/Quebra-Galho"),
        bg="#6c757d",  # Cinza
        fg="white"
    )
    btn_codigo_fonte.pack(pady=5)
    
    # btn_encerrar = tk.Button(
    #     janela, 
    #     text="Encerrar", 
    #     bg="#dc3545",  # Vermelho
    #     fg="white",
    #     font=regular, 
    #     command=janela.quit
    # )
    # btn_encerrar.pack(pady=5)

    janela.mainloop()

def menu_sql():
    janela = tk.Toplevel()
    janela.title("Ferramentas de SQL")
    janela.geometry("350x200")
    janela.iconbitmap(resource_path('icon.ico'))  # Caminho corrigido
    janela.minsize(350, 200)
    janela.configure(bg='#67d167')

    # Título
    titulo = tk.Label(janela, text="Ferramentas de SQL", font=bold,bg='#67d167')
    titulo.pack(pady=10)
    
    frame_1 = tk.Frame(janela, bg='#67d167')
    frame_1.pack(pady=5)

    # Botões do menu SQL
    btn_validador_sintaxe = tk.Button(frame_1, text="Validador de Sintaxe", font=regular, command=validador_sintaxe_interface)
    btn_validador_sintaxe.pack(side=tk.LEFT, padx=5)

    btn_gerador_scripts = tk.Button(frame_1, text="Gerador de Scripts", font=regular, command=menu_gerador_scripts)
    btn_gerador_scripts.pack(side=tk.LEFT, padx=5)
    
    frame_2 = tk.Frame(janela, bg='#67d167')
    frame_2.pack(pady=10)

    btn_formatacao_consultas = tk.Button(frame_2, text="Formatação de Script", font=regular, command=formatar_sql_interface)
    btn_formatacao_consultas.pack(side=tk.LEFT, padx=5)
    
    btn_exporta = tk.Button(frame_2, text="Exportar Resultados", font=regular, command=exportar_dados_interface)
    btn_exporta.pack(side=tk.LEFT, padx=5)

    btn_voltar = tk.Button(janela, text="Voltar", bg="#dc3545", font=regular, command=janela.destroy)
    btn_voltar.pack(pady=15)

def menu_datas():
    janela = tk.Toplevel()
    janela.title("Ferramentas de Datas")
    janela.geometry("370x180")
    janela.minsize(370, 180)
    janela.iconbitmap(resource_path('icon.ico'))  # Caminho corrigido
    janela.configure(bg='#bc7ff6')

    # Título
    titulo = tk.Label(janela, text="Ferramentas de Datas", font=bold,bg='#bc7ff6')
    titulo.pack(pady=10)

    # Botões do menu SQL
    btn_validador_sintaxe = tk.Button(janela, text="Converter Datas", font=regular, command=converter_data_interface)
    btn_validador_sintaxe.pack(pady=5)

    btn_gerador_scripts = tk.Button(janela, text="Calcular Dias Úteis", font=regular, command=calcular_dias_uteis_interface)
    btn_gerador_scripts.pack(pady=5)

    # btn_formatacao_consultas = tk.Button(janela, text="Em Desenvolvimento", font=regular)
    # btn_formatacao_consultas.pack(pady=5)
    
    # btn_exporta = tk.Button(janela, text="Em Desenvolvimento", font=regular)
    # btn_exporta.pack(pady=5)

    btn_voltar = tk.Button(janela, text="Voltar", bg="#dc3545", font=regular, command=janela.destroy)
    btn_voltar.pack(pady=5)
