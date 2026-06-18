# PokeLang

Linguagem de domínio específico desenvolvida para a disciplina de **Compiladores** utilizando **Python** e **PLY**.

A PokeLang permite definir uma fórmula de dano e executar uma batalha simplificada entre dois Pokémon com um ou mais turnos.

## Autores

* Caio Passos Torkst Ferreira
* Daniel Salvador Motta

---

# Estrutura do projeto

* `lexer.py`: análise léxica;
* `parser.py`: análise sintática e semântica;
* `main.py`: execução do programa;
* `exemplo.poke`: programa de exemplo;
* `requirements.txt`: dependências.

---

# 1. Análise léxica

A análise léxica é realizada pelo módulo `ply.lex`. Ela transforma o código-fonte em uma sequência de tokens.

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

## Estrutura do Pokémon

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

## Estrutura do golpe

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

A expressão possui três níveis:

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

As operações do mesmo nível são avaliadas da esquerda para a direita:

```text
ataque - poder - defesa
```

é interpretado como:

```text
(ataque - poder) - defesa
```

## Repetição dos turnos

```text
LT → TU LT'
LT' → TU LT' | ε
```

A produção `LT → TU LT'` garante pelo menos um turno.

Cada aplicação de:

```text
LT' → TU LT'
```

adiciona um novo turno.

A produção:

```text
LT' → ε
```

encerra a lista.

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

O arquivo `exemplo.poke` utiliza dois turnos para demonstrar a repetição durante a execução.

```text
dano = (ataque + poder - defesa) * efetividade;

batalha Pikachu(eletrico, 200, 80, 50) contra Squirtle(agua, 220, 70, 70) {
    turno { Pikachu usa choque(eletrico, 60); Squirtle usa jato_agua(agua, 50); }
    turno { Pikachu usa choque(eletrico, 60); Squirtle usa jato_agua(agua, 50); }
}
```

## Sentença utilizada na árvore de derivação

Para evitar uma árvore excessivamente grande, a árvore utiliza uma sentença aceita pela linguagem contendo apenas um turno.

```text
dano = (ataque + poder - defesa) * efetividade;

batalha Pikachu(eletrico, 200, 80, 50) contra Squirtle(agua, 220, 70, 70) {
    turno { Pikachu usa choque(eletrico, 60); Squirtle usa jato_agua(agua, 50); }
}
```

Nesse caso, a lista deriva como:

```text
LT → TU LT' → TU ε
```

## Árvore de derivação

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
│   │   │   │   │   ├── ataque
│   │   │   │   │   ├── +
│   │   │   │   │   ├── poder
│   │   │   │   │   ├── -
│   │   │   │   │   └── defesa
│   │   │   │   └── )
│   │   │   ├── *
│   │   │   └── efetividade
│   │   └── ε
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
    │   │   │   ├── G
    │   │   │   │   ├── id → choque
    │   │   │   │   ├── TP → eletrico
    │   │   │   │   └── num → 60
    │   │   │   └── ;
    │   │   ├── A
    │   │   │   ├── id → Squirtle
    │   │   │   ├── usa
    │   │   │   ├── G
    │   │   │   │   ├── id → jato_agua
    │   │   │   │   ├── TP → agua
    │   │   │   │   └── num → 50
    │   │   │   └── ;
    │   │   └── }
    │   └── LT'
    │       └── ε
    └── }
```

A árvore possui dois ramos principais:

```text
S
├── D → fórmula de dano
└── B → batalha
```

---

# 3. Análise semântica

A análise semântica atribui significado às estruturas reconhecidas pelo analisador sintático.

Ela é responsável por armazenar a fórmula, calcular o dano, atualizar as vidas e determinar o vencedor.

## Tabela de produções e ações semânticas

| Produção                                        | Ação semântica                                           |
| ----------------------------------------------- | -------------------------------------------------------- |
| `S → D B`                                       | Passa a fórmula produzida por `D` para a execução de `B` |
| `D → dano = E ;`                                | Armazena a árvore da expressão de dano                   |
| `E → TR E'`                                     | Constrói somas e subtrações                              |
| `E' → + TR E'`                                  | Adiciona uma soma                                        |
| `E' → - TR E'`                                  | Adiciona uma subtração                                   |
| `E' → ε`                                        | Finaliza a expressão                                     |
| `TR → F TR'`                                    | Constrói multiplicações e divisões                       |
| `TR' → * F TR'`                                 | Adiciona uma multiplicação                               |
| `TR' → / F TR'`                                 | Adiciona uma divisão                                     |
| `TR' → ε`                                       | Finaliza o termo                                         |
| `F → num`                                       | Produz um número                                         |
| `F → AT`                                        | Produz um atributo                                       |
| `F → ( E )`                                     | Propaga a expressão interna                              |
| `AT → ataque \| defesa \| poder \| efetividade` | Produz o atributo correspondente                         |
| `B → batalha POK1 contra POK2 { LT }`           | Inicializa os participantes e executa os turnos          |
| `POK → id ( TP, num1, num2, num3 )`             | Produz nome, tipo, vida, ataque e defesa                 |
| `LT → TU LT'`                                   | Cria a lista de turnos                                   |
| `LT' → TU LT'`                                  | Adiciona um turno                                        |
| `LT' → ε`                                       | Finaliza a lista                                         |
| `TU → turno { A1 A2 }`                          | Calcula os danos e atualiza as vidas                     |
| `A → id usa G ;`                                | Produz o usuário e o golpe                               |
| `G → id ( TP, num )`                            | Produz nome, tipo e poder                                |
| `TP → fogo \| agua \| eletrico`                 | Produz o tipo correspondente                             |

## Comunicação entre os ramos

Na produção:

```text
S → D B
```

o ramo `D` produz a árvore da fórmula:

```text
D.formula = (ataque + poder - defesa) * efetividade
```

O ramo `B` produz a batalha:

```text
B = participantes + turnos + ações
```

A ação semântica do nó `S` reúne os dois resultados:

```text
S.resultado = executar_batalha(D.formula, B)
```

Portanto, a fórmula não passa diretamente de um ramo para o outro. O nó pai `S` recebe os resultados de `D` e `B` e envia a fórmula para a execução da batalha.

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

## Árvore anotada da fórmula

Para a ação:

```text
Pikachu usa choque(eletrico, 60);
```

o contexto é:

```text
ataque = 80
poder = 60
defesa = 70
efetividade = 2.0
```

A árvore anotada é:

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
dano = (80 + 60 - 70) * 2.0 = 140
```

## Atualização das vidas

As duas ações são calculadas com os valores existentes no início do turno.

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

```text
dano_Pikachu = (80 + 60 - 70) * 2.0 = 140
dano_Squirtle = (70 + 50 - 50) * 1.0 = 70
```

```text
Pikachu.vida = 200 - 70 = 130
Squirtle.vida = 220 - 140 = 80
```

## Segundo turno

```text
Pikachu.vida = max(0, 130 - 70) = 60
Squirtle.vida = max(0, 80 - 140) = 0
```

## Árvore anotada da execução

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
        │   ├── A1 = { usuario = Pikachu, golpe = choque, dano = 140 }
        │   ├── A2 = { usuario = Squirtle, golpe = jato_agua, dano = 70 }
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

Caso todos os turnos terminem sem um Pokémon chegar a zero, vence aquele que possuir mais vida restante.

---

# Execução

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

