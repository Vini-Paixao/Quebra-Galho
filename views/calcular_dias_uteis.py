from datetime import datetime, timedelta
from dateutil import easter
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

from utilidades import resource_path, ICONS


def gerar_feriados(ano):
    """Gera uma lista de feriados nacionais brasileiros para um determinado ano."""
    feriados = [
        # Datas fixas
        datetime(ano, 1, 1).date(),  # Ano Novo
        datetime(ano, 4, 21).date(),  # Tiradentes
        datetime(ano, 5, 1).date(),  # Dia do Trabalho
        datetime(ano, 9, 7).date(),  # Independência
        datetime(ano, 10, 12).date(),  # Nossa Senhora Aparecida
        datetime(ano, 11, 2).date(),  # Finados
        datetime(ano, 11, 15).date(),  # Proclamação da República
        datetime(ano, 12, 25).date(),  # Natal
    ]
    # Datas móveis baseadas na Páscoa
    pascoa = easter.easter(ano)
    feriados.extend(
        [
            pascoa - timedelta(days=47),  # Carnaval
            pascoa - timedelta(days=2),  # Sexta-feira Santa
            pascoa,  # Páscoa
            pascoa + timedelta(days=60),  # Corpus Christi
        ]
    )
    return feriados


def calcular_dias_uteis(data_inicio, data_fim):
    try:
        inicio = datetime.strptime(data_inicio, "%d/%m/%Y").date()
        fim = datetime.strptime(data_fim, "%d/%m/%Y").date()

        if fim < inicio:
            return None, None, "A data final não pode ser menor que a data inicial."

        dias_corridos = (fim - inicio).days + 1
        dias_uteis = 0

        anos_no_intervalo = range(inicio.year, fim.year + 1)
        feriados = {
            feriado for ano in anos_no_intervalo for feriado in gerar_feriados(ano)
        }

        current_date = inicio
        while current_date <= fim:
            if current_date.weekday() < 5 and current_date not in feriados:
                dias_uteis += 1
            current_date += timedelta(days=1)

        return dias_uteis, dias_corridos, None
    except Exception as e:
        return None, None, f"Erro ao calcular as datas: {e}"


def calcular_dias_uteis_interface():
    def calcular():
        dias_uteis, dias_corridos, erro = calcular_dias_uteis(
            inicio_entry.get(), fim_entry.get()
        )

        if erro:
            messagebox.showerror("Erro", erro)
            lbl_resultado_uteis.config(text="Dias Úteis: -")
            lbl_resultado_corridos.config(text="Dias Corridos: -")
            return

        lbl_resultado_uteis.config(text=f"Dias Úteis: {dias_uteis}")
        lbl_resultado_corridos.config(text=f"Dias Corridos: {dias_corridos}")

    def limpar_campos():
        # Reseta os campos de data para a data atual
        hoje = datetime.now()
        inicio_entry.set_date(hoje)
        fim_entry.set_date(hoje)
        # Limpa os resultados
        lbl_resultado_uteis.config(text="Dias Úteis: -")
        lbl_resultado_corridos.config(text="Dias Corridos: -")

    janela = tk.Toplevel()
    janela.title("Calculadora de Dias Úteis")
    janela.geometry("420x350")
    janela.minsize(420, 350)
    janela.iconbitmap(resource_path("icon.ico"))

    main_frame = ttk.Frame(janela, padding=20)
    main_frame.pack(expand=True, fill="both")

    # --- ENTRADA DE DATAS ---
    datas_frame = ttk.Frame(main_frame)
    datas_frame.pack(fill="x")
    datas_frame.columnconfigure(0, weight=1)
    datas_frame.columnconfigure(1, weight=1)

    ttk.Label(datas_frame, text="Data Início:", font=("Segoe UI", 10, "bold")).grid(
        row=0, column=0, sticky="w"
    )
    inicio_entry = DateEntry(
        datas_frame, date_pattern="dd/mm/yyyy", locale="pt_BR", width=15
    )
    inicio_entry.grid(row=1, column=0, sticky="ew", pady=(5, 15))

    ttk.Label(datas_frame, text="Data Fim:", font=("Segoe UI", 10, "bold")).grid(
        row=0, column=1, sticky="w", padx=(10, 0)
    )
    fim_entry = DateEntry(
        datas_frame, date_pattern="dd/mm/yyyy", locale="pt_BR", width=15
    )
    fim_entry.grid(row=1, column=1, sticky="ew", padx=(10, 0), pady=(5, 15))

    # --- RESULTADOS ---
    resultado_frame = ttk.Labelframe(main_frame, text="Resultados", padding=15)
    resultado_frame.pack(fill="x", pady=10)
    resultado_frame.columnconfigure(0, weight=1)
    resultado_frame.columnconfigure(1, weight=1)

    lbl_resultado_uteis = ttk.Label(
        resultado_frame, text="Dias Úteis: -", font=("Segoe UI", 12, "bold")
    )
    lbl_resultado_uteis.grid(row=0, column=0)

    lbl_resultado_corridos = ttk.Label(
        resultado_frame, text="Dias Corridos: -", font=("Segoe UI", 12, "bold")
    )
    lbl_resultado_corridos.grid(row=0, column=1)

    # --- AVISO ---
    ttk.Label(
        main_frame,
        text="* Considera feriados nacionais brasileiros.",
        font=("Segoe UI", 8),
        justify=tk.CENTER,
    ).pack(side="bottom")

    # --- BOTÕES DE AÇÃO ---
    botoes_frame = ttk.Frame(main_frame)
    botoes_frame.pack(side="bottom", fill="x", pady=(20, 10))

    ttk.Button(
        botoes_frame,
        text="Voltar",
        image=ICONS.get("voltar2", tk.PhotoImage()),
        compound="left",
        command=janela.destroy,
    ).pack(side="right")
    ttk.Button(
        botoes_frame,
        text="Limpar",
        image=ICONS.get("limpar", tk.PhotoImage()),
        compound="left",
        command=limpar_campos,
    ).pack(side="right", padx=10)
    ttk.Button(
        botoes_frame,
        text="Calcular",
        style="Accent.TButton",
        image=ICONS.get("executar", tk.PhotoImage()),
        compound="left",
        command=calcular,
    ).pack(side="right")

    return janela
