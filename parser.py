```python
import ply.yacc as yacc
from lexer import tokens, lexer

def numero(valor):
    return {"tipo": "numero", "valor": valor}

def atributo(nome):
    return {"tipo": "atributo", "nome": nome}

def operacao(op, esquerda, direita):
    return {"tipo": "operacao", "op": op, "esquerda": esquerda, "direita": direita}

def associar_esquerda(inicio, operacoes):
    resultado = inicio
    for op, valor in operacoes:
        resultado = operacao(op, resultado, valor)
    return resultado

def avaliar(no, contexto):
    if no["tipo"] == "numero":
        return no["valor"]
    if no["tipo"] == "atributo":
        return contexto[no["nome"]]
    esquerda = avaliar(no["esquerda"], contexto)
    direita = avaliar(no["direita"], contexto)
    if no["op"] == "+": return esquerda + direita
    if no["op"] == "-": return esquerda - direita
    if no["op"] == "*": return esquerda * direita
    if direita == 0: raise ZeroDivisionError("Divisão por zero na fórmula de dano.")
    return esquerda / direita

def calcular_efetividade(tipo_golpe, tipo_defensor):
    tabela = {
        ("eletrico", "agua"): 2.0,
        ("agua", "eletrico"): 1.0,
        ("agua", "fogo"): 2.0,
        ("fogo", "agua"): 0.5,
        ("fogo", "fogo"): 0.5,
        ("agua", "agua"): 0.5,
        ("eletrico", "eletrico"): 0.5
    }
    return tabela.get((tipo_golpe, tipo_defensor), 1.0)

def calcular_dano(formula, atacante, defensor, golpe):
    contexto = {
        "ataque": atacante["ataque"],
        "defesa": defensor["defesa"],
        "poder": golpe["poder"],
        "efetividade": calcular_efetividade(golpe["tipo"], defensor["tipo"])
    }
    valor = avaliar(formula, contexto)
    return max(0, int(valor)), contexto

def executar_batalha(formula, batalha):
    p1, p2 = batalha["pokemon1"].copy(), batalha["pokemon2"].copy()
    participantes = {p1["nome"]: p1, p2["nome"]: p2}

    if p1["nome"] == p2["nome"]:
        print("[ERRO SEMÂNTICO] Um Pokémon não pode batalhar contra ele mesmo.")
        return None

    print("=" * 40)
    print(f"BATALHA: {p1['nome']} CONTRA {p2['nome']}")
    print("=" * 40)

    turnos_executados = []

    for numero_turno, turno in enumerate(batalha["turnos"], 1):
        if p1["vida"] == 0 or p2["vida"] == 0:
            break

        usuarios = [acao["usuario"] for acao in turno]
        if len(set(usuarios)) != 2 or set(usuarios) != set(participantes):
            print(f"[ERRO SEMÂNTICO] O turno {numero_turno} deve possuir uma ação de cada participante.")
            return None

        print(f"\nTURNO {numero_turno}")
        resultados = []

        for acao in turno:
            atacante = participantes[acao["usuario"]]
            defensor = p2 if atacante["nome"] == p1["nome"] else p1
            dano, contexto = calcular_dano(formula, atacante, defensor, acao["golpe"])
            resultados.append({"atacante": atacante, "defensor": defensor, "golpe": acao["golpe"], "dano": dano, "contexto": contexto})
            print(f"{atacante['nome']} usou {acao['golpe']['nome']}: dano = {dano}")

        for resultado in resultados:
            resultado["defensor"]["vida"] = max(0, resultado["defensor"]["vida"] - resultado["dano"])

        print(f"{p1['nome']}: {p1['vida']} de vida")
        print(f"{p2['nome']}: {p2['vida']} de vida")
        turnos_executados.append(resultados)

    if p1["vida"] > p2["vida"]: vencedor = p1["nome"]
    elif p2["vida"] > p1["vida"]: vencedor = p2["nome"]
    else: vencedor = "empate"

    print("\n" + "=" * 40)
    print(f"RESULTADO: {vencedor.upper()}")
    print("=" * 40)

    return {
        "pokemon1": p1,
        "pokemon2": p2,
        "turnos": turnos_executados,
        "vencedor": vencedor
    }

# S → D B
def p_programa(p):
    "programa : definicao_dano batalha"
    p[0] = {
        "tipo": "programa",
        "formula": p[1],
        "batalha": p[2],
        "resultado": executar_batalha(p[1], p[2])
    }

# D → dano = E ;
def p_definicao_dano(p):
    "definicao_dano : DANO IGUAL expressao PONTO_VIRGULA"
    p[0] = p[3]

# E → TR E'
def p_expressao(p):
    "expressao : termo expressao_linha"
    p[0] = associar_esquerda(p[1], p[2])

# E' → + TR E' | - TR E' | ε
def p_expressao_linha_mais(p):
    "expressao_linha : MAIS termo expressao_linha"
    p[0] = [("+", p[2])] + p[3]

def p_expressao_linha_menos(p):
    "expressao_linha : MENOS termo expressao_linha"
    p[0] = [("-", p[2])] + p[3]

def p_expressao_linha_vazia(p):
    "expressao_linha :"
    p[0] = []

# TR → F TR'
def p_termo(p):
    "termo : fator termo_linha"
    p[0] = associar_esquerda(p[1], p[2])

# TR' → * F TR' | / F TR' | ε
def p_termo_linha_vezes(p):
    "termo_linha : VEZES fator termo_linha"
    p[0] = [("*", p[2])] + p[3]

def p_termo_linha_dividido(p):
    "termo_linha : DIVIDIDO fator termo_linha"
    p[0] = [("/", p[2])] + p[3]

def p_termo_linha_vazia(p):
    "termo_linha :"
    p[0] = []

# F → num | AT | ( E )
def p_fator_numero(p):
    "fator : NUMERO"
    p[0] = numero(p[1])

def p_fator_atributo(p):
    "fator : atributo"
    p[0] = atributo(p[1])

def p_fator_parenteses(p):
    "fator : ABRE_PARENTESES expressao FECHA_PARENTESES"
    p[0] = p[2]

# AT → ataque | defesa | poder | efetividade
def p_atributo(p):
    """atributo : ATAQUE
                | DEFESA
                | PODER
                | EFETIVIDADE"""
    p[0] = p[1]

# B → batalha POK contra POK { LT }
def p_batalha(p):
    "batalha : BATALHA pokemon CONTRA pokemon ABRE_CHAVES lista_turnos FECHA_CHAVES"
    p[0] = {"tipo": "batalha", "pokemon1": p[2], "pokemon2": p[4], "turnos": p[6]}

# POK → id ( TP , num , num , num )
def p_pokemon(p):
    "pokemon : ID ABRE_PARENTESES tipo VIRGULA NUMERO VIRGULA NUMERO VIRGULA NUMERO FECHA_PARENTESES"
    p[0] = {"nome": p[1], "tipo": p[3], "vida": p[5], "ataque": p[7], "defesa": p[9]}
    if p[5] <= 0 or p[7] <= 0 or p[9] <= 0:
        print(f"[ERRO SEMÂNTICO] Os atributos de {p[1]} devem ser maiores que zero.")

# LT → TU LT'
def p_lista_turnos(p):
    "lista_turnos : turno lista_turnos_linha"
    p[0] = [p[1]] + p[2]

# LT' → TU LT' | ε
def p_lista_turnos_linha_turno(p):
    "lista_turnos_linha : turno lista_turnos_linha"
    p[0] = [p[1]] + p[2]

def p_lista_turnos_linha_vazia(p):
    "lista_turnos_linha :"
    p[0] = []

# TU → turno { A A }
def p_turno(p):
    "turno : TURNO ABRE_CHAVES acao acao FECHA_CHAVES"
    p[0] = [p[3], p[4]]

# A → id usa G ;
def p_acao(p):
    "acao : ID USA golpe PONTO_VIRGULA"
    p[0] = {"usuario": p[1], "golpe": p[3]}

# G → id ( TP , num )
def p_golpe(p):
    "golpe : ID ABRE_PARENTESES tipo VIRGULA NUMERO FECHA_PARENTESES"
    p[0] = {"nome": p[1], "tipo": p[3], "poder": p[5]}
    if p[5] <= 0:
        print(f"[ERRO SEMÂNTICO] O poder do golpe {p[1]} deve ser maior que zero.")

# TP → fogo | agua | eletrico
def p_tipo(p):
    """tipo : FOGO
            | AGUA
            | ELETRICO"""
    p[0] = p[1]

def p_error(p):
    if p:
        print(f"[ERRO SINTÁTICO] Token inesperado '{p.value}' na linha {p.lineno}.")
    else:
        print("[ERRO SINTÁTICO] Fim inesperado do programa.")

parser = yacc.yacc(start="programa", write_tables=False, debug=False)

def analisar(codigo):
    lexer.lineno = 1
    return parser.parse(codigo, lexer=lexer)
```
