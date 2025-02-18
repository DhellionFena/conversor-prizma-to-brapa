@echo off
setlocal
 
REM Verifica se a virtual environment já existe
if not exist .venv (
    echo Criando ambiente virtual...
    python -m venv .venv
)
 
REM Ativando a virtual environment
call .venv\Scripts\activate.bat
 
REM Instalando o Poetry
if not exist .venv\Scripts\poetry.exe (
    echo Instalando Poetry...
    .venv\Scripts\pip.exe install poetry
)
 
REM Instalando as dependências do projeto
echo Instalando dependencias...
poetry install
 
REM Executando o script Python
echo Criando run_prizma_to_brapa...
.venv\Scripts\python.exe config.py
 
echo Processo concluído.
endlocal