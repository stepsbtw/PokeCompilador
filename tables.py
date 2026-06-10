reservadas = {
    "pokemon": "POKEMON",
    "golpe": "GOLPE",
    "ensinar": "ENSINAR",
    "batalhar": "BATALHAR",
    "usar": "USAR",
}

TIPOS_POKEMON = {
    "fogo": "FOGO",
    "agua": "AGUA",
    "planta": "PLANTA",
    "eletrico": "ELETRICO",
    "pedra": "PEDRA",
    "voador": "VOADOR",
    "terrestre": "TERRESTRE",
    "gelo": "GELO",
    "normal": "NORMAL",
    "lutador": "LUTADOR",
    "sombrio": "SOMBRIO",
    "veneno": "VENENO",
    "inseto": "INSETO",
    "fantasma": "FANTASMA",
    "metal": "METAL",
    "dragao": "DRAGAO",
    "psiquico": "PSIQUICO",
    "fada": "FADA",
}

EFETIVIDADE_TIPO = {
    "fogo": {"planta": 2.0, "gelo": 2.0, "inseto": 2.0, "metal": 2.0, "fogo": 0.5, "agua": 0.5, "pedra": 0.5, "dragao": 0.5},

    "agua": {"fogo": 2.0, "pedra": 2.0, "terrestre": 2.0, "agua": 0.5, "planta": 0.5, "dragao": 0.5},

    "planta": {"agua": 2.0, "pedra": 2.0, "terrestre": 2.0, "fogo": 0.5, "planta": 0.5, "veneno": 0.5, "voador": 0.5, "inseto": 0.5, "dragao": 0.5, "metal": 0.5},

    "eletrico": {"agua": 2.0, "voador": 2.0, "eletrico": 0.5, "planta": 0.5, "dragao": 0.5, "terrestre": 0.0},

    "normal": {"pedra": 0.5, "metal": 0.5, "fantasma": 0.0},

    "pedra": {"fogo": 2.0, "gelo": 2.0, "voador": 2.0, "inseto": 2.0, "lutador": 0.5, "terrestre": 0.5, "metal": 0.5},

    "terrestre": {"fogo": 2.0, "eletrico": 2.0, "veneno": 2.0, "pedra": 2.0, "metal": 2.0, "planta": 0.5, "inseto": 0.5, "voador": 0.0},

    "voador": {"planta": 2.0, "lutador": 2.0, "inseto": 2.0, "eletrico": 0.5, "pedra": 0.5, "metal": 0.5},

    "psiquico": {"lutador": 2.0, "veneno": 2.0, "psiquico": 0.5, "metal": 0.5, "sombrio": 0.0},

    "gelo": {"planta": 2.0, "terrestre": 2.0, "voador": 2.0, "dragao": 2.0, "fogo": 0.5, "agua": 0.5, "gelo": 0.5, "metal": 0.5},

    "dragao": {"dragao": 2.0, "metal": 0.5, "fada": 0.0},

    "sombrio": {"psiquico": 2.0, "fantasma": 2.0, "lutador": 0.5, "sombrio": 0.5, "fada": 0.5},

    "lutador": {"normal": 2.0, "pedra": 2.0, "metal": 2.0, "gelo": 2.0, "sombrio": 2.0, "veneno": 0.5, "voador": 0.5, "psiquico": 0.5, "inseto": 0.5, "fada": 0.5, "fantasma": 0.0},

    "fantasma": {"psiquico": 2.0, "fantasma": 2.0, "sombrio": 0.5, "normal": 0.0},

    "veneno": {"planta": 2.0, "fada": 2.0, "veneno": 0.5, "terrestre": 0.5, "pedra": 0.5, "fantasma": 0.5, "metal": 0.0},

    "inseto": {"planta": 2.0, "psiquico": 2.0, "sombrio": 2.0, "fogo": 0.5, "lutador": 0.5, "veneno": 0.5, "voador": 0.5, "fantasma": 0.5, "metal": 0.5, "fada": 0.5},

    "metal": {"pedra": 2.0, "gelo": 2.0, "fada": 2.0, "fogo": 0.5, "agua": 0.5, "eletrico": 0.5, "metal": 0.5},

    "fada": {"lutador": 2.0, "dragao": 2.0, "sombrio": 2.0, "fogo": 0.5, "veneno": 0.5, "metal": 0.5},
}