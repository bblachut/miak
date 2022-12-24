from typing import Tuple
from colorama import Fore
from enum import Enum


class Token(Enum):
    PLUS = 1
    MINUS = 2
    TIMES = 3
    DIV = 4
    LPAREN = 5
    RPAREN = 6
    KEYWORD = 7
    ID = 8
    NUMBER = 9
    ERROR = 10
    BLANK = 11
    EQUALS = 12
    COLON = 13


keywords = {'if', 'else', 'elif', 'return', 'def', 'for', 'while'}
token_colors = {Token.ERROR: Fore.RED, Token.KEYWORD: Fore.GREEN, Token.ID: Fore.YELLOW, Token.NUMBER: Fore.CYAN}


def scanner(text: str, i: int) -> Tuple[int, Token, str]:
    if text[i] == '+':
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
            if identifier in keywords:
                return i, Token.KEYWORD, identifier
            i += 1
        return i-1, Token.ID, identifier
    if text[i].isdigit():
        number = ''
        while i < len(text) and text[i].isdigit():
            number += text[i]
            i += 1
        if i < len(text) and text[i].isalpha():
            return i, Token.ERROR, number+text[i]
        return i-1, Token.NUMBER, number
    if text[i].isspace():
        return i, Token.BLANK, text[i]
    return i, Token.ERROR, text[i]


def scan(text: str) -> None:
    i = 0
    while i < len(text):
        i, token, communicat = scanner(text, i)
        color = token_colors.get(token)
        if color is not None:
            print(color + communicat + Fore.RESET, end='')
        else:
            print(communicat + Fore.RESET, end='')
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
