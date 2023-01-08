from typing import List, Tuple, Union

from code_parser import Parser
from resources import Token


class Generator:
    def __init__(self, pseudocode: str):
        self.parser = Parser(pseudocode)
        self.code = ""
        self.saved_token = None
        self.indent_ctr = 0

    def _next_token_whitespace(self) -> Tuple[Token, str]:
        if self.saved_token is not None:
            token = self.saved_token
            self.saved_token = None
            return token
        token = next(self.parser, None)
        if token is None:
            raise EOFError
        if token[0] == Token.ERROR:
            print("Token error")
            exit()
        return token

    def _next_token(self) -> Tuple[Token, str]:
        token = self._next_token_whitespace()
        if token[0] == Token.WHITESPACE:
            return self._next_token()
        return token

    def _check_if_right_token(self, right_tokens: List[Token]) -> Tuple[Token, str]:
        token, communicat = self._next_token()
        if token not in right_tokens:
            print("Wrong token - check grammar")
            exit()
        return token, communicat

    def _check_optional_token(self, expected_tokens: List[Token]) -> Union[Tuple[Token, str], Tuple[None, None]]:
        token, communicat = self._next_token()
        if token not in expected_tokens:
            self.saved_token = (token, communicat)
            return None, None
        return token, communicat

    def _add_to_code(self, token: Token, communicat: str):

        if token == Token.ASSIGN:
            self.code += "="

        elif token in (Token.COMPARISON_OPERATORS, Token.MATH_OPERATORS):
            if communicat == "=":
                communicat += "="
            self.code +=  communicat

        elif token == Token.CURLY_BRACKET_BEGIN:
            self.code += ":\n"
            self.indent_ctr += 1
            self.code += " " * 4 * self.indent_ctr

        elif token == Token.CURLY_BRACKET_END:
            self.code = self.code[:-4]
            self.indent_ctr -= 1

        elif token == Token.SEMICOLON:
            self.code += "\n"
            self.code += " " * 4 * self.indent_ctr

        elif token in [Token.IF_TOKEN, Token.FOR_TOKEN, Token.OR_TOKEN, Token.AND_TOKEN, Token.NOT_TOKEN,
                       Token.RETURN_TOKEN, Token.FUNCTION]:
            self.code += communicat + " "

        else:
            self.code += communicat

    def _check_statement_or_skip(self) -> bool:
        res = self._check_statement()
        if not res:
            self._add_to_code(*self._check_if_right_token([Token.SKIP]))
        while True:
            res = self._check_statement()
            if not res:
                skip_res = self._check_optional_token([Token.SKIP])
                if skip_res[1] is None:
                    break
                else:
                    self._add_to_code(*skip_res)
        return True

    def _check_for_statement(self) -> bool:
        for_res = self._check_optional_token([Token.FOR_TOKEN])
        if for_res[1] is None:
            return False

        try:  # chyba niepotrzebne
            self._check_if_right_token([Token.ROUND_BRACKET_BEGIN])
            id1 = self._check_if_right_token([Token.ID])
            ass1 = self._check_if_right_token([Token.ASSIGN])
            id2 = self._check_if_right_token([Token.ID, Token.NUMBER])
            btw = self._check_if_right_token([Token.BETWEEN])
            id3 = self._check_if_right_token([Token.ID, Token.NUMBER])

            self._check_if_right_token([Token.ROUND_BRACKET_END])

            self._add_to_code(*for_res)
            self._add_to_code(*id1)
            self._add_to_code(Token.STRING, " in range")
            self._add_to_code(Token.ROUND_BRACKET_BEGIN, "(")
            self._add_to_code(*id2)
            self._add_to_code(Token.ID, ",")
            self._add_to_code(*id3)
            self._add_to_code(Token.ROUND_BRACKET_END, ")")
            self._add_to_code(*self._check_if_right_token([Token.CURLY_BRACKET_BEGIN]))

            self._check_statement_or_skip()

            self._add_to_code(*self._check_if_right_token([Token.CURLY_BRACKET_END]))
        except EOFError:
            exit()

        return True

    def _check_statement(self) -> bool:
        if not self._check_id_starting():
            if not self._check_for_statement():
                if not self._check_while_statement():
                    if not self._check_if_statement():
                        if not self._check_return_statement():
                            if not self._check_function_definition():
                                return False
        return True

    def _check_expression(self) -> bool:
        not_res = self._check_optional_token([Token.NOT_TOKEN])
        if not_res[1] is not None:
            self._add_to_code(*not_res)

        if self._check_variable_type():
            self._check_combined_expression()
            return True
        return False


    def _check_while_statement(self) -> bool:
        while_res = self._check_optional_token([Token.WHILE_TOKEN])
        if while_res[1] is None:
            return False
        try:
            self._add_to_code(*while_res)
            self._check_if_right_token([Token.ROUND_BRACKET_BEGIN])
            if not self._check_expression():
                print("ERROR: while statement must have expression")
                exit()
            self._check_if_right_token([Token.ROUND_BRACKET_END])

            self._add_to_code(*self._check_if_right_token([Token.CURLY_BRACKET_BEGIN]))

            self._check_statement_or_skip()

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
            self._check_if_right_token([Token.ROUND_BRACKET_BEGIN])
            if not self._check_expression():
                print("ERROR: if statement must have expression")
                exit()
            self._check_if_right_token([Token.ROUND_BRACKET_END])
            self._add_to_code(*self._check_if_right_token([Token.CURLY_BRACKET_BEGIN]))
            self._check_statement_or_skip()
            self._add_to_code(*self._check_if_right_token([Token.CURLY_BRACKET_END]))

            # else
            else_res = self._check_optional_token([Token.ELSE_TOKEN])
            if else_res[1] is not None:
                self._add_to_code(*else_res)
                self._add_to_code(*self._check_if_right_token([Token.CURLY_BRACKET_BEGIN]))
                self._check_statement_or_skip()
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

        self._add_to_code(*self._check_if_right_token([Token.SEMICOLON]))

        return True

    def _check_function_definition(self) -> bool:
        func_res = self._check_optional_token([Token.FUNCTION])
        if func_res[1] is None:
            return False
        try:
            self._add_to_code(*func_res)
            self._add_to_code(*self._check_if_right_token([Token.ID]))
            self._add_to_code(*self._check_if_right_token([Token.ROUND_BRACKET_BEGIN]))

            id1 = self._check_optional_token([Token.ID])
            if id1[1] is not None:
                self._add_to_code(*id1)
            if id1[1] is not None:
                while True:
                    com1 = self._check_optional_token([Token.COMMA])
                    if com1[1] is None:
                        break
                    self._add_to_code(*com1)
                    self._add_to_code(*self._check_if_right_token([Token.ID]))

            self._add_to_code(*self._check_if_right_token([Token.ROUND_BRACKET_END]))
            self._add_to_code(*self._check_if_right_token([Token.CURLY_BRACKET_BEGIN]))

            if not self._check_statement():
                exit()
            while self._check_statement():
                #checking additional statements in function def
                pass

            self._check_return_statement()

            self._add_to_code(*self._check_if_right_token([Token.CURLY_BRACKET_END]))
        except EOFError:
            exit()

        return True

    # and,or,comparision_operators,math_operators
    def _check_combined_expression(self) -> bool:
        token, communicat = self._check_optional_token(
            [Token.AND_TOKEN, Token.OR_TOKEN, Token.COMPARISON_OPERATORS, Token.MATH_OPERATORS])
        if token is None:
            return False
        self._add_to_code(token, communicat)
        if not self._check_expression():
            print("Error: expected expression")
            exit()
        return True

    def _check_array(self) -> bool:
        token, communicat = self._check_optional_token([Token.SQUARE_BRACKET_BEGIN])
        if token is None:
            return False
        self._add_to_code(token, communicat)
        if not self._check_variable_type():
            print("ERROR: expected variable type in array")
            exit()
        while True:
            token, communicat = self._check_optional_token([Token.COMMA])
            if token is None:
                break
            self._add_to_code(token, communicat)
            if not self._check_variable_type():
                print("ERROR: expected variable type in array")
                exit()

        token, communicat = self._check_if_right_token([Token.SQUARE_BRACKET_END])
        self._add_to_code(token, communicat)
        return True

    def _check_declaration(self) -> bool:
        token, communicat = self._check_optional_token([Token.ASSIGN])
        if token is None:
            return False
        self._add_to_code(token, communicat)
        if not self._check_variable_type():
            print("ERROR: expected variable type in declaration")
            exit()
        self._add_to_code(*self._check_if_right_token([Token.SEMICOLON]))
        return True

    def _check_function_call(self) -> bool:
        token, communicat = self._check_optional_token([Token.ROUND_BRACKET_BEGIN])
        if token is None:
            return False
        self._add_to_code(token, communicat)
        self._check_variable_type()
        while True:
            token, communicat = self._check_optional_token([Token.COMMA])
            if token is None:
                break
            self._add_to_code(token, communicat)
            self._check_variable_type()
        token, communicat = self._check_if_right_token([Token.ROUND_BRACKET_END])
        self._add_to_code(token, communicat)
        self._add_to_code(*self._check_if_right_token([Token.SEMICOLON]))
        return True

    def _check_variable_type(self) -> bool:
        token, communicat = self._check_optional_token([Token.BOOLEAN, Token.NUMBER, Token.ID])
        if token is not None:
            self._add_to_code(token, communicat)
            return True
        if self._check_array():
            return True
        if self._check_string():
            return True
        return False

    #  will print only correct tokens (maybe we should add errors to be availabl
    def _check_string(self) -> bool:
        token, communicat = self._check_optional_token([Token.QUOTATION_MARK])
        if token is None:
            return False
        self._add_to_code(token, communicat)
        token, communicat = self._next_token_whitespace()
        while token != Token.QUOTATION_MARK:
            self._add_to_code(Token.STRING, communicat)
            token, communicat = self._next_token_whitespace()
        self._add_to_code(token, communicat)
        return True

    def _check_id_starting(self) -> bool:
        token, communicat = self._check_optional_token([Token.ID])
        if token is None:
            return False
        self._add_to_code(token, communicat)
        if self._check_declaration():
            return True
        if self._check_function_call():
            return True
        return False

    def generate(self):
        try:
            while self._check_statement():
                pass

        except EOFError:
            print(self.code)
            exit()

        print("Not a statement")
