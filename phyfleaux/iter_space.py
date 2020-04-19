__license__ = """
Copyright (c) 2020 R. Tohid

Distributed under the Boost Software License, Version 1.0. (See accompanying
file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""

from typing import Callable
from ast import AST
import ast
from collections import OrderedDict, defaultdict

# from phyfleaux.api.plugins.tiramisu import argument_t, primitive_t
# from phyfleaux.api.plugins.tiramisu import buffer, computation, expr, init, var
# from phyfleaux.api.plugins.tiramisu import codegen
from phyfleaux.api.plugins.tiramisu import init
from phyfleaux.task import Task
from phyfleaux.util import Stack


class Polytope(Task):
    def __init__(self, fn: Callable) -> None:
        """Representation of the function in affine space.
    
        :arg fn: python function.

        related resources:
        ------------------
        https://polyhedral.info/

        https://en.wikipedia.org/wiki/Polytope_model
        https://en.wikipedia.org/wiki/Affine_space
        """

        Task.__init__(self, fn)

        # maps hashes of nodes in :function:fn`'s Python AST to their copy.
        self.visit(self.tree)

    """
    init("foo")
    srange_expr = expr(0) 
    erange_expr = expr(100) 
    i = var("i", srange_expr, erange_expr)
    j = var("j", srange_expr, erange_expr)
    iter_range = [i, j]
    crange_expr = expr(0)
    C = computation(iter_range, crange_expr)
    C.parallelize(i)
    C.vectorize(j, 4)

    #buffer_ranges = [ erange_expr, erange_expr ]
    #b_C = buffer("b_C", buffer_ranges, primitive_t.p_int32, argument_t.a_output)
    #C.codegen(b_C, "generated_code.o");
    buffers = [ C.get_buffer(), ]
    codegen(buffers, "generated_code.c")
    """

    def visit_For(self, node: ast.For) -> None:
        if isinstance(node.iter, ast.Call) and 'range' == node.iter.func.id:
            bounds = []
            for arg in node.iter.args:
                try:
                    if arg.id in self.args:
                        bounds.append(arg.id)
                except AttributeError:
                    if isinstance(arg, ast.Constant):
                        bounds.append(arg.n)
                except AttributeError:
                    raise AttributeError(
                        f"Expected '<class ast.Name>' received {type(arg)}")
            if 1 == len(bounds):
                bounds = [0] + bounds
            print(bounds)
            
        if isinstance(node.iter, ast.List):
            raise NotImplementedError(
                "List as an iteration space is not supported.)")

        lower = bounds[0]
        upper = bounds[1]
        print(f"(lower: {lower}, upper: {upper})")
        
        try:
            id_ = node.target.id
            print(node.target.id.__name__)
        except:
            NotImplementedError
        
        from astpretty import pprint
        pprint(node)
        # print(self.ir[hash(node)]['tiramisu'].body)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        init(node.name)
        for arg in node.args.args:
            self.visit(arg)

        for statement in node.body:
            self.visit(statement)

    def visit_Subscript(self, node: ast.Subscript) -> None:
        print("hello sub", node.value.id)

    # def __iter__(self):
    #     return self
