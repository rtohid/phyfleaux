# Copyright (c) 2020 R. Tohid
#
# Distributed under the Boost Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

import ast
from inspect import getsource
from collections import OrderedDict
from typing import Callable

from flow.ir.utils import print_dict



class IR:
    '''Internal Representation of code.'''

    def __init__(self, fn, transformation_rules: Callable = None):
        '''Construct internal representation.'''
        self.python_fn = fn
        self.python_ast = ast.parse(getsource(fn))
        self.ir = self.generate(self.python_ast)

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

    def on_module(self, node, parents=[]):
        return self.generate(node.body[0])


def flow(fn: Callable):
    internal_rep = IR(fn)

    print_dict(internal_rep.ir, _depth=10, _indent=2)
    return internal_rep.python_fn
