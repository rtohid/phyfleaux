# Copyright (c) 2019 R. Tohid
#
# Distributed under the Boost Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

import ast

from .nodes import *
from .symbol_table import *
from .utils import get_python_ast, remove_decorator, ast_string


class ArrayTemplate():
    dimension = 0
    _data = None
    defined = False

    @staticmethod
    def get_dim():
        return ArrayTemplate.dimension

    @property
    def data(self):
        return ArrayTemplate._data

    @data.setter
    def data(self, data_):
        ArrayTemplate._data = data_

    def __enter__(self):
        ArrayTemplate.dimension += 1

        if ArrayTemplate.dimension > 3:
            raise NotImplementedError(
                'Rhylanx does not support tensors with more than 3 dimensions.'
            )

    def __exit__(self, type, value, traceback):
        ArrayTemplate.dimension -= 1
        if not ArrayTemplate:
            ArrayTemplate._data = None


class IR:
    def __init__(self, func):
        self.func = remove_decorator(func)
        self.ast = get_python_ast(self.func)
        print(ast_string(self.ast))
        self.ir = self.visit(self.ast)

    def visit(self, node):
        """Calls the correct method, based on the name of the node."""
        node_name = node.__class__.__name__
        return eval('self._%s' % node_name)(node)

    # ##########################################################################
    # def _arg(self, node):
    #     """class arg(arg, annotation)
    #     A single argument in a list.
    #     `arg` is a raw string of the argument name.
    #     `annotation` is its annotation, such as a `Str` or `Name` node.
    #     TODO:
    #         add support to `annotation` which is ignored at this time. Maybe
    #         we can use this to let the user provide the type information!?!
    #     """

    #     arg = Argument(node.arg, current_ns(), node.lineno, node.col_offset)
    #     return arg

    def _arguments(self, node):
        """class arguments(args, vararg, kwonlyargs, kwarg, defaults, kw_defaults)
        The arguments for a function.
        `args` and `kwonlyargs` are lists of arg nodes.
        `vararg` and `kwarg` are single arg nodes, referring to the *args,
        **kwargs parameters.
        `defaults` is a list of default values for arguments that can be passed
        positionally. If there are fewer defaults, they correspond to the last
        n arguments.
        `kw_defaults` is a list of default values for keyword-only arguments. If
        one is None, the corresponding argument is required.
        """

        if node.vararg or node.kwarg:
            raise (Exception("Rhylanx does not support *args and **kwargs"))
        args = []
        for arg in node.args:
            argument = self.visit(arg)
            SymbolTable.add_symbol(argument)
            args.append(argument)
        return args

    def _Assign(self, node):
        """class Assign(targets, value)
        `targets` is a list of nodes which are assigned a value.
        `value` is a single node which gets assigned to `targets`.
        """

        if len(node.targets) > 1:
            raise Exception("Rhylanx does not support chain assignments.")
        if isinstance(node.targets[0], ast.Tuple):
            raise Exception(
                "Rhylanx does not support multi-target assignments.")

        lhs = node.targets[0]

        value = self.visit(node.value)

        target = self.visit(lhs)
        if ArrayTemplate.defined:
            func_name = 'store'
            ArrayTemplate.defined = False
        else:
            func_name = 'define'

        assign = FunctionCall(func_name, NameSpace.get(), lhs.lineno,
                              lhs.col_offset)
        assign.add_arg(target)
        assign.add_arg(value)
        return assign

    # def _Attribute(self, node):
    #     """class Attribute(value, attr, ctx)
    #     `value` is an AST node.
    #     `attr` is a bare string giving the name of the attribute.
    #     """
    #     attr_scope = [node.attr]
    #     current_node = node.value
    #     while isinstance(current_node, ast.Attribute):
    #         attr_scope.insert(0, current_node.attr)
    #         current_node = current_node.value
    #     attr_scope.insert(0, current_node.id)

    #     if isinstance(current_node, ast.Name):
    #         if attr_scope[0] in self.numpy_aliases:
    #             attr_scope[0] = 'numpy'
    #             attr_name = '.'.join(attr_scope)
    #             attr = Node(attr_name, current_ns(), node.lineno,
    #                         node.col_offset)
    #             return attr
    #         else:
    #             attr = '.'.join(attr_scope)
    #             raise NotImplementedError(
    #                 'Rhylanx does not support non-NumPy member functions.'
    #                 'Cannot transform: %s' % attr)

    def _AugAssign(self, node):
        """class AugAssign(target, op, value)"""

        aug_assign = FunctionCall('store', NameSpace.get(), node.lineno,
                                  node.col_offset)
        target = self.visit(node.target)
        value = self.visit(node.value)

        op_name = self.visit(node.op)
        op = FunctionCall(op_name, current_ns(), node.lineno,
                          node.col_offset)

        op.add_arg([target, value])
        aug_assign.add_arg([target, op])

        return aug_assign

    # def _BinOp(self, node):
    #     """class BinOp(left, op, right)"""

    #     op_name = self.visit(node.op)
    #     op = FunctionCall(op_name, current_ns(), node.lineno,
    #                       node.col_offset)
    #     left = self.visit(node.left)
    #     right = self.visit(node.right)
    #     op.add_arg([left, right])
    #     return op

    # def _BoolOp(self, node):
    #     """class BoolOp(left, op, right)"""

    #     if len(node.values) > 2:
    #         raise NotImplementedError("Nested boolean ops is not supported.")

    #     op_name = self.visit(node.op)
    #     op = FunctionCall(op_name, current_ns(), node.lineno,
    #                       node.col_offset)
    #     values = list(map(self.visit, node.values))
    #     op.add_arg(values)

    #     return op

    # def _Call(self, node):
    #     """class Call(func, args, keywords, starargs, kwargs)
    #     `func` is the function, which will often be a Name or Attribute object
    #     of the arguments.
    #     `args` holds a list of the arguments passed by position.
    #     `keywords` holds a list of keyword objects representing arguments passed
    #     by keyword.
    #     TODO(?):
    #         Add support for keywords, starargs, and kwargs
    #     """

    #     func = self.visit(node.func)
    #     func_call = FunctionCall(func.name, current_ns(), func.lineno,
    #                              func.col_offset)
    #     dtype = get_dtype(node)
    #     func_call.set_dtype(dtype)

    #     for arg in node.args:
    #         argument = self.visit(arg)
    #         func_call.add_arg(argument)

    #     return func_call

    # def _Compare(self, node):
    #     """class Compare(left, ops, comparators)
    #     A comparison of two or more values.
    #     `left` is the first value in the comparison
    #     `ops` is the list of operators
    #     `comparators` is the list of values after the first (`left`).
    #     """

    #     op_node = self.visit(node.ops[0])
    #     left = self.visit(node.left)
    #     right = self.visit(node.comparators[0])

    #     op = FunctionCall(op_node, current_ns(), node.lineno,
    #                       node.col_offset)
    #     op.add_arg([left, right])
    #     comparisons = [op]

    #     for i, _ in enumerate(node.comparators[1:]):
    #         op_node = self.visit(node.ops[i + 1])
    #         left = self.visit(node.comparators[i])
    #         right = self.visit(node.comparators[i + 1])

    #         op = FunctionCall(op_node, current_ns(), node.lineno,
    #                           node.col_offset)
    #         op.add_arg([left, right])
    #         comparisons.append(op)

    #     if 1 == len(comparisons):
    #         return comparisons[0]
    #     else:
    #         op = comparisons[-1]
    #         for i in range(len(comparisons), 1, -1):
    #             left = comparisons[i - 2]
    #             right = op
    #             op = FunctionCall('__and', current_ns(), node.lineno,
    #                               node.col_offset)
    #             op.add_arg([left, right])
    #         return op

    # def _Dict(self, node):
    #     res = []
    #     for i in range(len(node.keys)):
    #         key = self.visit(node.keys[i])
    #         val = self.visit(node.values[i])
    #         res += [["list", (key, val)]]
    #     return ["dict", (["list", tuple(res)], )]

    # def _Expr(self, node):
    #     """class Expr(value)
    #     `value` holds one of the other nodes (rules).
    #     """

    #     return self.visit(node.value)

    # def _ExtSlice(self, node):
    #     """class ExtSlice(dims)
    #     Advanced slicing.
    #     `dims` holds a list of `Slice` and `Index` nodes.
    #     """
    #     slicing = list(map(self.visit, node.dims))
    #     return slicing

    # def _For(self, node):
    #     """class For(target, iter, body, orelse)
    #     A for loop.
    #     `target` holds the variable(s) the loop assigns to, as a single Name,
    #         Tuple or List node.
    #     `iter` holds the item to be looped over, again as a single node.
    #     `body` contain lists of nodes to execute.
    #     `orelse` same as `body`, however, those in orelse are executed if the
    #         loop finishes normally, rather than via a break statement.
    #     """

    #     # this lookup table helps us to choose the right mapping function based on the
    #     # type of the iteration space (list, range, or prange).
    #     mapping_function = {
    #         'list': 'for_each',
    #         'slice': 'for_each',
    #         'range': 'for_each',
    #         'prange': 'parallel_map'
    #     }

    #     target = self.visit(node.target)

    #     iteration_space = self.visit(node.iter)

    #     body = FunctionCall('block', current_ns(), node.body[0].lineno,
    #                         node.body[0].col_offset)
    #     for statement in node.body:
    #         body.add_arg(self.visit(statement))

    #     lambda_ = FunctionCall('lambda', current_ns(), node.lineno,
    #                            node.col_offset)
    #     lambda_.add_arg([target, body])

    #     func_name = mapping_function.get(iteration_space.name, 'for_each')
    #     iteration_space.name = iteration_space.name.replace('prange', 'range')
    #     func = FunctionCall(func_name, current_ns(), node.lineno,
    #                         node.col_offset)
    #     func.add_arg([lambda_, iteration_space])

    #     return func
    #     # return [symbol, (target, iteration_space, body, orelse)]

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
            body = FunctionCall('block', NameSpace.get(), node.body[0].lineno,
                                node.body[0].col_offset)

            for statement in node.body:
                body.add_arg(self.visit(statement))
            func.add_arg(body)
        SymbolTable.add_symbol(func)
        return func

        # func = FunctionDef(node.name, self.space, node.lineno,
        #                    node.col_offset)

        # with NameSpace(func.name) as ns:
        #     func.add_arg(self.visit(node.args))
        #     body = FunctionCall('block', current_ns(), node.body[0].lineno,
        #                         node.body[0].col_offset)

        #     for statement in node.body:
        #         body.add_arg(self.visit(statement))
        #     func.add_arg(body)

        #     define = FunctionCall('define', current_ns(), node.lineno,
        #                           node.col_offset)
        #     define.add_arg(func)
        # SymbolTable.add_symbol(func)
        # return define

    # def _If(self, node):
    #     """class IfExp(test, body, orelse)
    #    `test` holds a single node, such as a Compare node.
    #    `body` and `orelse` each hold a list of nodes.
    #    """

    #     if_ = FunctionCall('if', current_ns(), node.lineno, node.col_offset)

    #     test = self.visit(node.test)

    #     body_node = node.body
    #     body_statements = []
    #     for b in body_node:
    #         statement = self.visit(b)
    #         body_statements.append(statement)

    #     body = FunctionCall('block', current_ns(), node.body[0].lineno,
    #                         node.body[0].col_offset)
    #     body.add_arg(body_statements)

    #     orelse_node = node.orelse
    #     if orelse_node:
    #         orelse_statements = []
    #         for o in orelse_node:
    #             statement = self.visit(o)
    #             orelse_statements.append(statement)

    #         orelse = FunctionCall('block', current_ns(),
    #                               node.orelse[0].lineno,
    #                               node.orelse[0].col_offset)
    #         orelse.add_arg(body_statements)
    #         if_.add_arg([test, body, orelse])
    #     else:
    #         if_.add_arg([test, body])

    #     return if_

    def _Index(self, node):
        """class Index(value)"""
        return self.visit(node.value)

    # def _Lambda(self, node):
    #     """class Lambda(args, body)
    #     `body` is a single node.
    #     """

    #     lambda_ = FunctionCall('lambda', current_ns(), node.lineno,
    #                            node.col_offset)
    #     args = self.visit(node.args)
    #     body = self.visit(node.body)
    #     lambda_.add_arg([args, body])

    #     return lambda_

    # def _List(self, node):
    #     """class List(elts, ctx)"""

    #     list_ = FunctionCall('list', current_ns(), node.lineno,
    #                          node.col_offset)
    #     for e in node.elts:
    #         list_.add_arg(self.visit(e))
    #     return list_

    def _Module(self, node):
        return [self.visit(m) for m in node.body]

    def _Name(self, node):
        """class Name(id, ctx)
        A variable name.
        `id` holds the name as a string.
        `ctx` is one of `Load`, `Store`, `Del`.
        """

        dim = ArrayTemplate.dimension
        if dim:
            name = Array(node.id, NameSpace.get(), node.lineno,
                         node.col_offset, node.ctx, dim)
        else:
            name = Variable(node.id, NameSpace.get(), node.lineno,
                            node.col_offset, node.ctx)
        symbol_entry = symbol_table[NameSpace.get()]['variables'][node.id]

        if symbol_entry:
            ArrayTemplate.defined = True

        SymbolTable.add_symbol(name)
        return name

        # def _NameConstant(self, node):
        #     name_constants = {None: 'nil', False: 'false', True: 'true'}
        #     name = Node(name_constants[node.value], current_ns())
        #     return name

        # def _Return(self, node):
        #     """class Return(value)
        #     TODO:
        #         implement return-from primitive (see section Function Return Values on
        #         https://goo.gl/wT6X4P). At this time Rhylanx only supports returns from the
        #         end of the function!
        #     """

        #     if isinstance(node.value, ast.Tuple):
        #         value = FunctionCall('list')
        #         for v in node.value:
        #             value.add_arg(self.visit(v))
        #             SymbolTable.add_symbol(v)

        #     else:
        #         value = self.visit(node.value)
        #         SymbolTable.add_symbol(value)

        #     return value

        # def _Slice(self, node):
        #     """class Slice(lower, upper, step)"""

        #     slice_ = FunctionCall('slice')

        #     lower = self.visit(node.lower)
        #     if lower is None:
        #         slice_.add_arg('nil')

        #     upper = self.visit(node.upper)
        #     if upper is None:
        #         slice_.add_arg('nil')

        #     step = self.visit(node.step)
        #     if step:
        #         slice_.add_arg(step)

        #     return slice_

    def _Subscript(self, node):
        """class Subscript(value, slice, ctx)"""
        with ArrayTemplate() as at:
            subscript = FunctionCall('slice', NameSpace.get(), node.lineno,
                                     node.col_offset)
            subscript.add_arg(self.visit(node.value))
            subscript.add_arg(self.visit(node.slice))

        return subscript

    # def _Tuple(self, node):
    #     """class Tuple(elts, ctx)"""

    #     expr = tuple(map(self.visit, node.elts))
    #     return expr

    #     return subscript

    # def _UnaryOp(self, node):
    #     """class UnaryOp(op, operand)"""

    #     operand = self.visit(node.operand)
    #     if isinstance(node.op, ast.UAdd):
    #         return [(operand, )]

    #     op = get_symbol_info(node, self.visit(node.op))
    #     return [op, (operand, )]

    # def _With(self, node):
    #     if 0 < len(node.items) and type(node.items[0]) == ast.withitem:
    #         withitem = node.items[0]
    #         if type(withitem.context_expr) == ast.Attribute:
    #             attribute = withitem.context_expr
    #             if attribute.attr == "parallel":
    #                 if self.fglobals[attribute.value.
    #                                  id].parallel.is_parallel_block():
    #                     return [
    #                         "parallel_block",
    #                         tuple(map(self.visit, node.body))
    #                     ]
    #         elif type(withitem.context_expr) == ast.Name:
    #             if withitem.context_expr.id == "parallel":
    #                 if self.fglobals["parallel"].is_parallel_block():
    #                     return [
    #                         "parallel_block",
    #                         tuple(map(self.visit, node.body))
    #                     ]
    #     raise Exception("Unsupported use of 'With'")

    # def _While(self, node):
    #     """class While(test, body, orelse)
    #     TODO:
    #     Figure out what `orelse` attribute may contain. From my experience this is always
    #     an empty list!
    #     """

    #     while_ = FunctionCall('while', current_ns(), node.lineno,
    #                           node.col_offset)
    #     test_block = FunctionCall('block', current_ns(), node.test.lineno,
    #                               node.test.col_offset)
    #     test_block.add_arg(self.visit(node.test))
    #     body_block = FunctionCall('block', current_ns(), node.lineno,
    #                               node.col_offset)
    #     body_statements = []
    #     for b in node.body:
    #         statement = self.visit(b)
    #         body_statements.append(statement)
    #     body_block.add_arg(body_statements)
    #     while_.add_arg([test_block, body_block])
    #     return while_

    # # ##########################################################################
    def _Add(self, node):
        return '__add'

    def _And(self, node):
        return '__and'

    def _Div(self, node):
        return '__div'

    def _Eq(self, node):
        return '__eq'

    def _Gt(self, node):
        return '__gt'

    def _GtE(self, node):
        return '__ge'

    def _In(self, node):
        raise Exception("`In` operator is not defined in Rhylanx.")

    def _Is(self, node):
        raise Exception("`Is` operator is not defined in Rhylanx.")

    def _IsNot(self, node):
        raise Exception("`IsNot` operator is not defined in Rhylanx.")

    def _Lt(self, node):
        return '__lt'

    def _LtE(self, node):
        return '__le'

    def _Mult(self, node):
        return '__mul'

    def _Not(self, node):
        return '__not'

    def _NotEq(self, node):
        return '__ne'

    def _NotIn(self, node):
        raise Exception("`NotIn` operator is not defined in Rhylanx.")

    def _Num(self, node):
        """class Num(n)"""
        return node.n

    def _Or(self, node):
        return '__or'

    def _Pass(self, node):
        return 'nil'

    def _Pow(self, node):
        return 'power'

    def _Str(self, node):
        return '"' + node.s + '"'

    def _Sub(self, node):
        return '__sub'

    def _UAdd(self, node):
        return ''

    def _USub(self, node):
        """Leaf node, returning raw string of the 'negative' operation."""

        return '__minus'