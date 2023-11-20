import ply.lex as lex

reserved = {
    "program": "PROGRAM",
    "vars": "VARS",
    "function": "FUNCTION",
    "main": "MAIN",
    "return": "RETURN",
    "read": "READ",
    "write": "WRITE",
    "if": "IF",
    "then": "THEN",
    "else": "ELSE",
    "while": "WHILE",
    "do": "DO",
    "for": "FOR",
    "to": "TO",
    "int": "INT",
    "float": "FLOAT",
    "char": "CHAR",
    "true": "TRUE",
    "false": "FALSE",
    "void": "VOID",
}

# --- Tokenizer
tokens = [
    "SEMICOLON",
    "COMMA",
    "LPAREN",
    "RPAREN",
    "LBRACKET",
    "RBRACKET",
    "LBRACE",
    "RBRACE",
    "EQUAL",
    "AND",
    "OR",
    "EQUALS",
    "LTHAN",
    "GTHAN",
    "LEQUAL",
    "GEQUAL",
    "DIFFERENCE",
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "MOD",
    "ID",
    "CTE_C",
    "CTE_S",
    "CTE_I",
    "CTE_F",
] + list(reserved.values())

# Ignored characters
t_ignore = " \t"

# Token matching rules are written as regexs
t_SEMICOLON = r";"
t_COMMA = r","

t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LBRACKET = r"\["
t_RBRACKET = r"\]"
t_LBRACE = r"{"
t_RBRACE = r"}"

t_EQUAL = r"="
t_AND = r"&"
t_OR = r"\|"

t_GTHAN = r"\>"
t_LTHAN = r"\<"
t_GEQUAL = r"\>="
t_LEQUAL = r"\<="
t_EQUALS = r"=="
t_DIFFERENCE = r"\<\>"

t_PLUS = r"\+"
t_MINUS = r"-"
t_TIMES = r"\*"
t_DIVIDE = r"/"
t_MOD = r"%"

t_CTE_S = r'"(.*?)"'
t_CTE_C = r"(L)?\'([^\\\n]|(\\.))*?\'"


def t_ID(t):
    r"([a-z][a-zA-Z0-9]*)"
    if t.value in reserved:
        t.type = reserved[t.value]
    return t


def t_CTE_F(t):
    r"[-]?[0-9]+([.][0-9]+)"
    t.value = float(t.value)
    return t


def t_CTE_I(t):
    r"[-]?[0-9]+"
    t.value = int(t.value)
    return t


def t_error(t):
    print(f"Illegal character {t.value[0]} in line {t.lexer.lineno}")
    t.lexer.skip(1)


def t_LINE_COMMENT(t):
    r"%.*"
    pass


def t_skip_newline(t):
    r"\n+"
    t.lexer.lineno += t.value.count("\n")


lexer = lex.lex()
