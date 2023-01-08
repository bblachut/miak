from enum import Enum


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
    ERROR = 24
    BOOLEAN = 25
    ID = 26
    NUMBER = 27
    SEMICOLON = 28
    FUNCTION = 29
    STRING = 31  # used only to make code smoother, not checked by parser


keywords = {'if': Token.IF_TOKEN, 'or': Token.OR_TOKEN, 'for': Token.FOR_TOKEN, 'not': Token.NOT_TOKEN,
            'else': Token.ELSE_TOKEN, 'while': Token.WHILE_TOKEN, 'return': Token.RETURN_TOKEN, 'continue': Token.SKIP,
            'break': Token.SKIP, 'and': Token.AND_TOKEN, 'True': Token.BOOLEAN, 'False': Token.BOOLEAN,
            'function': Token.FUNCTION}
