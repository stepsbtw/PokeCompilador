# PokeLang

Linguagem desenvolvida para a disciplina de **Compiladores** utilizando **Python** e **PLY**.

A PokeLang permite definir uma fórmula de dano e executar uma batalha simplificada entre dois Pokémon, contendo um ou mais turnos.

## Autores

* Caio Passos Torkst Ferreira
* Daniel 

---

# Estrutura do projeto

* `lexer.py`: análise léxica;
* `parser.py`: análise sintática e semântica;
* `main.py`: execução do programa;
* `exemplo.poke`: programa de exemplo;
* `requirements.txt`: dependências.

---

# 1. Análise léxica

A análise léxica é realizada pelo módulo `ply.lex`. Sua função é transformar o código-fonte em uma sequência de tokens.

## Palavras reservadas

```text
dano, batalha, contra, turno, usa, ataque, defesa, poder, efetividade, fogo, agua, eletrico
```

## Expressões regulares

| Token              | Expressão regular        | Exemplo                |
| ------------------ | ------------------------ | ---------------------- |
| `ID`               | `[A-Za-z_][A-Za-z0-9_]*` | `Pikachu`, `jato_agua` |
| `NUMERO`           | `\d+(\.\d+)?`            | `200`, `2.0`           |
| `MAIS`             | `\+`                     | `+`                    |
| `MENOS`            | `-`                      | `-`                    |
| `VEZES`            | `\*`                     | `*`                    |
| `DIVIDIDO`         | `/`                      | `/`                    |
| `IGUAL`            | `=`                      | `=`                    |
| `VIRGULA`          | `,`                      | `,`                    |
| `PONTO_VIRGULA`    | `;`                      | `;`                    |
| `ABRE_PARENTESES`  | `\(`                     | `(`                    |
| `FECHA_PARENTESES` | `\)`                     | `)`                    |
| `ABRE_CHAVES`      | `\{`                     | `{`                    |
| `FECHA_CHAVES`     | `\}`                     | `}`                    |
| `COMENTARIO`       | `\#.*`                   | `# comentário`         |
| `NOVA_LINHA`       | `\n+`                    | quebra de linha        |

Espaços e tabulações são ignorados:

```text
[ \t\r]+
```

Os identificadores são comparados com a tabela de palavras reservadas:

```text
Pikachu → ID
choque → ID
batalha → BATALHA
turno → TURNO
ataque → ATAQUE
```

Um caractere que não corresponde a nenhuma expressão regular gera um erro léxico.

---

# 2. Análise sintática

A análise sintática é realizada pelo módulo `ply.yacc`. Ela verifica se a sequência de tokens pertence à gramática da PokeLang.

## Definição formal

A gramática é definida por:

```text
G = (V, Σ, P, S)
```

Em que:

```text
V = conjunto de símbolos não terminais
Σ = conjunto de símbolos terminais
P = conjunto de produções
S = símbolo inicial
```

## Não terminais

```text
V = { S, D, E, E', TR, TR', F, AT, B, POK, LT, LT', TU, A, G, TP }
```

| Símbolo | Significado                    |
| ------- | ------------------------------ |
| `S`     | programa                       |
| `D`     | definição da fórmula de dano   |
| `E`     | expressão                      |
| `E'`    | continuação da expressão       |
| `TR`    | termo                          |
| `TR'`   | continuação do termo           |
| `F`     | fator                          |
| `AT`    | atributo                       |
| `B`     | batalha                        |
| `POK`   | Pokémon                        |
| `LT`    | lista de turnos                |
| `LT'`   | continuação da lista de turnos |
| `TU`    | turno                          |
| `A`     | ação                           |
| `G`     | golpe                          |
| `TP`    | tipo                           |

## Terminais

```text
Σ = { dano, batalha, contra, turno, usa, ataque, defesa, poder, efetividade, fogo, agua, eletrico, id, num, +, -, *, /, =, ,, ;, {, }, (, ) }
```

```text
id = identificador
num = número inteiro ou real
```

## Símbolo inicial

```text
S
```

## Gramática

```text
S → D B
D → dano = E ;
E → TR E'
E' → + TR E' | - TR E' | ε
TR → F TR'
TR' → * F TR' | / F TR' | ε
F → num | AT | ( E )
AT → ataque | defesa | poder | efetividade
B → batalha POK contra POK { LT }
POK → id ( TP , num , num , num )
LT → TU LT'
LT' → TU LT' | ε
TU → turno { A A }
A → id usa G ;
G → id ( TP , num )
TP → fogo | agua | eletrico
```

O símbolo `ε` representa a cadeia vazia.

## Estrutura dos Pokémon

```text
POK → id ( TP , num , num , num )
```

A ordem dos valores é:

```text
id(tipo, vida, ataque, defesa)
```

Exemplo:

```text
Pikachu(eletrico, 200, 80, 50)
```

## Estrutura dos golpes

```text
G → id ( TP , num )
```

A ordem dos valores é:

```text
id(tipo, poder)
```

Exemplo:

```text
choque(eletrico, 60)
```

## Precedência e associatividade

A gramática das expressões utiliza três níveis:

```text
E = expressão
TR = termo
F = fator
```

Multiplicação e divisão são reconhecidas em `TR`, enquanto soma e subtração são reconhecidas em `E`.

```text
ataque + poder * efetividade
```

é interpretado como:

```text
ataque + (poder * efetividade)
```

Operações do mesmo nível são avaliadas da esquerda para a direita:

```text
ataque - poder - defesa
```

é interpretado como:

```text
(ataque - poder) - defesa
```

## Repetição dos turnos

A repetição é representada por:

```text
LT → TU LT'
LT' → TU LT' | ε
```

Uma batalha possui pelo menos um turno. Cada aplicação de `LT' → TU LT'` adiciona outro turno, enquanto `LT' → ε` encerra a lista.

Para dois turnos:

```text
LT
├── TU
└── LT'
    ├── TU
    └── LT'
        └── ε
```

## Programa de exemplo

```text
dano = (ataque + poder - defesa) * efetividade;

batalha Pikachu(eletrico, 200, 80, 50) contra Squirtle(agua, 220, 70, 70) {
    turno { Pikachu usa choque(eletrico, 60); Squirtle usa jato_agua(agua, 50); }
    turno { Pikachu usa choque(eletrico, 60); Squirtle usa jato_agua(agua, 50); }
}
```

## Árvore de derivação

A árvore possui dois ramos principais:

```text
S
├── D
└── B
```

A árvore de derivação do programa de exemplo é representada por:

```text
S
├── D
│   ├── dano
│   ├── =
│   ├── E
│   │   ├── TR
│   │   │   ├── F
│   │   │   │   ├── (
│   │   │   │   ├── E
│   │   │   │   │   ├── TR
│   │   │   │   │   │   ├── F
│   │   │   │   │   │   │   └── AT
│   │   │   │   │   │   │       └── ataque
│   │   │   │   │   │   └── TR'
│   │   │   │   │   │       └── ε
│   │   │   │   │   └── E'
│   │   │   │   │       ├── +
│   │   │   │   │       ├── TR
│   │   │   │   │       │   ├── F
│   │   │   │   │       │   │   └── AT
│   │   │   │   │       │   │       └── poder
│   │   │   │   │       │   └── TR'
│   │   │   │   │       │       └── ε
│   │   │   │   │       └── E'
│   │   │   │   │           ├── -
│   │   │   │   │           ├── TR
│   │   │   │   │           │   ├── F
│   │   │   │   │           │   │   └── AT
│   │   │   │   │           │   │       └── defesa
│   │   │   │   │           │   └── TR'
│   │   │   │   │           │       └── ε
│   │   │   │   │           └── E'
│   │   │   │   │               └── ε
│   │   │   │   └── )
│   │   │   └── TR'
│   │   │       ├── *
│   │   │       ├── F
│   │   │       │   └── AT
│   │   │       │       └── efetividade
│   │   │       └── TR'
│   │   │           └── ε
│   │   └── E'
│   │       └── ε
│   └── ;
│
└── B
    ├── batalha
    ├── POK
    │   ├── id → Pikachu
    │   ├── (
    │   ├── TP → eletrico
    │   ├── ,
    │   ├── num → 200
    │   ├── ,
    │   ├── num → 80
    │   ├── ,
    │   ├── num → 50
    │   └── )
    ├── contra
    ├── POK
    │   ├── id → Squirtle
    │   ├── (
    │   ├── TP → agua
    │   ├── ,
    │   ├── num → 220
    │   ├── ,
    │   ├── num → 70
    │   ├── ,
    │   ├── num → 70
    │   └── )
    ├── {
    ├── LT
    │   ├── TU
    │   │   ├── turno
    │   │   ├── {
    │   │   ├── A
    │   │   │   ├── id → Pikachu
    │   │   │   ├── usa
    │   │   │   ├── G → choque(eletrico, 60)
    │   │   │   └── ;
    │   │   ├── A
    │   │   │   ├── id → Squirtle
    │   │   │   ├── usa
    │   │   │   ├── G → jato_agua(agua, 50)
    │   │   │   └── ;
    │   │   └── }
    │   └── LT'
    │       ├── TU
    │       │   ├── turno
    │       │   ├── {
    │       │   ├── A → Pikachu usa choque(eletrico, 60);
    │       │   ├── A → Squirtle usa jato_agua(agua, 50);
    │       │   └── }
    │       └── LT'
    │           └── ε
    └── }
```

---

# 3. Análise semântica

A análise semântica atribui significado às estruturas reconhecidas pelo analisador sintático.

Ela é responsável por:

* armazenar a fórmula de dano;
* interpretar os dados dos Pokémon e golpes;
* validar os participantes;
* calcular a efetividade;
* calcular os danos;
* atualizar as vidas;
* determinar o vencedor.

## Tabela de produções e ações semânticas

| Produção                                        | Ação semântica                           |
| ----------------------------------------------- | ---------------------------------------- |
| `S → D B`                                       | Armazena a fórmula e executa a batalha   |
| `D → dano = E ;`                                | Armazena a árvore da expressão           |
| `E → TR E'`                                     | Constrói somas e subtrações              |
| `E' → + TR E'`                                  | Adiciona uma soma                        |
| `E' → - TR E'`                                  | Adiciona uma subtração                   |
| `E' → ε`                                        | Finaliza a expressão                     |
| `TR → F TR'`                                    | Constrói multiplicações e divisões       |
| `TR' → * F TR'`                                 | Adiciona uma multiplicação               |
| `TR' → / F TR'`                                 | Adiciona uma divisão                     |
| `TR' → ε`                                       | Finaliza o termo                         |
| `F → num`                                       | Produz um número                         |
| `F → AT`                                        | Produz um atributo                       |
| `F → ( E )`                                     | Propaga a expressão interna              |
| `AT → ataque \| defesa \| poder \| efetividade` | Produz o atributo correspondente         |
| `B → batalha POK1 contra POK2 { LT }`           | Inicializa a batalha e executa os turnos |
| `POK → id ( TP, num1, num2, num3 )`             | Produz nome, tipo, vida, ataque e defesa |
| `LT → TU LT'`                                   | Cria a lista de turnos                   |
| `LT' → TU LT'`                                  | Adiciona um turno                        |
| `LT' → ε`                                       | Finaliza a lista                         |
| `TU → turno { A1 A2 }`                          | Calcula os danos e atualiza as vidas     |
| `A → id usa G ;`                                | Produz o usuário e o golpe               |
| `G → id ( TP, num )`                            | Produz nome, tipo e poder do golpe       |
| `TP → fogo \| agua \| eletrico`                 | Produz o tipo correspondente             |

## Regra de efetividade

A efetividade é determinada a partir do tipo do golpe e do tipo do defensor.

```text
efetividade(eletrico, agua) = 2.0
efetividade(agua, eletrico) = 1.0
efetividade(outros casos) = 1.0
```

## Regra de dano

```text
dano = (ataque + poder - defesa) * efetividade
```

O dano aplicado não pode ser negativo:

```text
dano_aplicado = max(0, dano)
```

## Árvore sintática abstrata da fórmula

```text
*
├── -
│   ├── +
│   │   ├── ataque
│   │   └── poder
│   └── defesa
└── efetividade
```

## Atualização das vidas

As duas ações de um turno são calculadas com os valores existentes no início daquele turno. Depois, as duas vidas são atualizadas.

```text
vida_saida_P1 = max(0, vida_entrada_P1 - dano_P2)
vida_saida_P2 = max(0, vida_entrada_P2 - dano_P1)
```

A saída de um turno é utilizada como entrada do próximo:

```text
TU2.vida_entrada_P1 = TU1.vida_saida_P1
TU2.vida_entrada_P2 = TU1.vida_saida_P2
```

## Primeiro turno

Ação de Pikachu:

```text
ataque = 80
poder = 60
defesa = 70
efetividade = 2.0
```

Árvore anotada da expressão:

```text
* = 140
├── - = 70
│   ├── + = 140
│   │   ├── ataque = 80
│   │   └── poder = 60
│   └── defesa = 70
└── efetividade = 2.0
```

```text
dano_Pikachu = (80 + 60 - 70) * 2.0 = 140
```

Ação de Squirtle:

```text
dano_Squirtle = (70 + 50 - 50) * 1.0 = 70
```

Vidas após o primeiro turno:

```text
Pikachu.vida = 200 - 70 = 130
Squirtle.vida = 220 - 140 = 80
```

## Segundo turno

```text
Pikachu.vida = max(0, 130 - 70) = 60
Squirtle.vida = max(0, 80 - 140) = 0
```

## Árvore anotada completa

```text
S
├── D
│   └── expressão = (ataque + poder - defesa) * efetividade
│
└── B
    ├── POK1 = { nome = Pikachu, tipo = eletrico, vida = 200, ataque = 80, defesa = 50 }
    ├── POK2 = { nome = Squirtle, tipo = agua, vida = 220, ataque = 70, defesa = 70 }
    │
    └── LT
        ├── TU1
        │   ├── A1 = { usuario = Pikachu, golpe = choque, poder = 60, efetividade = 2.0, dano = 140 }
        │   ├── A2 = { usuario = Squirtle, golpe = jato_agua, poder = 50, efetividade = 1.0, dano = 70 }
        │   ├── vida_Pikachu = 130
        │   └── vida_Squirtle = 80
        │
        └── LT'
            ├── TU2
            │   ├── A1 = { usuario = Pikachu, golpe = choque, dano = 140 }
            │   ├── A2 = { usuario = Squirtle, golpe = jato_agua, dano = 70 }
            │   ├── vida_Pikachu = 60
            │   ├── vida_Squirtle = 0
            │   └── vencedor = Pikachu
            │
            └── LT'
                └── ε
```

## Determinação do vencedor

```text
se vida_P1 = 0 e vida_P2 > 0, vencedor = P2
se vida_P2 = 0 e vida_P1 > 0, vencedor = P1
se vida_P1 = 0 e vida_P2 = 0, resultado = empate
```

No programa de exemplo:

```text
Pikachu.vida_final = 60
Squirtle.vida_final = 0
vencedor = Pikachu
```

---

# Execução

## Instalação

```bash
pip install -r requirements.txt
```

## Comando

```bash
python main.py exemplo.poke
```

## Saída esperada

```text
========================================
BATALHA: Pikachu CONTRA Squirtle
========================================

TURNO 1
Pikachu usou choque: dano = 140
Squirtle usou jato_agua: dano = 70
Pikachu: 130 de vida
Squirtle: 80 de vida

TURNO 2
Pikachu usou choque: dano = 140
Squirtle usou jato_agua: dano = 70
Pikachu: 60 de vida
Squirtle: 0 de vida

========================================
VENCEDOR: Pikachu
========================================
```

---

# Uso de inteligência artificial

Uma ferramenta de inteligência artificial foi utilizada para auxiliar na organização da gramática, simplificação do domínio, elaboração das árvores e revisão da documentação.

Prompts principais:

```text
Crie uma linguagem de domínio específico para demonstrar análise léxica, sintática e semântica utilizando PLY.
```

```text
Simplifique uma gramática de batalhas Pokémon mantendo expressão de dano, repetição de turnos e ações semânticas.
```

```text
Defina formalmente a gramática e construa uma árvore de derivação e uma árvore anotada.
```

As respostas foram revisadas e adaptadas pelos integrantes para definir o escopo final da linguagem.
