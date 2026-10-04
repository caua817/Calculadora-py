"""Calculadora de linha de comando em Python.

Aceita expressões completas, como `2 + 3 * (4 - 1)` ou `sqrt(16) + 2 ** 3`,
guarda histórico e permite reutilizar o último resultado com `ans`.

A avaliação usa o módulo `ast` em vez de `eval`, então só operações
matemáticas permitidas são executadas.
"""

import ast
import math
import operator

OPERADORES_BINARIOS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

OPERADORES_UNARIOS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

FUNCOES = {
    "sqrt": math.sqrt,
    "abs": abs,
    "round": round,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log10,
    "ln": math.log,
}

CONSTANTES = {
    "pi": math.pi,
    "e": math.e,
}

LIMITE_EXPOENTE = 1000

AJUDA = """
Operadores:  +  -  *  /  //  %  **  ( )
Funções:     sqrt  abs  round  sin  cos  tan  log (base 10)  ln
Constantes:  pi  e
Resultado anterior: ans

Comandos:
  historico   mostra os cálculos feitos
  limpar      apaga o histórico
  ajuda       mostra esta mensagem
  sair        encerra o programa

Exemplos:
  2 + 3 * (4 - 1)
  sqrt(144) / 3
  ans * 2
"""


class ErroDeCalculo(Exception):
    """Erro de sintaxe ou de operação na expressão."""


def _avaliar_no(no, ans):
    if isinstance(no, ast.Expression):
        return _avaliar_no(no.body, ans)

    if isinstance(no, ast.Constant):
        if isinstance(no.value, (int, float)) and not isinstance(no.value, bool):
            return no.value
        raise ErroDeCalculo("Só números são permitidos.")

    if isinstance(no, ast.Name):
        if no.id == "ans":
            if ans is None:
                raise ErroDeCalculo("Ainda não há resultado anterior.")
            return ans
        if no.id in CONSTANTES:
            return CONSTANTES[no.id]
        raise ErroDeCalculo(f"Nome desconhecido: {no.id}")

    if isinstance(no, ast.BinOp) and type(no.op) in OPERADORES_BINARIOS:
        esquerda = _avaliar_no(no.left, ans)
        direita = _avaliar_no(no.right, ans)
        if isinstance(no.op, ast.Pow) and abs(direita) > LIMITE_EXPOENTE:
            raise ErroDeCalculo("Expoente muito grande.")
        return OPERADORES_BINARIOS[type(no.op)](esquerda, direita)

    if isinstance(no, ast.UnaryOp) and type(no.op) in OPERADORES_UNARIOS:
        return OPERADORES_UNARIOS[type(no.op)](_avaliar_no(no.operand, ans))

    if isinstance(no, ast.Call) and isinstance(no.func, ast.Name):
        if no.func.id not in FUNCOES or no.keywords:
            raise ErroDeCalculo(f"Função desconhecida: {no.func.id}")
        argumentos = [_avaliar_no(arg, ans) for arg in no.args]
        return FUNCOES[no.func.id](*argumentos)

    raise ErroDeCalculo("Expressão não permitida.")


def avaliar(expressao, ans=None):
    """Calcula o valor de uma expressão matemática em texto."""
    try:
        arvore = ast.parse(expressao.strip(), mode="eval")
    except SyntaxError:
        raise ErroDeCalculo("Expressão inválida.") from None

    try:
        return _avaliar_no(arvore, ans)
    except ZeroDivisionError:
        raise ErroDeCalculo("Divisão por zero.") from None
    except (ValueError, TypeError):
        raise ErroDeCalculo("Operação inválida para esses valores.") from None
    except OverflowError:
        raise ErroDeCalculo("Resultado grande demais.") from None


def formatar(valor):
    """Mostra inteiros sem casas decimais e limita a precisão dos decimais."""
    if isinstance(valor, float):
        if valor.is_integer():
            return str(int(valor))
        return f"{valor:.10g}"
    return str(valor)


def main():
    print("=== Calculadora ===")
    print("Digite uma expressão, 'ajuda' para ver os comandos ou 'sair' para encerrar.")

    historico = []
    ans = None

    while True:
        try:
            entrada = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAté mais!")
            break

        if not entrada:
            continue

        comando = entrada.lower()

        if comando in ("sair", "exit", "quit"):
            print("Até mais!")
            break
        if comando == "ajuda":
            print(AJUDA)
            continue
        if comando == "historico":
            if not historico:
                print("Nenhum cálculo ainda.")
            for expressao, resultado in historico:
                print(f"  {expressao} = {resultado}")
            continue
        if comando == "limpar":
            historico.clear()
            print("Histórico apagado.")
            continue

        try:
            resultado = avaliar(entrada, ans)
        except ErroDeCalculo as erro:
            print(f"Erro: {erro}")
            continue

        ans = resultado
        texto = formatar(resultado)
        historico.append((entrada, texto))
        print(f"= {texto}")


if __name__ == "__main__":
    main()
