from .tokens import Token, TokenType
from .indexed import Indexed
from string import whitespace
from runtime.errors import quick_err

import sys

class Lexer(Indexed):
    def __init__(self, string_input: str) -> None:
        super().__init__(string_input)

    def display_err(self, msg):
        out = self.inp + '\n'
        for i in range(len(self.inp)):
            out += '^' if i == self.ix else '-'
        quick_err(tag="LEX-ERR",msg=msg)

    def parse_int(self) -> Token:
        buf = self.cur()
        while self.has_next() and ('0' <= self.next() <= '9'):
            self.advance()
            buf += self.cur()
        return Token(TokenType.INT, buf)

    def parse_number(self) -> Token:
        buf = self.parse_int().value
        if self.has_next() and self.next() == '.':
            self.advance()
            if self.has_next() and ('0' <= self.next() <= '9'):
                buf += self.cur()
                self.advance()
                buf += self.parse_int().value
                return Token(TokenType.FLT, buf)
            else:
                self.back()
        return Token(TokenType.INT, buf)

    def parse_arg(self) -> Token:
        buf = self.cur()
        while self.has_next() and (
                'A' <= self.next().upper() <= 'Z' or ('0' <= self.next().upper() <= '9') or self.next() == '_'):
            self.advance()
            buf += self.cur()
        return Token(TokenType.IDT, buf)

    def parse_str(self) -> Token:
        buf = ""
        fst_idx = self.ix  # used for error (if existing)
        self.advance()
        while self.has_next() and self.cur() != '"':
            buf += self.cur()
            self.advance()

        if self.cur() == '"':
            return Token(TokenType.STR, buf)
        else:
            self.ix = fst_idx
            self.display_err("Extra double quote here")

    def tokenize(self) -> list[Token]:
        p = []
        while self.has_next():
            self.advance()
            match self.cur():
                case i if '0' <= i <= '9':
                    t = self.parse_number()
                    p.append(t)
                case id if ('A' <= id.upper() <= 'Z') or id == '_':
                    t = self.parse_arg()
                    p.append(t)
                case '"':
                    t = self.parse_str()
                    p.append(t)
                case '(':
                    p.append(Token(TokenType.LPAR, self.cur()))
                case ')':
                    p.append(Token(TokenType.RPAR, self.cur()))
                case '[':
                    p.append(Token(TokenType.LBRK, self.cur()))
                case ']':
                    p.append(Token(TokenType.RBRK, self.cur()))
                case '{':
                    p.append(Token(TokenType.LCBK, self.cur()))
                case '}':
                    p.append(Token(TokenType.RCBK, self.cur()))
                case ':':
                    p.append(Token(TokenType.CLN, self.cur()))
                case ';':
                    p.append(Token(TokenType.SMCL, self.cur()))
                case ',':
                    p.append(Token(TokenType.CMA, self.cur()))
                case '.':
                    p.append(Token(TokenType.DOT, self.cur()))
                case '+':
                    p.append(Token(TokenType.PLUS, self.cur()))
                case '-':
                    p.append(Token(TokenType.MINUS, self.cur()))
                case '*':
                    p.append(Token(TokenType.STAR, self.cur()))
                case '/':
                    p.append(Token(TokenType.SLASH, self.cur()))
                case '%':
                    p.append(Token(TokenType.PERCT, self.cur()))
                case '@':
                    p.append(Token(TokenType.AT, self.cur()))
                case '$':
                    p.append(Token(TokenType.DLR, self.cur()))
                case c if c in whitespace:
                    pass
                case _:
                    p.append(Token(TokenType.UNK, self.cur()))
        return p