import tkinter as tk
from tkinter import ttk, font, messagebox
import sv_ttk
from PIL import Image, ImageTk
from utilidades import abrir_url, resource_path, open_tela, load_icons, ICONS

from views.alinhar_valores import alinhar_valores_interface
from views.calcular_dias_uteis import calcular_dias_uteis_interface
from views.converter_data import converter_data_interface
from views.exporta_dados import exportar_dados_interface
from views.formatar_xml import validar_formatar_json_xml_interface
from views.gerador_dados import gerador_dados_interface
from views.limpar_formatacao import limpar_formatacao
from views.validar_sintaxe import validador_sintaxe_interface
from views.gerador_scripts import menu_gerador_scripts
from views.formatar_sql import formatar_sql_interface


def menu_principal():
    janela = tk.Tk()
    janela.title("Quebra Galho")
    janela.geometry("410x520")
    janela.minsize(410, 520)
    janela.iconbitmap(resource_path("icon.ico"))

    default_font = font.nametofont("TkDefaultFont")
    default_font.configure(family="Segoe UI", size=12)
    janela.option_add("*Font", default_font)

    sv_ttk.set_theme("light")
    load_icons()  # Carrega os ícones na inicialização

    style = ttk.Style()
    style.configure("Link.TButton", font=("Segoe UI", 12))

    def toggle_theme():
        theme = "dark" if sv_ttk.get_theme() == "light" else "light"
        sv_ttk.set_theme(theme)

    main_frame = ttk.Frame(janela, padding=10)
    main_frame.pack(expand=True, fill="both")

    titulo = ttk.Label(main_frame, text="Quebra Galho", font=("Segoe UI", 26, "bold"))
    titulo.pack(pady=5)

    desc = ttk.Label(
        main_frame,
        text="Bem-vindo ao Quebra Galho! Este programa em Python automatiza tarefas repetitivas para facilitar seu dia a dia.",
        font=("Segoe UI", 12),
        wraplength=400,
        justify="center",
    )
    desc.pack(pady=10, fill="x")

    botoes_frame = ttk.Frame(main_frame)
    botoes_frame.pack(pady=10, fill="x")

    ttk.Button(
        botoes_frame,
        text=" Valores em Linha",
        image=ICONS.get("valores", tk.PhotoImage()),
        compound="left",
        command=lambda: open_tela("Alinhar Valores", alinhar_valores_interface),
    ).pack(pady=3, fill="x", ipady=2)
    ttk.Button(
        botoes_frame,
        text=" Limpar Formatação",
        image=ICONS.get("formatacao", tk.PhotoImage()),
        compound="left",
        command=lambda: open_tela("Limpar Formatação", limpar_formatacao),
    ).pack(pady=3, fill="x", ipady=2)
    ttk.Button(
        botoes_frame,
        text=" Gerar Dados Fictícios",
        image=ICONS.get("dados", tk.PhotoImage()),
        compound="left",
        command=lambda: open_tela("Gerar Dados Fictícios", gerador_dados_interface),
    ).pack(pady=3, fill="x", ipady=2)
    ttk.Button(
        botoes_frame,
        text=" Validador de JSON/XML",
        image=ICONS.get("json_xml", tk.PhotoImage()),
        compound="left",
        command=lambda: open_tela(
            "Validador de JSON/XML", validar_formatar_json_xml_interface
        ),
    ).pack(pady=3, fill="x", ipady=2)

    submenus_frame = ttk.Frame(main_frame)
    submenus_frame.pack(pady=5, fill="x")

    ttk.Button(
        submenus_frame,
        text=" Funções Datas",
        style="Accent.TButton",
        image=ICONS.get("datas", tk.PhotoImage()),
        compound="left",
        command=lambda: open_tela("Datas", menu_datas),
    ).pack(side=tk.LEFT, padx=5, fill="x", expand=True, ipady=4)
    ttk.Button(
        submenus_frame,
        text=" Funções SQL",
        style="Accent.TButton",
        image=ICONS.get("sql", tk.PhotoImage()),
        compound="left",
        command=lambda: open_tela("SQL", menu_sql),
    ).pack(side=tk.LEFT, padx=5, fill="x", expand=True, ipady=4)

    ttk.Separator(main_frame, orient="horizontal").pack(fill="x", pady=5)
    links_frame = ttk.Frame(main_frame)
    links_frame.pack(pady=10, fill="x")

    ttk.Button(
        links_frame,
        text=" Meu Site",
        style="Link.TButton",
        image=ICONS.get("site", tk.PhotoImage()),
        compound="left",
        command=lambda: abrir_url("https://marcuspaixao.com.br"),
    ).pack(side=tk.LEFT, padx=5, fill="x", expand=True)
    ttk.Button(
        links_frame,
        text=" Meu GitHub",
        style="Link.TButton",
        image=ICONS.get("github", tk.PhotoImage()),
        compound="left",
        command=lambda: abrir_url("https://github.com/Vini-Paixao"),
    ).pack(side=tk.LEFT, padx=5, fill="x", expand=True)

    bottom_frame = ttk.Frame(main_frame)
    bottom_frame.pack(side="bottom", fill="x", pady=5)
    autor_label = ttk.Label(
        bottom_frame,
        text="Desenvolvido por Marcus Paixão",
        font=("Segoe UI", 8, "bold"),
    )
    autor_label.pack(side="left", padx=10)
    theme_switch = ttk.Checkbutton(
        bottom_frame,
        text="Modo Escuro",
        command=toggle_theme,
        style="Switch.TCheckbutton",
    )
    theme_switch.pack(side="right", padx=10)

    def on_closing():
        if messagebox.askokcancel(
            "Sair", "Você tem certeza que deseja fechar o programa?"
        ):
            janela.destroy()

    janela.protocol("WM_DELETE_WINDOW", on_closing)
    janela.mainloop()


def menu_sql():
    janela = tk.Toplevel()
    janela.title("Ferramentas de SQL")
    janela.geometry("380x380")
    janela.iconbitmap(resource_path("icon.ico"))
    janela.minsize(380, 380)

    main_frame = ttk.Frame(janela, padding=15)
    main_frame.pack(expand=True, fill="both")

    titulo = ttk.Label(
        main_frame, text="Ferramentas de SQL", font=("Segoe UI", 16, "bold")
    )
    titulo.pack(pady=10)

    frame_1 = ttk.Frame(main_frame)
    frame_1.pack(pady=5, fill="x")
    ttk.Button(
        frame_1,
        text=" Validador de Sintaxe",
        image=ICONS.get("sintaxe", tk.PhotoImage()),
        compound="left",
        command=lambda: open_tela("Validador de Sintaxe", validador_sintaxe_interface),
    ).pack(pady=3, fill="x", ipady=3)
    ttk.Button(
        frame_1,
        text=" Gerador de Scripts",
        image=ICONS.get("scripts", tk.PhotoImage()),
        compound="left",
        command=lambda: open_tela("Gerador de Scripts", menu_gerador_scripts),
    ).pack(pady=3, fill="x", ipady=3)

    frame_2 = ttk.Frame(main_frame)
    frame_2.pack(pady=5, fill="x")
    ttk.Button(
        frame_2,
        text=" Formatação de Script",
        image=ICONS.get("formatar_sql", tk.PhotoImage()),
        compound="left",
        command=lambda: open_tela("Formatação de Script", formatar_sql_interface),
    ).pack(pady=3, fill="x", ipady=3)
    ttk.Button(
        frame_2,
        text=" Exportar Resultados",
        image=ICONS.get("exportar", tk.PhotoImage()),
        compound="left",
        command=lambda: open_tela("Exportar Resultados", exportar_dados_interface),
    ).pack(pady=3, fill="x", ipady=3)

    ttk.Button(
        main_frame,
        text=" Voltar",
        style="Accent.TButton",
        image=ICONS.get("voltar", tk.PhotoImage()),
        compound="left",
        command=janela.destroy,
    ).pack(pady=10, ipady=4)
    return janela


def menu_datas():
    janela = tk.Toplevel()
    janela.title("Ferramentas de Datas")
    janela.geometry("300x260")
    janela.iconbitmap(resource_path("icon.ico"))
    janela.minsize(300, 260)

    main_frame = ttk.Frame(janela, padding=15)
    main_frame.pack(expand=True, fill="both")

    titulo = ttk.Label(
        main_frame, text="Ferramentas de Datas", font=("Segoe UI", 16, "bold")
    )
    titulo.pack(pady=10)

    botoes_frame = ttk.Frame(main_frame)
    botoes_frame.pack(pady=5, fill="x")
    ttk.Button(
        botoes_frame,
        text=" Converter Datas",
        image=ICONS.get("converter_data", tk.PhotoImage()),
        compound="left",
        command=lambda: open_tela("Converter Datas", converter_data_interface),
    ).pack(pady=3, fill="x", ipady=3)
    ttk.Button(
        botoes_frame,
        text=" Calcular Dias Úteis",
        image=ICONS.get("dias_uteis", tk.PhotoImage()),
        compound="left",
        command=lambda: open_tela("Calcular Dias Úteis", calcular_dias_uteis_interface),
    ).pack(pady=3, fill="x", ipady=3)

    ttk.Button(
        main_frame,
        text=" Voltar",
        style="Accent.TButton",
        image=ICONS.get("voltar", tk.PhotoImage()),
        compound="left",
        command=janela.destroy,
    ).pack(pady=10, ipady=4)
    return janela


if __name__ == "__main__":
    menu_principal()
