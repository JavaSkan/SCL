"""
Definition of Tui KeyWords
"""
import tuiparsing
#TODO add bool
data_types_keywords = {
    'int': tuiparsing.TokenType.INTLIT,
    'flt': tuiparsing.TokenType.FLTLIT,
    'str': tuiparsing.TokenType.STRLIT
}