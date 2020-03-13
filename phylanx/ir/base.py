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
from typing import Callable, List

from phylanx.core.function import Function



class IR:
    '''Internal Representation of code.'''

    graph = networkx.DiGraph()

    def __init__(self, fn: Callable) -> None:
        '''Construct internal representation.'''

        self.fn = self.build_node(fn)
        self.register_node()

    def build_node(self, fn: Callable) -> Function:

        self.python_ast = ast.parse(getsource(fn)).body[0]

        # discount the decorator line.
        ast.increment_lineno(self.python_ast, n=-1)

        node = self.python_ast
        func = Function(fn, node.name, NameSpace.get(), node.lineno,
                        node.col_offset)

        with NameSpace(func.name) as ns:
            self.fillout_node(func, self.python_ast)
            print(NameSpace.get())
        print(NameSpace.get())

        return func

    def register_node(self):
        pass
        # IR.graph.add_node()

    def fillout_node(self, fn: Function, node: ast, parents: list = []):
        node_name = node.__class__.__name__.lower()
        if isinstance(node, list):
            _node = [self.fillout_node(fn, n) for n in node]
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
                _node[key] = self.fillout_node(fn, value)
            return _node
        else:
            return node

    def __repr__(self):
        return pprint.pformat(self.python_ast)

    def on_module(self, node: ast.AST, parents: List = []):
        return self.fillout_node(node.body[0])
