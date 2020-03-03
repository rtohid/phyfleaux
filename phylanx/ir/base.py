# Copyright (c) 2020 R. Tohid
#
# Distributed under the Boost Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

from __future__ import absolute_import

import ast
import astpretty
import networkx
import pprint

from collections import OrderedDict
from inspect import getsource
from typing import Callable, List

from phylanx.core.data import DataRegistry
from phylanx.core.task import TaskRegistry
from phylanx.ir.nodes import Function


class IRNode:
    def __init__(self, fn):
        self.phy_fn = fn
        self.functions = TaskRegistry(fn)
        self.data = DataRegistry(fn)
        IRGraph.register(self)


class IRGraph:
    graph = networkx.DiGraph()

    def __init__(self, node: IRNode, ast_: ast.AST):
        pass

    @staticmethod
    def register(node: IRNode):
        IRGraph.graph.add_node()

    @staticmethod
    def funcname(parameter_list):
        pass


class IR:
    '''Internal Representation of code.'''
    def __init__(self, fn: Callable, transformation_rules: Callable = None):
        '''Construct internal representation.'''
        self.python_fn = fn
        self.python_ast = ast.parse(getsource(fn))

        ast.increment_lineno(self.python_ast, n=-1)
        astpretty.pprint(self.python_ast.body[0])
        # self.ir_table = IRTable(self.python_fn, self.python_ast)
        # self.ir_graph = IRGraph(self.python_fn, self.python_ast)
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

    def __repr__(self):
        return pprint.pformat(self.ir)

    def on_module(self, node: ast.AST, parents: List = []):
        return self.generate(node.body[0])
