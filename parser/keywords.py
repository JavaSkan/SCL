"""
Definition of SCL KeyWords
"""
from parser import parsing

#TODO add bool
data_types_keywords = {
    'int': parsing.TokenType.INTLIT,
    'flt': parsing.TokenType.FLTLIT,
    'str': parsing.TokenType.STRLIT
}

new_cmd_varkind_kws = {
    'const',
    'temp',
    'mut'
}