import sys
from pprint import pprint

from parser import analisar_codigo


def executar_arquivo(nome_arquivo):
    try:
        with open(
            nome_arquivo,
            "r",
            encoding="utf-8",
        ) as arquivo:
            codigo_fonte = arquivo.read()

    except FileNotFoundError:
        print(
            f"Arquivo não encontrado: {nome_arquivo}"
        )
        return

    print(
        "===== EXECUTANDO POKELANG ====="
    )

    arvore = analisar_codigo(
        codigo_fonte
    )

    print(
        "\n===== ÁRVORE SINTÁTICA ABSTRATA ====="
    )

    pprint(
        arvore,
        width=110,
        sort_dicts=False,
    )

    print(
        "\n===== FIM ====="
    )


def main():
    if len(sys.argv) != 2:
        print("Uso:")
        print(
            "    python main.py exemplo.poke"
        )
        return

    executar_arquivo(
        sys.argv[1]
    )


if __name__ == "__main__":
    main()