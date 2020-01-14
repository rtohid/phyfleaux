# Copyright (c) 2020 R. Tohid
#
# Distributed under the Boost Software License, Version 1.0. (See a copy at
# http://www.boost.org/LICENSE_1_0.txt)

# Adapted from: https://bit.ly/2ussRWJ

from __future__ import absolute_import
import ast, re, inspect

from graphviz import Source, Graph, Digraph
import astor


class Register:
    def __init__(self):
        self.idx = 0
        self.content = {}

    def increment_idx(self):
        idx = self.idx
        self.idx += 1
        return idx

    def register_node(self, node):
        node.reg_idx = self.increment_idx()
        self.content[node.reg_idx] = node

    def reset(self):
        self.idx = 0
        self.content = {}

    def to_dict(self):
        return dict(self.content)


def init_cfg():
    _start_location = {
        'lineno': 0,
        'col_offset': 0,
        'end_lineno': 0,
        'end_col_offset': 0
    }

    _stop_location = {
        'lineno': -1,
        'col_offset': -1,
        'end_lineno': -1,
        'end_col_offset': -1
    }

    _start_node = ast.Expr(value=(ast.Name('__phy_cfg_start',
                                           ctx=ast.Load(),
                                           **_start_location)),
                           **_start_location)
    _stop_node = ast.Expr(value=(ast.Name('__phy__cfg_stop',
                                          ctx=ast.Load(),
                                          **_stop_location)),
                          **_stop_location)
    return _start_node, _stop_node


class Node(dict):
    def __init__(self, parents=[], _ast=None, cfg):
        if type(parents) is not list:
            raise Exception(TypeError,
                            "Expected a list but got: %s" % (type(parents)))
        cfg.register_node(self)
        self.parents = parents
        self.ast_node = ast
        self.update_children(parents)
        self.children = []
        self.calls = []

    @property
    def id(self):
        return str(self.reg_idx)

    @id.setter
    def id(self, reg_idx):
        self.reg_idx = reg_idx

    def update_children(self, parents):
        for p in parents:
            p.add_child(self)

    def add_child(self, c):
        if c not in self.children:
            self.children.append(c)

    def lineno(self):
        return self.ast_node.lineno if hasattr(self.ast_node, 'lineno') else 0

    def __str__(self):
        return "id:%d line[%d] parents: %s : %s" % (
            self.reg_idx, self.lineno(), str([p.reg_idx for p in self.parents
                                              ]), self.source())

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.reg_idx == other.reg_idx

    def __neq__(self, other):
        return self.reg_idx != other.reg_idx

    def set_parents(self, p):
        self.parents = p

    def add_parent(self, p):
        if p not in self.parents:
            self.parents.append(p)

    def add_parents(self, ps):
        for p in ps:
            self.add_parent(p)

    def add_calls(self, func):
        self.calls.append(func)

    def source(self):
        return astor.to_source(self.ast_node).strip()

    def to_json(self):
        return {
            'id': self.reg_idx,
            'parents': [p.reg_idx for p in self.parents],
            'children': [c.reg_idx for c in self.children],
            'calls': self.calls,
            'at': self.lineno(),
            'ast': self.source()
        }


class CFG:
    def __init__(self, fn):
        self.fn = fn
        self.python_code = inspect.getsource(fn)
        self.functions = {}
        self.functions_node = {}

    def build(self):
        _start_node, _stop_node = init_cfg()
        source = Node(parents=[], ast=_start_node)

        _ast = ast.parse(self.python_code)
        _cfg_nodes = self.walk(_ast, [source])
        sink = Node(parents=_cfg_nodes, ast=_stop_node)
        # self.last_node = Node(parents=nodes,
        #                       ast=ast.parse('__phy_stop').body[0])
        # ast.copy_location(self.last_node.ast_node, self.source.ast_node)
        # self.update_children()
        # self.update_functions()
        # self.link_functions()
        self.cfg = _cfg
        # if remove_start_stop:
        #     cache = {
        #         k: cache[k]
        #         for k in cache
        #         if cache[k].source() not in {'__phy_start', '__phy_stop'}
        #     }

    def parse(self, src):
        return ast.parse(src)

    def walk(self, node, myparents):
        fname = "on_%s" % node.__class__.__name__.lower()
        if hasattr(self, fname):
            fn = getattr(self, fname)
            v = fn(node, myparents)
            return v
        else:
            return myparents


class PhyCFG(CFG):
    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)


def phycfg(fn):
    cfg = PhyCFG(fn)
    cfg.build()
    return cfg