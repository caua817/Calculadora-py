# Calculadora em Python

Calculadora de linha de comando que aceita expressões completas, guarda histórico e permite reutilizar o último resultado.

## Funcionalidades

- Operadores: `+`, `-`, `*`, `/`, `//`, `%`, `**` e parênteses
- Funções: `sqrt`, `abs`, `round`, `sin`, `cos`, `tan`, `log` (base 10) e `ln`
- Constantes: `pi` e `e`
- `ans` para usar o resultado anterior
- Histórico dos cálculos
- Tratamento de erros, como divisão por zero e expressão inválida

## Como usar

Com o Python 3 instalado, execute no terminal:

```
python Calculadora.py
```

Digite uma expressão e pressione Enter. Comandos disponíveis: `historico`, `limpar`, `ajuda` e `sair`.

## Exemplo

```
> 2 + 3 * (4 - 1)
= 11

> sqrt(144) / 3
= 4

> ans * 5
= 20
```

## Como funciona

As expressões são avaliadas com o módulo `ast` do Python, e não com `eval`. Assim, só operações matemáticas permitidas são executadas, o que torna a calculadora mais segura.
