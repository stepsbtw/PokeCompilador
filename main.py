from parser import analisar

with open("exemplo.poke", encoding="utf-8") as arquivo:
    arvore = analisar(arquivo.read())