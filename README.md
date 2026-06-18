# PokeLang

A **PokeLang** é uma linguagem de domínio específico para representar batalhas simplificadas entre Pokémon.

A linguagem permite:

* definir uma fórmula de dano;
* declarar dois Pokémon;
* definir golpes;
* executar um ou mais turnos;
* calcular o dano e determinar o vencedor.

## Autores

* Caio Passos Torkst Ferreira
* Daniel Salvador Motta

## Gerador utilizado

O projeto foi desenvolvido em **Python** utilizando o **PLY**:

```text
ply.lex  → analisador léxico
ply.yacc → analisador sintático
```

---

# 1. Análise léxica

A análise léxica transforma o código-fonte em uma sequência de tokens.

## Palavras reservadas

```text
dano, batalha, contra, turno, usa, ataque, defesa, poder,
efetividade, fogo, agua, eletrico
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

Exemplos de reconhecimento:

```text
Pikachu   → ID
choque    → ID
batalha   → BATALHA
turno     → TURNO
ataque    → ATAQUE
200       → NUMERO
```

Caracteres que não pertencem à linguagem geram erro léxico.

---

# 2. Análise sintática

A análise sintática verifica se a sequência de tokens pertence à gramática da PokeLang.

## Definição formal

```text
G = (V, Σ, P, S)
```

## Não terminais

```text
V = { S, D, E, E', TR, TR', F, AT, B, POK, LT, LT', TU, A, G, TP }
```

| Símbolo | Significado                  |
| ------- | ---------------------------- |
| `S`     | programa                     |
| `D`     | definição da fórmula de dano |
| `E`     | expressão                    |
| `E'`    | continuação da expressão     |
| `TR`    | termo                        |
| `TR'`   | continuação do termo         |
| `F`     | fator                        |
| `AT`    | atributo                     |
| `B`     | batalha                      |
| `POK`   | Pokémon                      |
| `LT`    | lista de turnos              |
| `LT'`   | continuação da lista         |
| `TU`    | turno                        |
| `A`     | ação                         |
| `G`     | golpe                        |
| `TP`    | tipo                         |

## Terminais

```text
Σ = {
    dano, batalha, contra, turno, usa,
    ataque, defesa, poder, efetividade,
    fogo, agua, eletrico,
    id, num, +, -, *, /, =, ,, ;, {, }, (, )
}
```

## Símbolo inicial

```text
S
```

## Produções

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

## Estrutura de um Pokémon

```text
id(tipo, vida, ataque, defesa)
```

Exemplo:

```text
Pikachu(eletrico, 200, 80, 50)
```

## Estrutura de um golpe

```text
id(tipo, poder)
```

Exemplo:

```text
choque(eletrico, 60)
```

## Precedência e associatividade

A gramática possui três níveis:

```text
E  → soma e subtração
TR → multiplicação e divisão
F  → números, atributos e parênteses
```

Assim:

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

## Repetição de turnos

```text
LT → TU LT'
LT' → TU LT' | ε
```

A batalha deve possuir pelo menos um turno.

Cada aplicação de:

```text
LT' → TU LT'
```

adiciona outro turno.

A produção:

```text
LT' → ε
```

encerra a lista.

---

# Programa de exemplo

```text
dano = (ataque + poder - defesa) * efetividade;

batalha Pikachu(eletrico, 200, 80, 50) contra Squirtle(agua, 220, 70, 70) {
    turno { Pikachu usa choque(eletrico, 60); Squirtle usa jato_agua(agua, 50); }
    turno { Pikachu usa choque(eletrico, 60); Squirtle usa jato_agua(agua, 50); }
}
```

---

# Árvore de derivação

Para manter a árvore legível, é utilizada uma sentença com apenas um turno:

```text
dano = (ataque + poder - defesa) * efetividade;

batalha Pikachu(eletrico, 200, 80, 50) contra Squirtle(agua, 220, 70, 70) {
    turno { Pikachu usa choque(eletrico, 60); Squirtle usa jato_agua(agua, 50); }
}
```

Árvore:

```text
S
├── D
│   ├── dano
│   ├── =
│   ├── E
│   │   └── (ataque + poder - defesa) * efetividade
│   └── ;
│
└── B
    ├── batalha
    ├── POK
    │   ├── id → Pikachu
    │   ├── TP → eletrico
    │   ├── num → 200
    │   ├── num → 80
    │   └── num → 50
    ├── contra
    ├── POK
    │   ├── id → Squirtle
    │   ├── TP → agua
    │   ├── num → 220
    │   ├── num → 70
    │   └── num → 70
    ├── {
    ├── LT
    │   ├── TU
    │   │   ├── turno
    │   │   ├── {
    │   │   ├── A
    │   │   │   ├── id → Pikachu
    │   │   │   ├── usa
    │   │   │   └── G → choque(eletrico, 60)
    │   │   ├── A
    │   │   │   ├── id → Squirtle
    │   │   │   ├── usa
    │   │   │   └── G → jato_agua(agua, 50)
    │   │   └── }
    │   └── LT'
    │       └── ε
    └── }
```

---

# 3. Análise semântica

A análise semântica atribui significado às estruturas reconhecidas pela gramática.

Ela é responsável por:

* armazenar a fórmula de dano;
* construir os Pokémon e os golpes;
* calcular a efetividade;
* calcular o dano;
* atualizar as vidas;
* determinar o vencedor.

## Tabela de produções e ações semânticas

| Produção                               | Ação semântica                                                       |
| -------------------------------------- | -------------------------------------------------------------------- |
| `S → D B`                              | `S.resultado = executar_batalha(D.formula, B)`                       |
| `D → dano = E ;`                       | `D.formula = E.valor`                                                |
| `E → TR E'`                            | `E.valor = aplicar(TR.valor, E'.operacoes)`                          |
| `E' → + TR E'1`                        | `E'.operacoes = [+, TR.valor] + E'1.operacoes`                       |
| `E' → - TR E'1`                        | `E'.operacoes = [-, TR.valor] + E'1.operacoes`                       |
| `E' → ε`                               | `E'.operacoes = []`                                                  |
| `TR → F TR'`                           | `TR.valor = aplicar(F.valor, TR'.operacoes)`                         |
| `TR' → * F TR'1`                       | `TR'.operacoes = [*, F.valor] + TR'1.operacoes`                      |
| `TR' → / F TR'1`                       | `TR'.operacoes = [/, F.valor] + TR'1.operacoes`                      |
| `TR' → ε`                              | `TR'.operacoes = []`                                                 |
| `F → num`                              | `F.valor = num.valor`                                                |
| `F → AT`                               | `F.valor = AT.valor`                                                 |
| `F → ( E )`                            | `F.valor = E.valor`                                                  |
| `AT → ataque`                          | `AT.valor = atacante.ataque`                                         |
| `AT → defesa`                          | `AT.valor = defensor.defesa`                                         |
| `AT → poder`                           | `AT.valor = golpe.poder`                                             |
| `AT → efetividade`                     | `AT.valor = efetividade(golpe.tipo, defensor.tipo)`                  |
| `POK → id ( TP , num1 , num2 , num3 )` | `POK = {nome: id, tipo: TP, vida: num1, ataque: num2, defesa: num3}` |
| `G → id ( TP , num )`                  | `G = {nome: id, tipo: TP, poder: num}`                               |
| `A → id usa G ;`                       | `A = {usuario: id, golpe: G}`                                        |
| `TU → turno { A1 A2 }`                 | `TU.acoes = [A1, A2]`                                                |
| `LT → TU LT'`                          | `LT.lista = [TU] + LT'.lista`                                        |
| `LT' → TU LT'1`                        | `LT'.lista = [TU] + LT'1.lista`                                      |
| `LT' → ε`                              | `LT'.lista = []`                                                     |
| `B → batalha POK1 contra POK2 { LT }`  | `B = {pok1: POK1, pok2: POK2, turnos: LT.lista}`                     |
| `TP → fogo`                            | `TP.valor = fogo`                                                    |
| `TP → agua`                            | `TP.valor = agua`                                                    |
| `TP → eletrico`                        | `TP.valor = eletrico`                                                |

## Comunicação entre os ramos

A produção inicial é:

```text
S → D B
```

O ramo `D` produz a fórmula:

```text
D.formula = (ataque + poder - defesa) * efetividade
```

O ramo `B` produz a batalha:

```text
B = Pokémon + turnos + ações
```

O símbolo inicial reúne os dois resultados:

```text
S.resultado = executar_batalha(D.formula, B)
```

## Regra de efetividade

```text
efetividade(eletrico, agua) = 2.0
efetividade(agua, eletrico) = 1.0
efetividade(outros casos) = 1.0
```

## Regra de dano

```text
dano = (ataque + poder - defesa) * efetividade
```

O dano não pode ser negativo:

```text
dano = max(0, dano)
```

## Código intermediário

Para uma ação do atacante contra o defensor:

```text
t1 = atacante.ataque + golpe.poder
t2 = t1 - defensor.defesa
t3 = t2 * efetividade(golpe.tipo, defensor.tipo)
dano = max(0, t3)
```

## Atualização das vidas

As duas ações de um turno são calculadas antes da atualização das vidas:

```text
pok1.vida = max(0, pok1.vida - dano_pok2)
pok2.vida = max(0, pok2.vida - dano_pok1)
```

A vida resultante de um turno é utilizada no turno seguinte.

---

# Árvore de derivação anotada

Para a ação de Pikachu contra Squirtle:

```text
S
├── D
│   └── formula = (ataque + poder - defesa) * efetividade
│
└── B
    ├── POK1
    │   ├── nome = Pikachu
    │   ├── tipo = eletrico
    │   ├── vida = 200
    │   ├── ataque = 80
    │   └── defesa = 50
    │
    ├── POK2
    │   ├── nome = Squirtle
    │   ├── tipo = agua
    │   ├── vida = 220
    │   ├── ataque = 70
    │   └── defesa = 70
    │
    └── TU
        ├── A1
        │   ├── atacante.ataque = 80
        │   ├── golpe.poder = 60
        │   ├── defensor.defesa = 70
        │   ├── efetividade = 2.0
        │   ├── t1 = 80 + 60 = 140
        │   ├── t2 = 140 - 70 = 70
        │   └── dano1 = 70 * 2.0 = 140
        │
        ├── A2
        │   ├── atacante.ataque = 70
        │   ├── golpe.poder = 50
        │   ├── defensor.defesa = 50
        │   ├── efetividade = 1.0
        │   ├── t3 = 70 + 50 = 120
        │   ├── t4 = 120 - 50 = 70
        │   └── dano2 = 70 * 1.0 = 70
        │
        ├── Pikachu.vida = 200 - 70 = 130
        └── Squirtle.vida = 220 - 140 = 80
```

---

# Resultado dos turnos

## Primeiro turno

```text
dano de Pikachu = 140
dano de Squirtle = 70

Pikachu.vida = 130
Squirtle.vida = 80
```

## Segundo turno

```text
Pikachu.vida = max(0, 130 - 70) = 60
Squirtle.vida = max(0, 80 - 140) = 0
```

## Vencedor

```text
Pikachu.vida = 60
Squirtle.vida = 0

vencedor = Pikachu
```

---

# Execução

Instalação:

```bash
pip install ply
```

Execução:

```bash
python main.py exemplo.poke
```

Saída esperada:

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

Uma ferramenta de inteligência artificial foi utilizada para auxiliar na organização da gramática, simplificação da linguagem, elaboração das árvores e revisão da documentação.

Prompts principais:

<img width="761" height="668" alt="image" src="https://github.com/user-attachments/assets/9821918b-acb1-45ae-8371-fb793e9a55a3" />

As respostas foram revisadas e adaptadas por nós para definir a linguagem que gostaríamos.

Inclusive, inicialmente, o ChatGPT focou em realizar todos os cálculos de forma semântica tornando a gramática muito simples. 

<img width="765" height="911" alt="image" src="https://github.com/user-attachments/assets/d1252421-f883-48bc-a7c4-8f56cf961a72" />

E esse foi o principal impasse, manter a linguagem complexa o suficiente, mas ainda limitada para que possamos abrir as árvores de derivação manualmente.

<img width="730" height="336" alt="image" src="https://github.com/user-attachments/assets/fe3d34b6-1e73-417f-8bb7-dcd507cff11e" />
