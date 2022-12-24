from typing import Tuple, List

from resources import Token, keywords


class Parser:
    def __init__(self, pseudocode: str) -> None:
        self.tokens = self._parse(pseudocode)

    @staticmethod
    def _scanner(text: str, i: int) -> Tuple[int, Token, str]:
        if len(text) > i + 1 and text[i: i + 2] == '<-':
            return i + 1, Token.ASSIGN, '<-'
        if text[i] == '{':
            return i, Token.CURLY_BRACKET_BEGIN, '{'
        if text[i] == '}':
            return i, Token.CURLY_BRACKET_END, '}'
        if text[i] == '(':
            return i, Token.ROUND_BRACKET_BEGIN, '('
        if text[i] == ')':
            return i, Token.ROUND_BRACKET_END, ')'
        if text[i] == '[':
            return i, Token.SQUARE_BRACKET_BEGIN, '['
        if text[i] == ']':
            return i, Token.SQUARE_BRACKET_END, ']'
        if text[i] == '"':
            return i, Token.QUOTATION_MARK, '"'
        if text[i] == ',':
            return i, Token.COMMA, ','
        if text[i] == '.':
            if len(text) > i + 2 and text[i + 1] == '.' and text[i + 2] == '.':
                return i + 2, Token.BETWEEN, '...'
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
        if text[i] in ('+', '-', '*', '/', '%', '^'):
            return i, Token.MATH_OPERATORS, text[i]
        if text[i] in ('<', '>', '='):
            if len(text) > i + 1 and text[i + 1] == '=' and text[i] != '=':
                return i + 1, Token.COMPARISON_OPERATORS, text[i] + '='
            return i, Token.COMPARISON_OPERATORS, text[i]
        if text[i] == '\n':
            return i, Token.NEW_LINE, text[i]
        if text[i].isspace():
            return i, Token.WHITESPACE, text[i]
        return i, Token.ERROR, text[i]

    def _parse(self, text: str) -> List[Tuple[str, Token]]:
        tokens = []
        i = 0
        while i < len(text):
            i, token, communicat = self._scanner(text, i)
            tokens.append((communicat, token))
            i += 1
        return tokens

    def __iter__(self):
        return self

    def __next__(self):
        return self.tokens.pop(0)



if __name__ == '__main__':
    pseudocode = '''x <- 1
if x = 1{
    y<-2
} else {
    y<-3
}

my_print(x){
    for i <- 1…x{
        print i
    }
    return true
}

my_print(5)

arr = [1,2,3]
z <- arr[2]
'''
    parser = Parser(pseudocode)
    while True:
        print(next(parser))
