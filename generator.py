from typing import List, Tuple, Union

from parser import Parser
from resources import Token


class Generator:
    def __init__(self, pseudocode: str):
        self.parser = Parser(pseudocode)
        self.code = ""
        self.saved_token = None
        self.indent_ctr = 0

    def next_token(self) -> Tuple[Token, str]:
        if self.saved_token is not None:
            token = self.saved_token
            self.saved_token = None
            return token
        token = next(self.parser, None)
        if token is None:
            raise EOFError
        return token

    def _check_if_right_token(self, right_tokens: List[Token]) -> Tuple[Token, str]:
        token, communicat = self.next_token()
        if token not in right_tokens:
            print("Wrong token")
            exit()
        return token, communicat

    def _check_optional_token(self, expected_tokens: List[Token]) -> Union[Tuple[Token, str], Tuple[None, None]]:
        token, communicat = self.next_token()
        if token not in expected_tokens:
            self.saved_token = (token, communicat)
            return None, None
        return token, communicat

    def _add_to_code(self, token: Token, communicat: str):

        if token == Token.ASSIGN:
            self.code += "="

        elif token in (Token.COMPARISON_OPERATORS, Token.MATH_OPERATORS):
            if communicat == "=":
                communicat += "=="
            self.code += " " + communicat + " "

        elif token == Token.CURLY_BRACKET_BEGIN:
            self.code += ":"
            self.indent_ctr += 1

        elif token == Token.CURLY_BRACKET_END:
            self.indent_ctr -= 1

        elif token == Token.SEMICOLON:
            self.code += "\n"
            self.code += " " * 4 * self.indent_ctr

        else:
            self.code += communicat

    def _check_for_statement(self) -> bool:
        for_res = self._check_optional_token([Token.FOR_TOKEN])
        if for_res[1] is None:
            return False

        try:  # chyba niepotrzebne
            id1 = self._check_if_right_token([Token.ID])
            ass1 = self._check_if_right_token([Token.ASSIGN])
            id2 = self._check_if_right_token([Token.ID, Token.NUMBER])
            btw = self._check_if_right_token([Token.BETWEEN])
            id3 = self._check_if_right_token([Token.ID, Token.NUMBER])

            self._add_to_code(*for_res)
            self._add_to_code(*id1)
            self._add_to_code(Token.ID, "in range")
            self._add_to_code(Token.ROUND_BRACKET_BEGIN, "(")
            self._add_to_code(*id2)
            self._add_to_code(Token.ID, ",")
            self._add_to_code(*id3)
            self._add_to_code(Token.ROUND_BRACKET_END, ")")

            self._add_to_code(*self._check_if_right_token([Token.CURLY_BRACKET_BEGIN]))

            res = self._check_statement()
            while (res):
                res = self._check_statement()

            self._add_to_code(*self._check_if_right_token([Token.CURLY_BRACKET_END]))
        except EOFError:
            exit()

        return True

    def _check_statement(self):
        if not self._check_for_statement():
            if not self._check_while_statement():
                if not self._check_if_statement():
                    if not self._check_return_statement():
                        if not self._check_declaration():
                            if not self._check_function_call():
                                exit()

    def _check_expression(self):
        flag = True
        not_res = self._check_optional_token([Token.NOT_TOKEN])
        if not_res[1] is not None:
            self._add_to_code(*not_res)
            flag = False

        if not self._check_math_expression():
            if not self._check_variable_type():
                if flag == True:
                    self._check_if_right_token([Token.SKIP])
                else:
                    exit()
            else:
                self._check_if_right_token([Token.SEMICOLON])
        else:
            self._check_if_right_token([Token.SEMICOLON])




    def _check_while_statement(self) -> bool:
        while_res = self._check_optional_token([Token.WHILE_TOKEN])
        if while_res[1] is None:
            return False
        try:
            self._add_to_code(*while_res)
            self._check_expression()

            self._add_to_code(*self._check_if_right_token([Token.CURLY_BRACKET_BEGIN]))

            res = self._check_statement()
            while (res):
                res = self._check_statement()

            self._add_to_code(*self._check_if_right_token([Token.CURLY_BRACKET_END]))
        except EOFError:
            exit()

        return True

    def _check_if_statement(self) -> bool:
        if_res = self._check_optional_token([Token.IF_TOKEN])
        if if_res[1] is None:
            return False
        try:
            self._add_to_code(*if_res)
            self._check_expression()
            self._add_to_code(*self._check_if_right_token([Token.CURLY_BRACKET_BEGIN]))
            res = self._check_statement()
            while (res):
                res = self._check_statement()
            self._add_to_code(*self._check_if_right_token([Token.CURLY_BRACKET_END]))

            # else
            else_res = self._check_optional_token([Token.ELSE_TOKEN])
            if  else_res[1] is not None:
                self._add_to_code(*else_res)
                self._check_expression()
                self._add_to_code(*self._check_if_right_token([Token.CURLY_BRACKET_BEGIN]))

                res = self._check_statement()
                while (res):
                    res = self._check_statement()
                self._add_to_code(*self._check_if_right_token([Token.CURLY_BRACKET_END]))

        except EOFError:
            exit()

        return True

    def _check_return_statement(self) -> bool:
        return_res = self._check_optional_token([Token.RETURN_TOKEN])
        if return_res[1] is None:
            return False
        self._add_to_code(*return_res)
        self._check_variable_type()

        return True

    def _check_function_definition(self):
        pass

    #and,or,comparision_operators,math_operators
    def _check_math_expression(self):
        pass

    # BOGUS

    def _check_array(self):
        pass

    def _check_declaration(self):
        pass

    def _check_function_call(self):
        pass

    def _check_variable_type(self):
        token, communicat = self._check_optional_token([Token.BOOLEAN, Token.NUMBER, Token.ID])
        if token is not None:
            self._add_to_code(token, communicat)
            return True
        if self._check_array():
            return True
        if self._check_string():
            return True
        return False

    def _check_string(self):
        pass

    def generate(self) -> str:
        pass