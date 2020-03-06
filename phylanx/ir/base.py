from __future__ import absolute_import

_license__ = """ 
Copyright (c) 2020 R. Tohid

Distributed under the Boost Software License, Version 1.0. (See accompanying
file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""

import ast
import astpretty
import networkx
import pprint

from collections import OrderedDict
from inspect import getsource
from typing import Callable, List


class NameSpace:
    full_name = []

    def __init__(self, namespace=None):
        self.current_space = namespace

    @staticmethod
    def get():
        return '_'.join(NameSpace.full_name)

    def __enter__(self):
        if self.namespace:
            NameSpace.full_name.append(self.current_space)

    def __exit__(self, type, value, traceback):
        if self.namespace:
            NameSpace.full_name.pop()


class IR:
    '''Internal Representation of code.'''

    graph = networkx.DiGraph()

    def __init__(self, fn: Callable):
        '''Construct internal representation.'''
        self.python_fn = fn
        self.python_ast = ast.parse(getsource(fn))

        self.build_node()
        self.register_node()

    def build_node(self):

        # discount the decorator line.
        ast.increment_lineno(self.python_ast, n=-1)

        def _FunctionDef(self, node):
            """class FunctionDef(name, args, body, decorator_list, returns)
            `name` is a raw string of the function name.
            `args` is a arguments node.
            `body` is the list of nodes inside the function.
            `decorator_list` is the list of decorators to be applied, stored
                outermost first (i.e. the first in the list will be applied last).
            `returns` is the return annotation (Python 3 only).
            Notes:
                We ignore decorator_list and returns.
            """

            func = FunctionDef(node.name, NameSpace.get(), node.lineno,
                               node.col_offset)

            with NameSpace(func.name) as ns:
                func.add_arg(self.visit(node.args))
                body = FunctionCall('block', NameSpace.get(),
                                    node.body[0].lineno,
                                    node.body[0].col_offset)

                for statement in node.body:
                    body.add_arg(self.visit(statement))
                func.add_arg(body)
            SymbolTable.add_symbol(func)
            return func

    def register_node(self):
        pass
        # IR.graph.add_node()

    def generate(self, node: ast, parents: list = []):
        node_name = node.__class__.__name__.lower()
        if isinstance(node, list):
            _node = [self.generate(n) for n in node]
            return _node

        handler_name = 'on_' + node_name
        node_hash = hash(node)
        if hasattr(self, handler_name):
            handler = getattr(self, handler_name)
            return handler(node)
        elif isinstance(node, ast.AST):
            _node = OrderedDict()
            _node['node'] = (node_hash, node)
            for key, value in vars(node).items():
                _node[key] = self.generate(value)
            return _node
        else:
            return node

    def __repr__(self):
        return pprint.pformat(self.python_ast)

    def on_module(self, node: ast.AST, parents: List = []):
        return self.generate(node.body[0])
