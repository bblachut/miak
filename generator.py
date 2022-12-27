from parser import Parser
from resources import Token
from typing import List,Tuple


class Generator:
    def __init__(self, pseudocode: str):
        self.parser = Parser(pseudocode)
        self.code = ""
        self.saved_token = None
        self.indent_ctr = 0

    def next_token(self) -> Tuple[str, Token]:
        if self.saved_token is not None:
            token = self.saved_token
            self.saved_token = None
            return token
        token = next(self.parser, None)
        if token is None:
            raise EOFError
        return token

    def _check_if_right_token(self, right_token: List[Token]) -> (Token, str):
        communicat, token = self.next_token()
        if token not in right_token:
            self.saved_token = (communicat, token)
            print("Segmentation fault")
            exit()
        return token, communicat


    def _add_to_code(self, token: Token, communicat: str):

        if token == Token.ASSIGN:
            self.code += "="

        elif token == Token.COMPARISON_OPERATORS and communicat == "=":
            self.code += "=="

        elif token == Token.CURLY_BRACKET_BEGIN:
            self.code += ":"
            self.indent_ctr += 1

        elif token == Token.CURLY_BRACKET_END:
            self.indent_ctr -= 1

        elif token == Token.SEMICOLON:
            self.code += "\n"
            self.code += " "*4*self.indent_ctr

        else:
            self.code += communicat



    def _check_for_statement(self):
        try:
            id1 = self._check_if_right_token([Token.ID])
            ass1 = self._check_if_right_token([Token.ASSIGN])
            id2 = self._check_if_right_token([Token.ID, Token.NUMBER])
            btw = self._check_if_right_token([Token.BETWEEN])
            id3 = self._check_if_right_token([Token.ID, Token.NUMBER])

            self.code += f"for {id1[1]} in range({id2[1]},{id3[1]}):"

            self._add_to_code(*self._check_if_right_token([Token.CURLY_BRACKET_BEGIN]))

            res = self._check_statement()
            while (res):
                res = self._check_statement()

            self._add_to_code(*self._check_if_right_token([Token.CURLY_BRACKET_END]))
        except EOFError:
            exit()

    def generate(self) -> str:

        while (1):
            communicat, token = self.next_token()
            if token == Token.FOR_TOKEN:
                self._check_for_statement()
