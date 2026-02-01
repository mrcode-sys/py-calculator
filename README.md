# Calculadora em Python com Kivy
## Descrição
Aplicação desenvolvida em Python utilizando Kivy para criar uma calculadora com interface gráfica.

## Funcionalidades
- Operações básicas (adição, subtração, multiplicação e divisão)
- Interface gráfica simples e funcional
- Tratamento básico de erros

## Tecnologias utilizadas
- Python
- Kivy

## Executar
Siga os passos abaixo para executar o projeto localmente.
### Caso esteja utilizando sistemas Linux baseados em Debian:
Instalar Python 3:
```
sudo apt update
sudo apt install python3
```
Instalar pip:
```
sudo apt install python3-pip
```
Criar e iniciar ambiente virtual:
```
python3 -m venv env
source env/bin/activate
```
### Caso esteja utilizando sistemas Linux baseados em fedora:
Instalar Python 3:
```
sudo dnf install python3
```
Instalar pip:
```
sudo dnf install python3-pip
```
Criar e iniciar ambiente virtual:
```
python3 -m venv env
source env/bin/activate
```
### Caso esteja utilizando sistemas Linux baseados em Arch:
Instalar Python 3:
```
sudo pacman -Syu
sudo pacman -S python
```
Instalar pip:
```
sudo pacman -S python-pip
```
Criar e iniciar ambiente virtual:
```
python3 -m venv env
source env/bin/activate
```
### Caso esteja utilizando sistemas Windows:
Para instalar o python e o pip consulte o site https://www.python.org/

Criar e iniciar ambiente virtual:
```
python3 -m venv env
env\Scripts\activate.bat
```
### Instalação da biblioteca:
```
pip install kivy
```
Após isso será possível executar a calculadora com esse comando na pasta raiz do projeto:
```
python3 main.py
```
ou, caso não funcione
```
python main.py
```
## O que aprendi com este projeto
- Estruturação de uma aplicação em Python
- Criação de interface gráfica utilizando Kivy
- Organização de código e separação de responsabilidades
