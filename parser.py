import ply.yacc as yacc
from tables import tokens, EFETIVIDADE_TIPO


pokemons = {}
golpes = {}
batalha_ativa = None

def calcular_dano(atacante, defensor, golpe):
    # dano = ataque + poder - defesa
    # efetividade: super efetivo x2, não muito efetivo x0.5, neutro x1
    # Same Type Attack Bonus (STAB): 
    #   se o tipo do pokemon e do golpe for o mesmo x1.5 o dano.

    dano_base = atacante["atk"] + golpe["poder"] - defensor["def"]

    mult_stab = 1.5 if atacante["tipo"] == golpe["tipo"] else 1
    
    mult_tipo = get_efetividade_tipo(golpe["tipo"], defensor["tipo"])

    dano_final = dano_base * mult_stab * mult_tipo

    if mult_tipo == 0.0:
        dano_final = 0
    
    return dano_final, mult_tipo # retornar o multiplicador pra efetividade

def get_efetividade_tipo(tipo_golpe, tipo_defensor):
    return EFETIVIDADE_TIPO.get(tipo_golpe, {}).get(tipo_defensor, 1.0)

def get_mensagem_efetividade(mult_tipo):
    if mult_tipo == 2.0:
        return "É super efetivo!"
    elif mult_tipo == 0.5:
        return "Não é muito efetivo..."
    elif mult_tipo == 0.0:
        return "Não tem efeito!"
    else:
        return ""


# pokemon NOME TIPO HP ATK DEF SPATK SPDEF SPEED
# pokemon Pikachu eletrico 100 55 50 50 40 90 
def p_criar_pokemon(p):
    # criar_pokemon : POKEMON NOME TIPO NUMERO NUMERO NUMERO NUMERO NUMERO NUMERO
    numero = p[2]
    nome = p[3]
    tipo_pokemon = p[4]
    vida = p[5]
    ataque = p[6]
    defesa = p[7]
    ataque_especial = p[8]
    defesa_especial = p[9]
    velocidade = p[10]

    if nome in pokemons:
        erro_semantico(f"O Pokémon '{nome}' já foi cadastrado.")
        p[0] = None
        return

    if vida <= 0 or ataque <= 0 or defesa <= 0 or velocidade <= 0 or ataque_especial <= 0 or defesa_especial <= 0:
        erro_semantico("HP, ATK, DEF, SPD, SP.ATK e SP.DEF devem ser maiores que zero.")
        p[0] = None
        return

    pokemons[nome] = {
        "numero": numero,
        "nome": nome,
        "tipo": tipo_pokemon,
        "hp_max": vida,
        "hp": vida,
        "atk": ataque,
        "def": defesa,
        "spatk": ataque_especial,
        "spdef": defesa_especial,
        "speed": velocidade,
        "golpes": {}
    }

    print(f"Pokémon cadastrado: {nome} (Tipo: {tipo_pokemon}, HP: {vida}, ATK: {ataque}, DEF: {defesa}, SP.ATK: {ataque_especial}, SP.DEF: {defesa_especial}, SPD: {velocidade})")
    p[0] = ("criar_pokemon", pokemons[nome])

# golpe NOME TIPO PODER PP
# golpe choque_do_tovao eletrico 90 15
def p_criar_golpe(p):
    # criar_golpe: GOLPE NOME TIPO NUMERO NUMERO
    nome = p[2]
    tipo_golpe = p[3]
    poder = p[4]
    pp = p[5]

    if nome in golpes:
        erro_semantico(f"O golpe '{nome}' já foi cadastrado.")

    if pp <= 0:
        erro_semantico("O PP do golpe deve ser maior que zero.")
        p[0] = None
        return

    golpes[nome] = {
        "nome": nome,
        "tipo": tipo_golpe,
        "poder": poder,
        "max_pp": pp
    }    

    print(f"Golpe cadastrado: {nome} ({tipo_golpe}) PODER={poder} PP={pp}")

    p[0] = ("criar_golpe", nome)