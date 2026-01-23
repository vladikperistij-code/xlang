# lexer.py
import re

TOKEN_SPEC = [
    ("NUMBER",   r"\d+"),
    ("STRING",   r'"[^"]*"'),
    ("IDENT",    r"[a-zA-Z_][a-zA-Z0-9_]*"),
    ("PLUS",     r"\+"),
    ("MINUS",    r"-"),
    ("MUL",      r"\*"),
    ("DIV",      r"/"),
    ("EQUAL",    r"="),
    ("LPAREN",   r"\("),
    ("RPAREN",   r"\)"),
    ("COMMA",    r","),
    ("COLON",    r":"),
    ("NEWLINE",  r"\n"),
    ("SKIP",     r"[ \t]+"),
]

KEYWORDS = {
    "var": "VAR",
    "func": "FUNC",
    "if": "IF",
    "else": "ELSE",
    "print": "PRINT",
    "sleep": "SLEEP",
    "echo": "ECHO",
}

token_re = re.compile(
    "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC)
)

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"{self.type}({self.value})"


def tokenize(code: str):
    tokens = []
    for match in token_re.finditer(code):
        kind = match.lastgroup
        value = match.group()

        if kind == "SKIP" or kind == "NEWLINE":
            continue

        if kind == "IDENT" and value in KEYWORDS:
            kind = KEYWORDS[value]

        tokens.append(Token(kind, value))

    return tokens
