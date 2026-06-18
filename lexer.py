import ply.lex as lex

reservadas = {
    "dano": "DANO",
    "batalha": "BATALHA",
    "contra": "CONTRA",
    "turno": "TURNO",
    "usa": "USA",
    "ataque": "ATAQUE",
    "defesa": "DEFESA",
    "poder": "PODER",
    "efetividade": "EFETIVIDADE",
    "fogo": "FOGO",
    "agua": "AGUA",
    "eletrico": "ELETRICO"
}

tokens = [
    "ID", "NUMERO",
    "MAIS", "MENOS", "VEZES", "DIVIDIDO",
    "IGUAL", "VIRGULA", "PONTO_VIRGULA",
    "ABRE_PARENTESES", "FECHA_PARENTESES",
    "ABRE_CHAVES", "FECHA_CHAVES"
] + list(reservadas.values())

t_MAIS = r"\+"
t_MENOS = r"-"
t_VEZES = r"\*"
t_DIVIDIDO = r"/"
t_IGUAL = r"="
t_VIRGULA = r","
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
    t.value = float(t.value) if "." in t.value else int(t.value)
    return t

def t_ID(t):
    r"[A-Za-z_][A-Za-z0-9_]*"
    palavra = t.value.lower()
    t.type = reservadas.get(palavra, "ID")
    if palavra in reservadas:
        t.value = palavra
    return t

def t_NOVA_LINHA(t):
    r"\n+"
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"[ERRO LÉXICO] Caractere inválido '{t.value[0]}' na linha {t.lexer.lineno}.")
    t.lexer.skip(1)

lexer = lex.lex()