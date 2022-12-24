from parser import Parser
from resources import Token
from typing import List,Tuple


class Generator:
    def __init__(self, pseudocode: str):
        self.parser = Parser(pseudocode)
        self.code = ""

    def next_token(self) -> Tuple[str, Token]:
        tupl = next(self.parser, None)
        if tupl == None:
            # TODO
            pass
        return tupl

    def _check_if_right_token(self, right_token: List[Token]) -> (str,bool):
        communicat, token = self.next_token()
        if token != right_token:
            return False
        return (communicat,True)

    def _check_statement(self):
        #TODO
        pass

    '''for_statement: for_token id assign [id | number] between [id | number] curly_bracket_begin
      [statement([new_line][statement])*] curly_bracket_end'''


    def _check_for_statement(self):
        self._check_if_right_token([Token.ID])
        self._check_if_right_token([Token.ASSIGN])
        self._check_if_right_token([Token.ID, Token.NUMBER])
        self._check_if_right_token([Token.BETWEEN])
        self._check_if_right_token([Token.ID, Token.NUMBER])
        self._check_if_right_token([Token.CURLY_BRACKET_BEGIN])




    def generate(self) -> str:

        while(1):
            communicat, token = self.next_token()
            if token == Token.FOR_TOKEN:
                self._check_for_statement()

