# thou-lang

Custom programming language based on the classic english grammar. Created for Insper's 2021.1 Computer Logic class.

## O que é

A linguagem Thou é uma linguagem de programação baseada na gramática do inglês clássico e inspirada pela linguagem C. A sintática da linguagem tenta ser maix próxima da fala do que apenas de comandos imperativos.

## EBNF

```
MAIN = FUNCTION ;

FUNCTION = TYPE, IDENTIFIER, "(", [{PARAM}], ")", BLOCK ;
PARAM = TYPE, IDENTIFIER ;
RETURN = "return_to_the_one_whom_bid_thou", (EXPRESSION | COMPARISON), ";" ;

FUNCTION_CALL = IDENTIFIER, "(", (EXPRESSION | COMPARISON), {",", (EXPRESSION | COMPARISON)}, ")", ";" ;

BLOCK = "{", STATEMENT, { STATEMENT }, "}" ;
STATEMENT = ( λ | ASSIGNMENT | PRINT | IF | WHILE | RETURN | FUNCTION_CALL) ;

PRINT = "thou_shalt_utter", "(", (EXPRESSION | COMPARISON), ")", ";" ;

IF = "shouldst_this_be_true", "(", COMPARISSON, ")", BLOCK, { ELSE };
ELSE = "if_naught", BLOCK ;

WHILE = "thou_shall_repeat_if", "(", COMPARISSON, ")", BLOCK ;

TYPE = "maths" | "is*it_true" | "kayne_west_phrase" ;
IDENTIFIER = LETTER, { LETTER | DIGIT | "*" } ;

ASSIGNMENT = TYPE, IDENTIFIER, "=", (COMPARISON | EXPRESSION | NUMBER | STRING | BOOLEAN), ";" ;
ASSIGNMENT = TYPE, IDENTIFIER, ";" ;
COMPARISON = EXPRESSION, (">", "<", "==", ">=", "<=", "!=", "&&", "||"), EXPRESSION ;

EXPRESSION = TERM, { ("+" | "-"), TERM } ;
TERM = FACTOR, { ("\*" | "/"), FACTOR } ;
FACTOR = (("+" | "-"), FACTOR) | NUMBER | "(", EXPRESSION, ")" | IDENTIFIER ;

BOOLEAN = "it_is_sooth" | "it_is_false" ;

NUMBER = DIGIT, { DIGIT } ;
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;

STRING = '"', LETTER, { LETTER }, '"' ;
LETTER = ( a | ... | z | A | ... | Z ) ;
```

## Exemplos

### Variáveis

A linguagem Thou conta apenas com 3 tipos de variáveis. Esses tipos são:

1. `maths`, que é igual ao tipo `int` da linguagem C.
2. `is_it_true`, que é igual ao tipo `bool` da linguagem C.
3. `kayne_west_phrase`, que é igual ao tipo `char[]` da linguagem C.

```
maths x = 1;
x = 3;
is_it_true y = it_is_sooth;
y = it_is_false;
kanye_west_phrase a = "abc";
a = "abcd";
```

### Funções

Toda função na linguagem Thou tem que retornar alguma coisa. O retorno pode ser de qualquer tipo. Além disso, é obrigatório que todas as funções tenham o retorno dentro de seus comandos.

```
maths main() {
    maths x = 0;
    return_to_the_one_whom_bid_thou 0;
}
```

### If/Else

```
shouldst_this_be_true (x == 1)
{
    return_to_the_one_whom_bid_thou 1;
} if_naught
{
    return_to_the_one_whom_bid_thou x * factorial(x - 1);
}
```

### While

```
maths x = 0;
thou_shall_repeat_if (x < 10)
{
    thou_shalt_utter(x);
    x = x + 1;
}
```

### Print

```
maths x = 0;
thou_shalt_utter(x);
```

### Function Call

```
maths sum(maths a, maths b)
{
    return_to_the_one_whom_bid_thou a + b;
}

maths main()
{
    maths x = sum(25, 26);
    thou_shalt_utter(x);
}
```

### Comparações

```
maths x = 1;
is_it_true y = x == 1;
y = x != 1;
y = x > 1;
y = x >= 1;
y = x < 1;
y = x <= 1;
y = x && 1;
y = x || 1;
```

## Exemplos de programas

[in02.thou](./tests/in02.thou)

```
maths factorial(maths x)
{
    shouldst_this_be_true (x == 1)
    {
        return_to_the_one_whom_bid_thou 1;
    } if_naught
    {
        return_to_the_one_whom_bid_thou x * factorial(x - 1);
    }
}

maths main()
{
    thou_shalt_utter(factorial(5));

    return_to_the_one_whom_bid_thou 0;
}
```

[in03.thou](./tests/in03.thou)

```
maths random(maths x)
{
    thou_shall_repeat_if (x < 10)
    {
        x = x + 1;
        thou_shalt_utter(x);
    }

    return_to_the_one_whom_bid_thou 99;
}

maths main()
{
    thou_shalt_utter(random(4));

    return_to_the_one_whom_bid_thou 0;
}
```

## Ferraments e implementação

A implementação da linguagem foi feita usando o [Sly][sly] como lexer e parser e o [LLVMlite][llvmlite] como compilador.

### Lexer

A análise léxica e a tokenização da linguagem são feitas pela classe `ThouLexer`, no arquivo [tokenizer.py](./src/compiler/tokenizer.py). Todos o marcadores da linaguagem são definidos usando Regex Strings.

### Parser

O módulo [Sly][sly] permite que o parsing da linguagem seja feito de maneira muito parecida à EBNF. A partir da definicão de regras de produção (como as da EBNF) podemos fazer o parse rapidamente da linguagem. Apesar da simplicidade do parsing, a criação da AST ainda é feita manualmente. Desse modo, a classe `ThouParser`, no arquivo [parser.py](./src/compiler/parser.py), fica responsável pelo parsing e a construção da AST.

### Geração de código

O módulo [LLVMlite][llvmlite] traz uma abstração totalmente em Python do LLVM, facilitando a criação de linguagens imensamente. Ele permite que todas as estruturas da linguagem sejam definidas em cada nó e inteiramente em Python.

Sendo assim, a classe `CodeGen`, no arquivo [codegen.py](./src/compiler/codegen.py), é responsável por gerar todo os objetos necessários para a utilização do [LLVMlite][llvmlite]. É aqui que é definida a função principal `main` e seu tipos, tanto de retorno como os argumentos.

### Nós

Os nós da AST se encontram na pasta [./src/models/nodes](./src/models/nodes/). Cada nó é responsável pela criação de suas instruções em relação ao [LLVMlite][llvmlite].

### Logger

Foi utilizado um logger para facilitar o debugging durante a criação da linguagem. Ele funciona printando as mensagens no terminal, caso a flag de debug esteja ativada. A quantidade de mensagens de log pode ser controlada com o nível de verbosity.

## Utilização

### Instalação

Como a linguagem depende dos módulos [Sly][sly] e [LLVMlite][llvmlite], precisamos instalar eles antes de começar a usar o compilador.

Para controlar as dependências do projeto foi usado o [Pipenv][pipenv]. Ele permite a criação e compartilhamento de ambientes virtuais de Python facilmente. Existe um arquivo [Pipfile](./Pipfile) que lista todas as dependências do compilador, tanto as de utilização quantos as de desenvolvimento, para usa-lo basta executar o seguinte comando:

```bash
pipenv install
```

### Utilização

Para executar o compilador podemos usar do [Makefile][makefile], que contém todos os comandos necessário para compilar e gerar um executável. Ele necessita de apenas um argumento `IN`, que diz qual o arquivo de entrada do programa.

1. Para rodar todas as etapas, basta usar:

```
make IN="./tests/in00.thou"
```

2. Para apenas gerar o arquivo LLVM resultante basta:

```
make gen_ll IN="./tests/in00.thou"
```

3. Para apenas gerar o arquivo LLVM resultante juntamente com todos o logs basta:

```
make gen_ll_debug IN="./tests/in00.thou"
```

**Obs:** Todos os arquivos de saída do compilador ficam na pasta `out`, incluindo os logs gerados, o arquivo LLVM resultante, e o executável gerado.

[sly]: https://github.com/dabeaz/sly
[llvmlite]: https://github.com/numba/llvmlite
[pipenv]: https://github.com/pypa/pipenv
[makefile]: ./Makefile
