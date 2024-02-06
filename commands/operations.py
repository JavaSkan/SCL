from runtime.allocable import DT_TYPES
from parser.parsing import TokenType

################################
# DATA TYPES
################################


datatypes_support_add = {
    DT_TYPES.INT,
    DT_TYPES.FLT,
    DT_TYPES.STR
}

datatypes_support_sub = {
    DT_TYPES.INT,
    DT_TYPES.FLT
}

datatypes_support_mul = {
    DT_TYPES.INT,
    DT_TYPES.FLT
}

datatypes_support_div = {
    DT_TYPES.INT,
    DT_TYPES.FLT
}

datatypes_support_pow = {
    DT_TYPES.INT,
    DT_TYPES.FLT
}

################################
# TOKEN TYPES
################################

tokentypes_support_add = {
    TokenType.INTLIT,
    TokenType.FLTLIT,
    TokenType.STRLIT
}

tokentypes_support_sub = {
    TokenType.INTLIT,
    TokenType.FLTLIT,
}

tokentypes_support_mul = {
    TokenType.INTLIT,
    TokenType.FLTLIT,
}

tokentypes_support_div = {
    TokenType.INTLIT,
    TokenType.FLTLIT,
}

tokentypes_support_pow = {
    TokenType.INTLIT,
    TokenType.FLTLIT,
}