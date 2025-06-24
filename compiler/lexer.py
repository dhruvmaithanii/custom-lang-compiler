import re

TOKEN_SPEC = [
    # Hinglish symbols and keywords FIRST
    ('SHURU', r'\bshuru karo\b'),
    ('KHATAM', r'\bkhatam karo\b'),
    ('RAKHO', r'\brakho\b'),
    ('EQUALTO', r'\bbarabar hai\b'),   # Moved up
    ('ASSIGN', r'\bbarabar\b'),
    ('DIKHAO', r'\bdikhao\b'),
    ('AGAR', r'\bagar\b'),
    ('NAHITO', r'\bnahi to\b'),
    ('WARNA', r'\bwarna\b'),
    ('JABTAK', r'\bjabtak\b'),
    ('KELIYE', r'\bke liye\b'),
    ('JABKARO', r'\bjab karo\b'),
    ('CHHODO', r'\bchhodo\b'),
    ('TODO', r'\btodo\b'),
    ('WAPIS', r'\bwapis\b'),

    # Parentheses, Brackets, Delimiters
    ('LBRACE', r'\bshuru bhai\b'),
    ('RBRACE', r'\bband karo\b'),
    ('LPAREN', r'\bkholo\b'),
    ('RPAREN', r'\bband\b'),
    ('LBRACKET', r'\['),
    ('RBRACKET', r'\]'),
    ('COMMA', r','),
    ('ARDHAVIRAM', r'\bardhaviram\b'),

    # Array keywords
    ('SOOCHI', r'\bsoochi\b'),
    ('ELEMENT', r'\belement\b'),

    # Operators
    ('JODO', r'\bjodo\b'),
    ('GHATAYO', r'\bghatayo\b'),
    ('GUNA', r'\bguna\b'),
    ('BHAG', r'\bbhag\b'),
    ('LESSTHAN', r'\bchota hai\b'),
    ('GREATERTHAN', r'\bbada hai\b'),

    # Literals
    ('SANKHYA', r'\d+'),
    ('TANTA', r'"(?:\\.|[^"\\])*"'),

    # IDENTIFIERS LAST
    ('PEHCHAN', r'[a-zA-Z_]\w*'),

    # Whitespace, Comments, Errors
    ('NEWLINE', r'\n'),
    ('SKIP', r'[ \t]+'),
    ('MISMATCH', r'.'),
]

TOKEN_REGEX = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPEC)

def lexer(code):
    for mo in re.finditer(TOKEN_REGEX, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind in ('SKIP', 'COMMENT'):
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f"Unexpected character: {value}")
        elif kind == 'SANKHYA':
            yield (kind, int(value))
        else:
            yield (kind, value)
