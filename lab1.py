import re
import math

def tokenize(expression):
    pattern = r'\d+(?:\.\d*)?|\.\d+|[A-Za-z_]\w*|[+\-*/()]'
    tokens = re.findall(pattern, expression)
    # Удаляем допустимые токены и пробелы.
    if re.sub(pattern, '', expression).strip():
        raise ValueError("Недопустимые символы в выражении")
    return tokens

def calculate(expression):
    tokens = tokenize(expression)
    position = 0
    def parse_expression():
        nonlocal position
        result = parse_term()
        while position < len(tokens) and tokens[position] in ('+', '-'):
            operator = tokens[position]
            position += 1
            right = parse_term()
            if operator == '+':
                result = result + right
            else:
                result = result - right
        return result
    def parse_term():
        nonlocal position
        result = parse_factor()
        while position < len(tokens) and tokens[position] in ('*', '/'):
            operator = tokens[position]
            position += 1
            right = parse_factor()
            if operator == '*':
                result = result * right
            else:
                if right == 0:
                    raise ZeroDivisionError("Деление на ноль")
                result = result / right
        return result
    def parse_factor():
        nonlocal position
        if position >= len(tokens):
            raise ValueError("Неожиданный конец выражения")
        token = tokens[position]
        # Унарные знаки
        if token == '+':
            position += 1
            return parse_factor()
        if token == '-':
            position += 1
            return -parse_factor()
        # Функция cos(x), аргумент задаётся в радианах
        if token == 'cos':
            position += 1
            if position >= len(tokens) or tokens[position] != '(':
                raise ValueError("После cos ожидается '('")
            position += 1
            argument = parse_and()
            if position >= len(tokens) or tokens[position] != ')':
                raise ValueError("Не хватает ')' после cos")
            position += 1
            return math.cos(argument)
        # Выражение в скобках
        if token == '(':
            position += 1
            result = parse_and()
            if position >= len(tokens) or tokens[position] != ')':
                raise ValueError("Не хватает закрывающей скобки")
            position += 1
            return result
        # Числовой токен
        if re.fullmatch(r'\d+(?:\.\d*)?|\.\d+', token):
            position += 1
            return float(token)
        raise ValueError(f"Неожиданный токен: {token}")
    # Логическое И
    def parse_and():
        nonlocal position
        result = parse_expression()
        while position < len(tokens) and tokens[position] == 'and':
            position += 1
            right = parse_expression()
            result = 1.0 if (result != 0 and right != 0) else 0.0
        return result
    if not tokens:
        raise ValueError("Пустое выражение")
    result = parse_and()
    if position != len(tokens):
        raise ValueError(f"Лишний токен: {tokens[position]}")
    return result
if __name__ == "__main__":
    expression = input("Введите выражение: ")
    try:
        print("Результат:", calculate(expression))
    except (ValueError, ZeroDivisionError) as error:
        print("Ошибка:", error)
    except RecursionError:
        print("Ошибка: слишком глубокая вложенность выражения")
