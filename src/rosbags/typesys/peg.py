# Copyright 2020-2022  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""PEG Parser.

Parsing expression grammar inspired parser for simple EBNF-like notations. It
implements just enough features to support parsing of the different ROS message
definition formats.

"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Optional, Pattern, TypeVar, Union

    Tree = Any
    T = TypeVar('T')


class Rule:
    """Rule base class."""

    LIT = 'LITERAL'
    WS = re.compile(r'\s+', re.M | re.S)

    def __init__(
        self,
        value: Union[str, Pattern[str], Rule, list[Rule]],
        rules: dict[str, Rule],
        name: Optional[str] = None,
    ):
        """Initialize.

        Args:
            value: Value of this rule.
            rules: Grammar containing all rules.
            name: Name of this rule.

        """
        self.value = value
        self.rules = rules
        self.name = name

    def skip_ws(self, text: str, pos: int) -> int:
        """Skip whitespace."""
        match = self.WS.match(text, pos)
        return match.span()[1] if match else pos

    def make_node(self, data: T) -> Union[T, dict[str, Union[str, T]]]:
        """Make node for parse tree."""
        return {'node': self.name, 'data': data} if self.name else data

    def parse(self, text: str, pos: int) -> tuple[int, Any]:
        """Apply rule at position."""
        raise NotImplementedError  # pragma: no cover


class RuleLiteral(Rule):
    """Rule to match string literal."""

    def __init__(self, value: str, rules: dict[str, Rule], name: Optional[str] = None):
        """Initialize.

        Args:
            value: Value of this rule.
            rules: Grammar containing all rules.
            name: Name of this rule.

        """
        super().__init__(value, rules, name)
        self.value = value[1:-1].replace('\\\'', '\'')

    def parse(self, text: str, pos: int) -> tuple[int, Any]:
        """Apply rule at position."""
        value = self.value
        assert isinstance(value, str)
        if text[pos:pos + len(value)] == value:
            npos = pos + len(value)
            npos = self.skip_ws(text, npos)
            return npos, (self.LIT, value)
        return -1, ()


class RuleRegex(Rule):
    """Rule to match regular expression."""

    value: Pattern[str]

    def __init__(self, value: str, rules: dict[str, Rule], name: Optional[str] = None):
        """Initialize.

        Args:
            value: Value of this rule.
            rules: Grammar containing all rules.
            name: Name of this rule.

        """
        super().__init__(value, rules, name)
        self.value = re.compile(value[2:-1], re.M | re.S)

    def parse(self, text: str, pos: int) -> tuple[int, Any]:
        """Apply rule at position."""
        match = self.value.match(text, pos)
        if not match:
            return -1, ()
        npos = self.skip_ws(text, match.span()[1])
        return npos, self.make_node(match.group())


class RuleToken(Rule):
    """Rule to match token."""

    value: str

    def parse(self, text: str, pos: int) -> tuple[int, Any]:
        """Apply rule at position."""
        token = self.rules[self.value]
        npos, data = token.parse(text, pos)
        if npos == -1:
            return npos, data
        return npos, self.make_node(data)


class RuleOneof(Rule):
    """Rule to match first matching subrule."""

    value: list[Rule]

    def parse(self, text: str, pos: int) -> tuple[int, Any]:
        """Apply rule at position."""
        for value in self.value:
            npos, data = value.parse(text, pos)
            if npos != -1:
                return npos, self.make_node(data)
        return -1, ()


class RuleSequence(Rule):
    """Rule to match a sequence of subrules."""

    value: list[Rule]

    def parse(self, text: str, pos: int) -> tuple[int, Any]:
        """Apply rule at position."""
        data = []
        npos = pos
        for value in self.value:
            npos, node = value.parse(text, npos)
            if npos == -1:
                return -1, ()
            data.append(node)
        return npos, self.make_node(tuple(data))


class RuleZeroPlus(Rule):
    """Rule to match zero or more occurences of subrule."""

    value: Rule

    def parse(self, text: str, pos: int) -> tuple[int, Any]:
        """Apply rule at position."""
        data: list[Any] = []
        lpos = pos
        while True:
            npos, node = self.value.parse(text, lpos)
            if npos == -1:
                return lpos, self.make_node(tuple(data))
            data.append(node)
            lpos = npos


class RuleOnePlus(Rule):
    """Rule to match one or more occurences of subrule."""

    value: Rule

    def parse(self, text: str, pos: int) -> tuple[int, Any]:
        """Apply rule at position."""
        npos, node = self.value.parse(text, pos)
        if npos == -1:
            return -1, ()
        data = [node]
        lpos = npos
        while True:
            npos, node = self.value.parse(text, lpos)
            if npos == -1:
                return lpos, self.make_node(tuple(data))
            data.append(node)
            lpos = npos


class RuleZeroOne(Rule):
    """Rule to match zero or one occurence of subrule."""

    value: Rule

    def parse(self, text: str, pos: int) -> tuple[int, Any]:
        """Apply rule at position."""
        npos, node = self.value.parse(text, pos)
        if npos == -1:
            return pos, self.make_node(())
        return npos, self.make_node((node,))


class Visitor:  # pylint: disable=too-few-public-methods
    """Visitor transforming parse trees."""

    RULES: dict[str, Rule] = {}

    def __init__(self) -> None:
        """Initialize."""

    def visit(self, tree: Tree) -> Tree:
        """Visit all nodes in parse tree."""
        if isinstance(tree, tuple):
            return tuple(self.visit(x) for x in tree)

        if isinstance(tree, str):
            return tree

        assert isinstance(tree, dict), tree
        assert list(tree.keys()) == ['node', 'data'], tree.keys()

        tree['data'] = self.visit(tree['data'])
        func = getattr(self, f'visit_{tree["node"]}', lambda x: x)
        return func(tree['data'])


def split_token(tok: str) -> list[str]:
    """Split repetition and grouping tokens."""
    return list(filter(None, re.split(r'(^\()|(\)(?=[*+?]?$))|([*+?]$)', tok)))


def collapse_tokens(toks: list[Optional[Rule]], rules: dict[str, Rule]) -> Rule:
    """Collapse linear list of tokens to oneof of sequences."""
    value: list[Rule] = []
    seq: list[Rule] = []
    for tok in toks:
        if tok:
            seq.append(tok)
        else:
            value.append(RuleSequence(seq, rules) if len(seq) > 1 else seq[0])
            seq = []
    value.append(RuleSequence(seq, rules) if len(seq) > 1 else seq[0])
    return RuleOneof(value, rules) if len(value) > 1 else value[0]


def parse_grammar(grammar: str) -> dict[str, Rule]:
    """Parse grammar into rule dictionary."""
    rules: dict[str, Rule] = {}
    for token in grammar.split('\n\n'):
        lines = token.strip().split('\n')
        name, *defs = lines
        items = [z for x in defs for y in x.split(' ') if y for z in split_token(y) if z]
        assert items
        assert items[0] == '='
        items.pop(0)
        stack: list[Optional[Rule]] = []
        parens: list[int] = []
        while items:
            tok = items.pop(0)
            if tok in ['*', '+', '?']:
                assert isinstance(stack[-1], Rule)
                stack[-1] = {
                    '*': RuleZeroPlus,
                    '+': RuleOnePlus,
                    '?': RuleZeroOne,
                }[tok](stack[-1], rules)
            elif tok == '/':
                stack.append(None)
            elif tok == '(':
                parens.append(len(stack))
            elif tok == ')':
                index = parens.pop()
                rule = collapse_tokens(stack[index:], rules)
                stack = stack[:index]
                stack.append(rule)
            elif len(tok) > 2 and tok[:2] == 'r\'':
                stack.append(RuleRegex(tok, rules))
            elif tok[0] == '\'':
                stack.append(RuleLiteral(tok, rules))
            else:
                stack.append(RuleToken(tok, rules))

        res = collapse_tokens(stack, rules)
        res.name = name
        rules[name] = res
    return rules
