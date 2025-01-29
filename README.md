
# Quebra Galho <img align="center" alt="Vini-Python" height="40" width="40" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg">

Um programa em Python que auxilia em tarefas do dia a dia, facilitando assim tarefas "chatas" e que podem ser realizadas de maneira automática, desenvolvi esse programa com intuito de me auxiliar no meu trabalho na JBS, assim facilitando consultas SQL e tarefas do dia a dia.

## Funcionalidades

- **Valores em Linha** - Recebe uma certa quantidade de dados empilhados um em cima do outro, e transforma todos em linha separado por vírgula, facilitando consultas SQL.
- **Limpar Formatação** - Recebe qualquer tipo de numeração com máscara (CPF, NF-e, CEP) e retira todos os caracteres não numéricos, mantendo apenas os números e facilitando consultas SQL.
- **Converter Data** - Recebe datas em diversos formatos e automaticamente coloca em formato americano para consultas SQL
- **Funções SQL**
  - **Validar Sintaxe** - Recebe um Script SQL e faz a validação se o mesmo é um script que rodaria sem nenhum erro de sintaxe.
  - **Gerador de Scripts** - Gera Scripts SQL básicos (INSERT, UPDATE e DELETE) com base nos dados fornecidos.
  - **Formatação de Consulta** - Recebe um SCRIPT SQL e formata o mesmo na indentação correta, facilitando na hora de visualizar os dados e realizar a consulta.
  - **Exportação de Consulta** - Recebe o resultado de uma consulta SQL e fornece a opção de exportar em **CSV, XML** ou **Excel (.xlsx)** assim facilitando a manipulação de dados externamente.

## Instalação

O projeto já está compilado, basta apenas acessar a aba de [Release](https://github.com/Vini-Paixao/Quebra-Galho/releases) e realizar o download do .exe
(Disponível somente para Windows).

Caso prefira pode Fazer manualmente na sua IDE de preferência, certifiquesse de ter o Python e o pip instalado na máquina, e siga os passos a passos:

Clonando o Projeto:

```bash
  git clone https://github.com/Vini-Paixao/Quebra-Galho.git
```

Entrando na pasta do projeto:

```bash
  cd Quebra-Galho
```

Instalando as depêndencias externas:

```bash
  pip install sqlfluff sqlparse pandas faker xlsxwriter lxml
```

Executando:

```bash
  python main.py
```

## Licença

[MIT](https://choosealicense.com/licenses/mit/)
