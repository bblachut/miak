from enum import Enum
from typing import Tuple


class Token(Enum):
    ASSIGN = 1
    IF_TOKEN = 2
    ELSE_TOKEN = 3
    WHILE_TOKEN = 4
    FOR_TOKEN = 5
    RETURN_TOKEN = 6
    AND_TOKEN = 7
    OR_TOKEN = 8
    SKIP = 9
    NOT_TOKEN = 10
    CURLY_BRACKET_BEGIN = 11
    CURLY_BRACKET_END = 12
    ROUND_BRACKET_BEGIN = 13
    ROUND_BRACKET_END = 14
    SQUARE_BRACKET_BEGIN = 15
    SQUARE_BRACKET_END = 16
    QUOTATION_MARK = 17
    COMPARISON_OPERATORS = 18
    MATH_OPERATORS = 19
    COMMA = 20
    BETWEEN = 21
    WHITESPACE = 22
    NEW_LINE = 23
    ERROR = 24
    BOOLEAN = 25
    ID = 26
    NUMBER = 27


keywords = {'if': Token.IF_TOKEN, 'or': Token.OR_TOKEN, 'for': Token.FOR_TOKEN, 'not': Token.NOT_TOKEN,
            'else': Token.ELSE_TOKEN, 'while': Token.WHILE_TOKEN, 'return': Token.RETURN_TOKEN, 'continue': Token.SKIP,
            'break': Token.SKIP, 'and': Token.AND_TOKEN, 'True': Token.BOOLEAN, 'False': Token.BOOLEAN}


def scanner(text: str, i: int) -> Tuple[int, Token, str]:
    if text[i] == '<':
        if text[i + 1] == '=':
            return i+1, Token.COMPARISON_OPERATORS, '<='
        if text[i+1] == '-':
            return i+1, Token.ASSIGN, '<-'
        return i, Token.PLUS, text[i]

    if text[i] == '-':
        return i, Token.PLUS, text[i]
    if text[i] == '*':
        return i, Token.PLUS, text[i]
    if text[i] == '/':
        return i, Token.PLUS, text[i]
    if text[i] == '(':
        return i, Token.PLUS, text[i]
    if text[i] == ')':
        return i, Token.PLUS, text[i]
    if text[i] == '=':
        return i, Token.EQUALS, text[i]
    if text[i] == ':':
        return i, Token.COLON, text[i]
    if text[i].isalpha():
        identifier = ''
        while i < len(text) and (text[i].isdigit() or text[i].isalpha()):
            identifier += text[i]
            if identifier in keywords.keys():
                return i, keywords[identifier], identifier
            i += 1
        return i - 1, Token.ID, identifier
    if text[i].isdigit():
        number = ''
        while i < len(text) and text[i].isdigit():
            number += text[i]
            i += 1
        if i < len(text) and text[i].isalpha():
            return i, Token.ERROR, number + text[i]
        return i - 1, Token.NUMBER, number
    if text[i].isspace():
        return i, Token.BLANK, text[i]
    return i, Token.ERROR, text[i]


def scan(text: str) -> None:
    i = 0
    while i < len(text):
        i, token, communicat = scanner(text, i)
        print(communicat, end='')
        i += 1


if __name__ == '__main__':
    scan('''def scan(text: str) -> None:
    i = 0
    while i < len(text):
        i, token, communicat = scanner(text, i)
        color = token_colors.get(token)
        if color is not None:
            print(color + communicat + Fore.RESET, end='')
        else:
            print(communicat + Fore.RESET, end='')
        i += 1''')
