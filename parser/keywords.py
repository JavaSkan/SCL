"""
Definition of SCL Keywords and Symbols
"""

#Basic datatypes
basic_datatypes = {
    'int',
    'flt',
    'str',
    'bool'
}

#Complex datatypes
complex_datatypes = {
    'arr',
    'any'
}

#array command options
arr_opts = {
    'new'
}

#all possible types of a return value
return_datatypes = basic_datatypes.copy()
return_datatypes.add('any')
return_datatypes.add('nil')

#all possible types of arrays
arr_types = basic_datatypes.copy()
arr_types.add('any')

#all possible types of function formal parameters
fml_prm_datatypes = basic_datatypes.copy()
fml_prm_datatypes.update(complex_datatypes)

#all variable kinds
varkinds = {
    'const',
    'temp',
    'mut'
}

#foreach command options
foreach_opts = {
    'in'
}

class BOOLEAN_KWS:
    AND  = r'&'
    OR   = r'\|'
    EQL  = r'='
    NOT  = r'!'
    TRUE = r'true'
    FALSE= r'false'