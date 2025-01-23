import subprocess
import tempfile
import os

def capturar_entrada_sql():
    """
    Captura múltiplas linhas de entrada do usuário até uma linha vazia ser inserida.
    """
    print("Insira a consulta SQL (pressione Enter em uma linha vazia para finalizar):")
    linhas = []
    while True:
        linha = input()
        if linha.strip() == "":
            break
        linhas.append(linha)
    return "\n".join(linhas)

def validar_sintaxe_sql(consulta_sql):
    """
    Valida a sintaxe da consulta SQL usando o SQLFluff.
    """
    # Cria um arquivo temporário para armazenar a consulta SQL
    with tempfile.NamedTemporaryFile(delete=False, suffix='.sql', mode='w') as temp_file:
        temp_file.write(consulta_sql)
        temp_file_path = temp_file.name
    
    try:
        # Executa o SQLFluff para validar a sintaxe
        resultado = subprocess.run(
            ['sqlfluff', 'lint', temp_file_path, '--dialect', 'sqlite'],
            capture_output=True,
            text=True
        )
        
        # Verifica o código de retorno e analisa as saídas
        if resultado.returncode == 0:
            return "Sintaxe válida."
        else:
            return f"Erros encontrados:\n{resultado.stderr or resultado.stdout}"
    finally:
        # Remove o arquivo temporário
        os.remove(temp_file_path)