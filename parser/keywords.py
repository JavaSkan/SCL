"""
Definition of SCL KeyWords
"""

data_types_keywords = {
    'int',
    'flt',
    'str',
    'bool'
}

funret_data_types_keywords = data_types_keywords.copy()
funret_data_types_keywords.add('nil')

new_cmd_varkind_kws = {
    'const',
    'temp',
    'mut'
}