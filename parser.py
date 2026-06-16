from copy import deepcopy

import ply.yacc as yacc

from lexer import analisador_lexico, tokens

tabela_efetividade = {}
tabela_pokemon = {}
tabela_golpes = {}

formula_dano = None

erros_semanticos = []


def reiniciar_estado():
    global formula_dano

    tabela_efetividade.clear()
    tabela_pokemon.clear()
    tabela_golpes.clear()
    erros_semanticos.clear()

    formula_dano = None


def erro_semantico(mensagem):
    erros_semanticos.append(mensagem)

    print(
        f"[ERRO SEMÂNTICO] {mensagem}"
    )

def criar_no_numero(valor):
    return {
        "no": "numero",
        "valor": valor,
    }


def criar_no_atributo(nome):
    return {
        "no": "atributo",
        "nome": nome,
    }


def criar_no_operacao(
    operador,
    esquerda,
    direita,
):
    return {
        "no": "operacao_binaria",
        "operador": operador,
        "esquerda": esquerda,
        "direita": direita,
    }


def associar_a_esquerda(
    inicial,
    operacoes,
):
    resultado = inicial

    for operador, operando in operacoes:
        resultado = criar_no_operacao(
            operador,
            resultado,
            operando,
        )

    return resultado

def avaliar_expressao(
    no,
    contexto,
):
    if no["no"] == "numero":
        return no["valor"]

    if no["no"] == "atributo":
        nome = no["nome"]

        if nome not in contexto:
            raise ValueError(
                f"O atributo '{nome}' não está "
                "disponível no contexto."
            )

        return contexto[nome]

    if no["no"] == "operacao_binaria":
        esquerda = avaliar_expressao(
            no["esquerda"],
            contexto,
        )

        direita = avaliar_expressao(
            no["direita"],
            contexto,
        )

        operador = no["operador"]

        if operador == "+":
            return esquerda + direita

        if operador == "-":
            return esquerda - direita

        if operador == "*":
            return esquerda * direita

        if operador == "/":
            if direita == 0:
                raise ZeroDivisionError(
                    "Divisão por zero "
                    "na fórmula de dano."
                )

            return esquerda / direita

    raise ValueError(
        "Nó inválido na árvore da expressão."
    )


def obter_efetividade(
    tipo_golpe,
    tipo_defensor,
):
    return tabela_efetividade.get(
        (
            tipo_golpe,
            tipo_defensor,
        ),
        1.0,
    )

def validar_acao(
    acao,
    participantes,
):
    usuario = acao["usuario"]
    golpe = acao["golpe"]

    valido = True

    if usuario not in participantes:
        erro_semantico(
            f"O Pokémon '{usuario}' "
            "não participa da batalha."
        )

        valido = False

    if usuario not in tabela_pokemon:
        erro_semantico(
            f"O Pokémon '{usuario}' "
            "não foi declarado."
        )

        valido = False

    if golpe not in tabela_golpes:
        erro_semantico(
            f"O golpe '{golpe}' "
            "não foi declarado."
        )

        valido = False

    return valido

def executar_acao(
    acao,
    defensor_nome,
    estado_batalha,
):
    atacante_nome = acao["usuario"]
    golpe_nome = acao["golpe"]

    atacante = estado_batalha[
        atacante_nome
    ]

    defensor = estado_batalha[
        defensor_nome
    ]

    golpe = tabela_golpes[
        golpe_nome
    ]

    efetividade = obter_efetividade(
        golpe["tipo"],
        defensor["tipo"],
    )

    contexto = {
        "ataque": atacante["ataque"],
        "defesa": defensor["defesa"],
        "poder": golpe["poder"],
        "efetividade": efetividade,
    }

    try:
        dano_calculado = avaliar_expressao(
            formula_dano,
            contexto,
        )

    except (
        ValueError,
        ZeroDivisionError,
    ) as erro:
        erro_semantico(
            str(erro)
        )

        return None

    dano_aplicado = max(
        0,
        int(dano_calculado),
    )

    vida_anterior = defensor["vida"]

    defensor["vida"] = max(
        0,
        defensor["vida"] - dano_aplicado,
    )

    print(
        f"\n[AÇÃO] {atacante_nome} usou "
        f"{golpe_nome} em {defensor_nome}."
    )

    print(
        f"[VALORES] "
        f"ataque={atacante['ataque']} | "
        f"poder={golpe['poder']} | "
        f"defesa={defensor['defesa']} | "
        f"efetividade={efetividade}"
    )

    print(
        f"[DANO] "
        f"calculado={dano_calculado} | "
        f"aplicado={dano_aplicado}"
    )

    print(
        f"[VIDA] {defensor_nome}: "
        f"{vida_anterior} -> {defensor['vida']}"
    )

    return {
        "atacante": atacante_nome,
        "defensor": defensor_nome,
        "golpe": golpe_nome,
        "dano": dano_aplicado,
        "vida_restante": defensor["vida"],
    }

def executar_batalha(batalha):
    pokemon_1 = batalha["pokemon_1"]
    pokemon_2 = batalha["pokemon_2"]

    valida = True

    if pokemon_1 not in tabela_pokemon:
        erro_semantico(
            f"O Pokémon '{pokemon_1}' "
            "não foi declarado."
        )

        valida = False

    if pokemon_2 not in tabela_pokemon:
        erro_semantico(
            f"O Pokémon '{pokemon_2}' "
            "não foi declarado."
        )

        valida = False

    if pokemon_1 == pokemon_2:
        erro_semantico(
            "Um Pokémon não pode batalhar "
            "contra ele mesmo."
        )

        valida = False

    if formula_dano is None:
        erro_semantico(
            "A fórmula de dano não foi declarada."
        )

        valida = False

    participantes = [
        pokemon_1,
        pokemon_2,
    ]

    for acao in batalha["acoes"]:
        if not validar_acao(
            acao,
            participantes,
        ):
            valida = False

    usuarios = [
        acao["usuario"]
        for acao in batalha["acoes"]
    ]

    if set(usuarios) != set(participantes):
        erro_semantico(
            "A batalha deve conter uma ação "
            "de cada participante."
        )

        valida = False

    if not valida:
        return {
            "valida": False,
            "acoes": [],
        }

    estado_batalha = {
        pokemon_1: deepcopy(
            tabela_pokemon[pokemon_1]
        ),

        pokemon_2: deepcopy(
            tabela_pokemon[pokemon_2]
        ),
    }

    print(
        "\n========================================"
    )

    print(
        f"BATALHA: {pokemon_1} CONTRA {pokemon_2}"
    )

    print(
        "========================================"
    )

    resultados = []

    for acao in batalha["acoes"]:
        atacante = acao["usuario"]

        if atacante == pokemon_1:
            defensor = pokemon_2
        else:
            defensor = pokemon_1

        resultado = executar_acao(
            acao,
            defensor,
            estado_batalha,
        )

        resultados.append(
            resultado
        )

    print(
        "\n========================================"
    )

    print(
        "RESULTADO"
    )

    print(
        "========================================"
    )

    print(
        f"{pokemon_1}: "
        f"{estado_batalha[pokemon_1]['vida']} VIDA"
    )

    print(
        f"{pokemon_2}: "
        f"{estado_batalha[pokemon_2]['vida']} VIDA"
    )

    return {
        "valida": True,

        "vida_pokemon_1":
            estado_batalha[pokemon_1]["vida"],

        "vida_pokemon_2":
            estado_batalha[pokemon_2]["vida"],

        "acoes": resultados,
    }


# ============================================================
# PROGRAMA
#
# P → RE D DEC B
# ============================================================

def p_programa(p):
    """
    programa : regras_efetividade regra_dano declaracoes batalha
    """

    resultado_batalha = executar_batalha(
        p[4]
    )

    p[0] = {
        "no": "programa",
        "regras_efetividade": p[1],
        "regra_dano": p[2],
        "declaracoes": p[3],
        "batalha": p[4],
        "resultado_batalha":
            resultado_batalha,
        "erros_semanticos":
            list(erros_semanticos),
    }


# ============================================================
# REGRAS DE EFETIVIDADE
#
# RE → R RE'
# RE' → R RE' | ε
# ============================================================

def p_regras_efetividade(p):
    """
    regras_efetividade : regra_efetividade regras_efetividade_linha
    """

    p[0] = [
        p[1]
    ] + p[2]


def p_regras_efetividade_linha_mais(p):
    """
    regras_efetividade_linha : regra_efetividade regras_efetividade_linha
    """

    p[0] = [
        p[1]
    ] + p[2]


def p_regras_efetividade_linha_vazia(p):
    """
    regras_efetividade_linha :
    """

    p[0] = []


def p_regra_efetividade(p):
    """
    regra_efetividade : EFETIVIDADE tipo_pokemon CONTRA tipo_pokemon IGUAL NUMERO PONTO_VIRGULA
    """

    tipo_atacante = p[2]
    tipo_defensor = p[4]
    multiplicador = p[6]

    chave = (
        tipo_atacante,
        tipo_defensor,
    )

    if chave in tabela_efetividade:
        erro_semantico(
            f"A efetividade de "
            f"'{tipo_atacante}' contra "
            f"'{tipo_defensor}' "
            "já foi declarada."
        )

    else:
        tabela_efetividade[
            chave
        ] = multiplicador

    p[0] = {
        "no": "regra_efetividade",
        "tipo_atacante": tipo_atacante,
        "tipo_defensor": tipo_defensor,
        "multiplicador": multiplicador,
    }


# ============================================================
# REGRA DE DANO
#
# D → dano = E ;
# ============================================================

def p_regra_dano(p):
    """
    regra_dano : DANO IGUAL expressao PONTO_VIRGULA
    """

    global formula_dano

    formula_dano = p[3]

    p[0] = {
        "no": "regra_dano",
        "expressao": p[3],
    }


# ============================================================
# EXPRESSÕES
#
# E  → T E'
# E' → + T E' | - T E' | ε
#
# T  → F T'
# T' → * F T' | / F T' | ε
#
# F → num | AT | ( E )
# ============================================================

def p_expressao(p):
    """
    expressao : termo expressao_linha
    """

    p[0] = associar_a_esquerda(
        p[1],
        p[2],
    )


def p_expressao_linha_mais(p):
    """
    expressao_linha : MAIS termo expressao_linha
    """

    p[0] = [
        (
            "+",
            p[2],
        )
    ] + p[3]


def p_expressao_linha_menos(p):
    """
    expressao_linha : MENOS termo expressao_linha
    """

    p[0] = [
        (
            "-",
            p[2],
        )
    ] + p[3]


def p_expressao_linha_vazia(p):
    """
    expressao_linha :
    """

    p[0] = []


def p_termo(p):
    """
    termo : fator termo_linha
    """

    p[0] = associar_a_esquerda(
        p[1],
        p[2],
    )


def p_termo_linha_vezes(p):
    """
    termo_linha : VEZES fator termo_linha
    """

    p[0] = [
        (
            "*",
            p[2],
        )
    ] + p[3]


def p_termo_linha_dividido(p):
    """
    termo_linha : DIVIDIDO fator termo_linha
    """

    p[0] = [
        (
            "/",
            p[2],
        )
    ] + p[3]


def p_termo_linha_vazia(p):
    """
    termo_linha :
    """

    p[0] = []


def p_fator_numero(p):
    """
    fator : NUMERO
    """

    p[0] = criar_no_numero(
        p[1]
    )


def p_fator_atributo(p):
    """
    fator : atributo
    """

    p[0] = criar_no_atributo(
        p[1]
    )


def p_fator_parenteses(p):
    """
    fator : ABRE_PARENTESES expressao FECHA_PARENTESES
    """

    p[0] = p[2]


def p_atributo(p):
    """
    atributo : ATAQUE
             | DEFESA
             | PODER
             | EFETIVIDADE
    """

    p[0] = p[1]


# ============================================================
# DECLARAÇÕES
#
# DEC  → DC DEC'
# DEC' → DC DEC' | ε
# DC   → DP | DG
# ============================================================

def p_declaracoes(p):
    """
    declaracoes : declaracao declaracoes_linha
    """

    p[0] = [
        p[1]
    ] + p[2]


def p_declaracoes_linha_mais(p):
    """
    declaracoes_linha : declaracao declaracoes_linha
    """

    p[0] = [
        p[1]
    ] + p[2]


def p_declaracoes_linha_vazia(p):
    """
    declaracoes_linha :
    """

    p[0] = []


def p_declaracao(p):
    """
    declaracao : declaracao_pokemon
               | declaracao_golpe
    """

    p[0] = p[1]

def p_declaracao_pokemon(p):
    """
    declaracao_pokemon : POKEMON ID DOIS_PONTOS tipo_pokemon ABRE_CHAVES atributos_pokemon FECHA_CHAVES
    """

    nome = p[2]
    tipo = p[4]
    atributos = p[6]

    if nome in tabela_pokemon:
        erro_semantico(
            f"O Pokémon '{nome}' "
            "já foi declarado."
        )

    else:
        tabela_pokemon[nome] = {
            "nome": nome,
            "tipo": tipo,
            "vida": atributos["vida"],
            "ataque": atributos["ataque"],
            "defesa": atributos["defesa"],
        }

    p[0] = {
        "no": "declaracao_pokemon",
        "nome": nome,
        "tipo": tipo,
        "atributos": atributos,
    }


def p_atributos_pokemon(p):
    """
    atributos_pokemon : VIDA IGUAL NUMERO PONTO_VIRGULA ATAQUE IGUAL NUMERO PONTO_VIRGULA DEFESA IGUAL NUMERO PONTO_VIRGULA
    """

    atributos = {
        "vida": p[3],
        "ataque": p[7],
        "defesa": p[11],
    }

    for nome, valor in atributos.items():
        if valor <= 0:
            erro_semantico(
                f"O atributo '{nome}' "
                "deve ser maior que zero."
            )

    p[0] = atributos

def p_declaracao_golpe(p):
    """
    declaracao_golpe : GOLPE ID DOIS_PONTOS tipo_pokemon ABRE_CHAVES atributos_golpe FECHA_CHAVES
    """

    nome = p[2]
    tipo = p[4]
    atributos = p[6]

    if nome in tabela_golpes:
        erro_semantico(
            f"O golpe '{nome}' "
            "já foi declarado."
        )

    else:
        tabela_golpes[nome] = {
            "nome": nome,
            "tipo": tipo,
            "poder": atributos["poder"],
        }

    p[0] = {
        "no": "declaracao_golpe",
        "nome": nome,
        "tipo": tipo,
        "atributos": atributos,
    }


def p_atributos_golpe(p):
    """
    atributos_golpe : PODER IGUAL NUMERO PONTO_VIRGULA
    """

    if p[3] <= 0:
        erro_semantico(
            "O poder do golpe deve "
            "ser maior que zero."
        )

    p[0] = {
        "poder": p[3],
    }

def p_tipo_pokemon(p):
    """
    tipo_pokemon : FOGO
                 | AGUA
                 | ELETRICO
    """

    p[0] = p[1]


# ============================================================
# BATALHA
#
# B → batalha id contra id { A A }
# A → id usa id ;
# ============================================================

def p_batalha(p):
    """
    batalha : BATALHA ID CONTRA ID ABRE_CHAVES acao acao FECHA_CHAVES
    """

    p[0] = {
        "no": "batalha",
        "pokemon_1": p[2],
        "pokemon_2": p[4],
        "acoes": [
            p[6],
            p[7],
        ],
    }


def p_acao(p):
    """
    acao : ID USA ID PONTO_VIRGULA
    """

    p[0] = {
        "no": "acao",
        "usuario": p[1],
        "golpe": p[3],
    }

def p_error(p):
    if p is None:
        print(
            "[ERRO SINTÁTICO] "
            "Fim inesperado da entrada."
        )

    else:
        print(
            f"[ERRO SINTÁTICO] "
            f"Token inesperado '{p.value}' "
            f"na linha {p.lineno}."
        )

analisador_sintatico = yacc.yacc(
    start="programa",
    write_tables=False,
    debug=False,
)


def analisar_codigo(codigo_fonte):
    reiniciar_estado()

    analisador_lexico.lineno = 1

    return analisador_sintatico.parse(
        codigo_fonte,
        lexer=analisador_lexico,
    )