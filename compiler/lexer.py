"""
SecureCC — Phase 1: Lexical Analysis (Tokenizer)

Converts raw C source code into a stream of tokens.
Each token carries its type, value, and source line number.
This is the first phase of the compiler pipeline.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List


# ── C language keywords ──────────────────────────────────────────────
C_KEYWORDS = {
    "auto", "break", "case", "char", "const", "continue", "default", "do",
    "double", "else", "enum", "extern", "float", "for", "goto", "if",
    "inline", "int", "long", "register", "restrict", "return", "short",
    "signed", "sizeof", "static", "struct", "switch", "typedef", "union",
    "unsigned", "void", "volatile", "while",
}


# ── Token type constants ─────────────────────────────────────────────
class TokenType:
    KEYWORD      = "KEYWORD"
    IDENTIFIER   = "IDENTIFIER"
    INTEGER      = "INTEGER"
    FLOAT        = "FLOAT"
    STRING       = "STRING"
    CHAR_LIT     = "CHAR"
    OPERATOR     = "OPERATOR"
    PUNCTUATION  = "PUNCTUATION"
    PREPROCESSOR = "PREPROCESSOR"
    COMMENT      = "COMMENT"
    EOF          = "EOF"


@dataclass
class Token:
    """A single lexical token."""
    type: str
    value: str
    line: int

    def __repr__(self) -> str:
        return f"Token({self.type}, {self.value!r}, line={self.line})"


# ── Ordered token patterns (longest match first) ─────────────────────
_PATTERNS: list[tuple[str, str | None]] = [
    # Block comments
    (r"/\*[\s\S]*?\*/",                                       TokenType.COMMENT),
    # Line comments
    (r"//[^\n]*",                                             TokenType.COMMENT),
    # Preprocessor directives
    (r"#\s*(?:include|define|undef|ifdef|ifndef|if|else|elif|"
     r"endif|pragma|error|warning)[^\n]*",                    TokenType.PREPROCESSOR),
    # String literals
    (r'"(?:[^"\\]|\\.)*"',                                    TokenType.STRING),
    # Character literals
    (r"'(?:[^'\\]|\\.)*'",                                    TokenType.CHAR_LIT),
    # Floating-point literals (must come before integer)
    (r"\b\d+\.\d*(?:[eE][+-]?\d+)?[fFlL]?\b",                TokenType.FLOAT),
    (r"\b\d*\.\d+(?:[eE][+-]?\d+)?[fFlL]?\b",                TokenType.FLOAT),
    # Hex integer literals
    (r"\b0[xX][0-9a-fA-F]+[uUlL]*\b",                        TokenType.INTEGER),
    # Octal integer literals
    (r"\b0[0-7]+[uUlL]*\b",                                  TokenType.INTEGER),
    # Decimal integer literals
    (r"\b\d+[uUlL]*\b",                                      TokenType.INTEGER),
    # Multi-character operators (order: longest first)
    (r"<<=|>>=|->|<<|>>|<=|>=|==|!=|&&|\|\|"
     r"|\+=|-=|\*=|/=|%=|&=|\|=|\^=|\+\+|--",                TokenType.OPERATOR),
    # Single-character operators
    (r"[+\-*/%=<>!&|^~?:]",                                  TokenType.OPERATOR),
    # Punctuation
    (r"[{}\[\]();,.]",                                        TokenType.PUNCTUATION),
    # Identifiers / keywords
    (r"\b[A-Za-z_]\w*\b",                                    "_WORD"),
    # Whitespace (skipped, but we need to count newlines)
    (r"\s+",                                                  None),
]

# Pre-compile patterns once at import time
_COMPILED = [(re.compile(p), t) for p, t in _PATTERNS]


def tokenize(source: str) -> List[Token]:
    """
    Perform lexical analysis on C source code.

    Returns an ordered list of Token objects. Comments are preserved
    as COMMENT tokens so later phases can optionally use them.
    The list always ends with a single EOF token.
    """
    tokens: List[Token] = []
    pos = 0
    line = 1
    length = len(source)

    while pos < length:
        matched = False
        for regex, token_type in _COMPILED:
            m = regex.match(source, pos)
            if not m:
                continue

            value = m.group(0)
            newlines = value.count("\n")

            if token_type == "_WORD":
                # Classify as keyword or identifier
                if value in C_KEYWORDS:
                    tokens.append(Token(TokenType.KEYWORD, value, line))
                else:
                    tokens.append(Token(TokenType.IDENTIFIER, value, line))
            elif token_type is not None:
                tokens.append(Token(token_type, value, line))
            # else: whitespace — skip silently

            line += newlines
            pos = m.end()
            matched = True
            break

        if not matched:
            # Skip unrecognised character
            if source[pos] == "\n":
                line += 1
            pos += 1

    tokens.append(Token(TokenType.EOF, "", line))
    return tokens
