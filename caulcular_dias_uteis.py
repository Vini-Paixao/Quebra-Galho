from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from tkinter import ttk, messagebox
import tkinter as tk
from tkcalendar import DateEntry
from dateutil import easter

from utilidades import resource_path

# Função para gerar feriados brasileiros
def gerar_feriados(ano):
    from datetime import date
    
    feriados = [
        # Datas fixas
        date(ano, 1, 1),   # Ano Novo
        date(ano, 4, 21),  # Tiradentes
        date(ano, 5, 1),   # Dia do Trabalho
        date(ano, 9, 7),   # Independência
        date(ano, 10, 12), # Nossa Senhora Aparecida
        date(ano, 11, 2),  # Finados
        date(ano, 11, 15), # Proclamação da República
        date(ano, 12, 25), # Natal
        
        # Datas móveis
        easter.easter(ano) - timedelta(days=47),  # Carnaval
        easter.easter(ano) - timedelta(days=2),   # Sexta-feira Santa
        easter.easter(ano),                       # Páscoa
        easter.easter(ano) + timedelta(days=60)   # Corpus Christi
    ]
    return feriados

def calcular_dias_uteis(data_inicio, data_fim):
    try:
        inicio = datetime.strptime(data_inicio, "%d/%m/%Y").date()
        fim = datetime.strptime(data_fim, "%d/%m/%Y").date()
        
        if fim < inicio:
            return None, None, "Data final menor que inicial!"
        dias_corridos = (fim - inicio).days + 1
        dias_uteis = 0
        feriados = []
        
        # Gera feriados para todos os anos no intervalo
        for ano in range(inicio.year, fim.year + 1):
            feriados.extend(gerar_feriados(ano))
        
        current_date = inicio
        while current_date <= fim:
            # Verifica se é final de semana
            if current_date.weekday() < 5:  # 0-4 = Segunda a Sexta
                # Verifica se é feriado
                if current_date not in feriados:
                    dias_uteis += 1
            current_date += timedelta(days=1)
            
        return dias_uteis, dias_corridos, None
    
    except Exception as e:
        return None, None, f"Erro: {str(e)}"

def calcular_dias_uteis_interface():
    def calcular():
        resultado = calcular_dias_uteis(
            inicio_entry.get(),
            fim_entry.get()
        )
        
        if resultado[2]:  # Se houver erro
            messagebox.showerror("Erro", resultado[2])
            return
        
        lbl_resultado_uteis.config(text=f"Dias Úteis: {resultado[0]}")
        lbl_resultado_corridos.config(text=f"Dias Corridos: {resultado[1]}")
    
    janela = tk.Toplevel()
    janela.title("Calculadora de Dias Úteis")
    janela.geometry("450x300")
    janela.minsize(450, 300)
    janela.iconbitmap(resource_path('icon.ico'))
    janela.configure(bg='#bc7ff6')
    
    # Fontes
    regular = tk.font.Font(family="Verdana", size=10)
    bold = tk.font.Font(family="Verdana", size=12, weight="bold")
    
    # Widgets
    tk.Label(janela, text="Data Início:", font=bold, bg='#bc7ff6').pack(pady=5)
    inicio_entry = DateEntry(janela, 
                           date_pattern='dd/mm/yyyy',
                           font=regular,
                           locale='pt_BR')
    inicio_entry.pack(pady=5)
    
    tk.Label(janela, text="Data Fim:", font=bold, bg='#bc7ff6').pack(pady=5)
    fim_entry = DateEntry(janela, 
                        date_pattern='dd/mm/yyyy',
                        font=regular,
                        locale='pt_BR')
    fim_entry.pack(pady=5)
    
    tk.Button(janela, text="Calcular", bg="#67d167", font=regular, command=calcular).pack(pady=10)
    
    lbl_frame = tk.Frame(janela, bg='#bc7ff6')
    lbl_frame.pack(pady=5)
    
    # Resultados
    lbl_resultado_uteis = tk.Label(lbl_frame, text="Dias Úteis: -", font=bold, bg='#bc7ff6')
    lbl_resultado_uteis.pack(side=tk.LEFT,padx=5)
    
    lbl_resultado_corridos = tk.Label(lbl_frame, text="Dias Corridos: -", font=bold, bg='#bc7ff6')
    lbl_resultado_corridos.pack(side=tk.LEFT,padx=5)
    
    # Aviso
    tk.Label(janela, 
           text="* Considera feriados nacionais brasileiros e finais de semana",
           font=regular, 
           bg='#bc7ff6').pack(pady=10)
    
    # Botão para fechar a janela
    btn_encerrar = tk.Button(janela, text="Fechar", bg="#dc3545", font=regular, command=janela.destroy)
    btn_encerrar.pack(pady=5)
    
    janela.mainloop()