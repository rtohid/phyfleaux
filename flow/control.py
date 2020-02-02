# Copyright (c) 2020 R. Tohid
#
# Distributed under the Boost Software License, Version 1.0. (See a copy at
# http://www.boost.org/LICENSE_1_0.txt)

from __future__ import absolute_import

from copy import deepcopy
import ast
import inspect

from networkx import DiGraph

start_location = {
    'lineno': 0,
    'col_offset': 0,
    'end_lineno': 0,
    'end_col_offset': 0
}

end_location = {
    'lineno': -1,
    'col_offset': -1,
    'end_lineno': -1,
    'end_col_offset': -1
}


def get_cfg_start():

    start_node = ast.Expr(value=(ast.Name('__phy_cfg_start',
                                          ctx=ast.Load(),
                                          **start_location)),
                          **start_location)
    return start_node


def get_cfg_end():

    end_node = ast.Expr(value=(ast.Name('__phy_cfg_end',
                                        ctx=ast.Load(),
                                        **end_location)),
                        **end_location)
    return end_node


class ControlNode:
    def __init__(self, cfg, parents=[], _ast=None):
        if type(parents) is not list:
            raise Exception(TypeError,
                            "Expected a list but got: %s" % (type(parents)))
        if parents:
            self.parents = parents
        self.ast_node = _ast


class CFG:
    '''
    Control Flow Graph

    In computer science, a control-flow graph (CFG) is a representation, using
    graph notation, of all paths that might be traversed through a program
    during its execution. https://bit.ly/2t1skKT
    '''

    def __init__(self, fn):
        self.python_code = inspect.getsource(fn)
        self.ast = ast.parse(self.python_code)
        self.graph = None
        self.walk(self.ast)

    def walk(self, node, parents=[]):
        fn_name = "on_%s" % node.__class__.__name__.lower()
        if hasattr(self, fn_name):
            fn = getattr(self, fn_name)
            return fn(node, parents)

    def on_module(self, node, parents):
        self.graph = DiGraph()

        start = ControlNode(self, parents=parents, _ast=get_cfg_start())
        self.graph.add_node(start)

        for child in node.body:
            self.walk(child, [node])

        stop = ControlNode(self, parents=parents, _ast=get_cfg_end())
        self.graph.add_node(stop)

    def on_functiondef(self, node, parents):
        fn_name = node.name
        args = node.args
        returns = node.returns

        block = ControlNode(self, parents=parents, _ast=node)
        self.graph.add_node(block)


class Context:
    '''
    The environment of the function execution.

    Dynamically selected and, if necessary, constructed.
    '''

    def __init__(self, fn):
        pass


class Function(object):
    '''
     A function run on a :class:Context:.
    '''

    def __init__(self, fn):

        self.fn = fn
        self.pst = PST(fn)

    def __call__(self, *args, **kwargs):
        self.args = deepcopy(args)
        self.kwargs = deepcopy(kwargs)
        if kwargs:
            self.fn(*self.args, self.kwargs)
            return self.fn(*self.args, self.kwargs)
        else:
            result = self.fn(*self.args)
            return result

    def env(self):
        '''
        Returns the context of function execution.
        '''
        pass


class SESE:
    """
    Single Entry Single Exit region.

    a SESE region in a graph G is an ordered [list?] of edge pair (a, b) of
    distinct control flow edges 'a', the entry edge, and 'b', the exit edge,
    where
    1. 'a' dominates 'b'
        * ensure that every path from the start into the region passes through
          the region's entry edge, i.e., 'a'.
    2. 'b' postdominates 'a',
        * ensure that every path from the region to the end passes through the
          exit edge, i.e., 'b'.
    3. every cycle containing 'a' also contains 'b' and vice versa.
        * every path from inside the region to a point above 'a' is passes
          through 'b'.
        * everypath from below 'b' to a point inside the region is passes
          through 'a'.
    """
    pass


def phyfn(fn):
    return Function(fn)


class PST(object):
    def __init__(self, fn):
        self.cfg = CFG(fn)
