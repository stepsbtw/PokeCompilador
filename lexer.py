import ply.lex as lex


reservadas = {
    "efetividade": "EFETIVIDADE",
    "contra": "CONTRA",
    "dano": "DANO",

    "pokemon": "POKEMON",
    "golpe": "GOLPE",

    "batalha": "BATALHA",
    "usa": "USA",

    "vida": "VIDA",
    "ataque": "ATAQUE",
    "defesa": "DEFESA",
    "poder": "PODER",

    "fogo": "FOGO",
    "agua": "AGUA",
    "eletrico": "ELETRICO",
}


tokens = [
    "ID",
    "NUMERO",

    "MAIS",
    "MENOS",
    "VEZES",
    "DIVIDIDO",

    "IGUAL",
    "DOIS_PONTOS",
    "PONTO_VIRGULA",

    "ABRE_PARENTESES",
    "FECHA_PARENTESES",

    "ABRE_CHAVES",
    "FECHA_CHAVES",
] + list(reservadas.values())


t_MAIS = r"\+"
t_MENOS = r"-"
t_VEZES = r"\*"
t_DIVIDIDO = r"/"

t_IGUAL = r"="
t_DOIS_PONTOS = r":"
t_PONTO_VIRGULA = r";"

t_ABRE_PARENTESES = r"\("
t_FECHA_PARENTESES = r"\)"

t_ABRE_CHAVES = r"\{"
t_FECHA_CHAVES = r"\}"

t_ignore = " \t\r"


def t_COMENTARIO(t):
    r"\#.*"
    pass


def t_NUMERO(t):
    r"\d+(\.\d+)?"

    if "." in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)

    return t


def t_ID(t):
    r"[A-Za-z_][A-Za-z0-9_]*"

    valor_minusculo = t.value.lower()

    if valor_minusculo in reservadas:
        t.type = reservadas[valor_minusculo]
        t.value = valor_minusculo

    return t


def t_nova_linha(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(
        f"[ERRO LÉXICO] Caractere inválido "
        f"'{t.value[0]}' na linha {t.lexer.lineno}."
    )

    t.lexer.skip(1)


analisador_lexico = lex.lex()


if __name__ == "__main__":
    codigo = """
    efetividade eletrico contra agua = 2.0;

    dano =
        (ataque + poder - defesa) * efetividade;

    pokemon Pikachu : eletrico {
        vida = 200;
        ataque = 80;
        defesa = 50;
    }
    """

    analisador_lexico.input(codigo)

    while True:
        token = analisador_lexico.token()

        if token is None:
            break

        print(
            f"tipo={token.type:<20} "
            f"valor={str(token.value):<20} "
            f"linha={token.lineno}"
        )
