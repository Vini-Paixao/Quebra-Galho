import re
from datetime import datetime


def converter_data(data_input):
    """
    Converte uma data fornecida em vários formatos para o padrão americano YYYY-MM-DD.
    Aceita os seguintes formatos de entrada:
    - DD/MM/YYYY
    - DD/MM
    - DDMMYYYY
    - DDMM
    """
    data_input = data_input.strip()
    ano_atual = datetime.now().year

    # Expressões regulares para diferentes formatos de data
    formatos = [
        (r'^(\d{2})/(\d{2})/(\d{4})$', '%d/%m/%Y'),  # DD/MM/YYYY
        (r'^(\d{2})/(\d{2})$', '%d/%m'),  # DD/MM
        (r'^(\d{2})(\d{2})(\d{4})$', '%d%m%Y'),  # DDMMYYYY
        (r'^(\d{2})(\d{2})$', '%d%m')  # DDMM
    ]

    for regex, date_format in formatos:
        match = re.match(regex, data_input)
        if match:
            try:
                data = datetime.strptime(data_input, date_format)
                # Se o formato não inclui o ano, adiciona o ano atual
                if '%Y' not in date_format:
                    data = data.replace(year=ano_atual)
                return data.strftime('%Y-%m-%d')
            except ValueError:
                continue

    raise ValueError(f"Formato de data inválido: {data_input}")
