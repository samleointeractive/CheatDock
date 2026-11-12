"""Split a multi-line snippet into the separate commands it contains.

Most multi-line cards are a few related one-liners ("Copy-Item ...",
"Move-Item ...") that people want to copy one at a time. Some are a single
command spread over several lines (a SQL query, a pandas call with arguments,
a Python function). This groups lines so each group can be pasted and run.

A line continues the current command when:
- it is indented, or starts with a closing bracket, "|", ".method(" or a
  block keyword (else, except, catch, done, fi, RETURN...)
- the previous line ends with a continuation sign (| ` \\ , ( [ { = + && || AND OR)
  or is a Python decorator
- brackets opened earlier are still open
- the snippet is SQL that uses ";" as a terminator and the current command has no ";" yet

A blank line ends a command unless the next line is indented.
"""

from __future__ import annotations

import re

_CONT_END = re.compile(r"(\||`|\s\\|,|\(|\[|\{|=|\+|&&|\|\||\bAND|\bOR)$", re.IGNORECASE)
_CONT_START = re.compile(
    r"^([)\]}|]|\.[A-Za-z_]\w*\("
    r"|(catch|finally|else|elif|except|done|fi|esac|then|do|VAR|RETURN)\b)"
)
_KEYS = re.compile(r"^(Ctrl|Shift|Alt|Win|F\d)\b")  # keyboard shortcuts, not code
_SQL = re.compile(r"^\s*(SELECT|WITH|INSERT|UPDATE|DELETE|CREATE|ALTER|DROP|BEGIN)\b", re.MULTILINE)


def _depth(line: str) -> int:
    """Net bracket change for one line, ignoring brackets inside quotes."""
    depth, quote = 0, ""
    for ch in line:
        if quote:
            if ch == quote:
                quote = ""
        elif ch in "\"'":
            quote = ch
        elif ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
    return depth


def split_commands(code: str) -> list[str]:
    lines = code.split("\n")
    semicolons = bool(_SQL.search(code)) and any(l.rstrip().endswith(";") for l in lines)
    groups: list[list[str]] = []
    depth = 0
    blank = False
    for line in lines:
        text = line.rstrip()
        if not text.strip():
            blank = True
            continue
        prev = groups[-1] if groups else None
        joins = False
        if prev:
            last = prev[-1]
            indented = text[0] in " \t"
            if blank:
                joins = indented or depth > 0
            else:
                joins = (
                    depth > 0
                    or indented
                    or bool(_CONT_START.match(text))
                    or (bool(_CONT_END.search(last)) and not _KEYS.match(last))
                    or last.startswith("@")
                    or (semicolons and not last.endswith(";"))
                )
        if joins:
            if blank:
                prev.append("")
            prev.append(text)
        else:
            groups.append([text])
            depth = 0
        depth = max(0, depth + _depth(text))
        blank = False
    return ["\n".join(g) for g in groups]
