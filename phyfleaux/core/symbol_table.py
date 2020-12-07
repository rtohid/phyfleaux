from __future__ import absolute_import
from __future__ import annotations
from phyfleaux.plugins.tiramisu import Buffer, Function, Call

__license__ = """
Copyright (c) 2020 R. Tohid (@rtohid)

Distributed under the Boost Software License, Version 1.0. (See accompanying
file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""

from collections import ChainMap
from typing import Union

current_namespace = []


class Table:
    def add_symbol(self, symbol: Union[Buffer, Function, Call]):
        current_namespace.append(self.namespace)


class NameSpace:
    def __init__(self, namespace=None):
        self.namespace = namespace

    def __enter__(self):
        if self.namespace:
            current_namespace.append(self.namespace)

    def __exit__(self, type, value, traceback):
        if self.namespace:
            current_namespace.pop()


class SymbolTable:
    @staticmethod
    def add_symbol(symbol):
        if isinstance(symbol, Function):
            symbol_table['_'.join(current_namespace)]['functions'][
                symbol.name].append(symbol)
        elif isinstance(symbol, Variable):
            symbol_table['_'.join(current_namespace)]['variables'][
                symbol.name].append(symbol)
        elif isinstance(symbol, Argument):
            symbol_table['_'.join(current_namespace)]['arguments'][
                symbol.name].append(symbol)
        else:
            raise ValueError(f"Unknown symbol type: {type(symbol)}")

    @staticmethod
    def check_symbol(symbol_name, symbol_type, namespace=None):
        valid_types = ('arguments', 'functions', 'variables')
        if symbol_type in valid_types:
            if namespace:
                return symbol_table[namespace][symbol_type][symbol_name]
            else:
                sym_instances = []
                for ns in symbol_table.keys():
                    sym_entry = symbol_table[ns][symbol_type][symbol_name]
                    if sym_entry:
                        sym_instances.append((ns, sym_entry))
                return sym_instances
        else:
            raise ValueError(f"Invalid symbol type: {symbol_type}")