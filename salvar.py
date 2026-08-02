import json

def write(arquivo, text):
    with open(arquivo, 'w') as arquivo:
        json.dump(text, arquivo, indent=4)

def read(arquivo):
    print(arquivo)
    with open(arquivo, 'r') as arquivo:
        try:
            dados = json.load(arquivo)
        except json.JSONDecodeError:
            dados = []
    return dados

def add(arquivo, text):
    arq = read(arquivo)
    arq.append(text)
    write(arquivo, arq)

def clear(arquivo):
    with open(arquivo, 'w') as arquivo:
        json.dump([], arquivo, indent=4)