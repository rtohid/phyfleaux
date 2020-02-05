# Copyright (c) 2020 R. Tohid
#
# Distributed under the Boost Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

from copy import deepcopy

# class Context:
#     '''
#     The environment of the function execution.

#     Dynamically selected and, if necessary, constructed.
#     '''

#     def __init__(self, fn):
#         pass

# class Function(object):
#     '''
#      A function run on a :class:`Context`.
#     '''

#     def __init__(self, fn):

#         self.fn = fn

#     def __hash__(self):
#         return hash(self.fn)

#     def __call__(self, *args, **kwargs):
#         self.args = deepcopy(args)
#         self.kwargs = deepcopy(kwargs)
#         if kwargs:
#             self.fn(*self.args, self.kwargs)
#             return self.fn(*self.args, self.kwargs)
#         else:
#             result = self.fn(*self.args)
#             return result

# class For(Node):
#     def __init__(self, parents=[], _ast=None):
#         super().__init__(parents=parents, _ast=_ast)

#         self.target = _ast.target
#         self.iter = _ast.iter
#         self.body = _ast.body
#         self.orelse = _ast.orelse


class Data(Object):
    def __init__(self, ):
        super().__init__(name, scope, lineno, col_offset)
        self.type = type_

    def __eq__(self, other):
        self_ = (self.name, self.scope, self.lineno, self.col_offset,
                 self.type)
        other_ = (other.name, other.scope, other.lineno, other.col_offset,
                  self.type)
        return self_ == other_


class Array(Data):
    def __init__(self,
                 name,
                 scope,
                 lineno,
                 col_offset,
                 dimension=None,
                 shape=None):
        super().__init__(name, scope, lineno, col_offset)

        if dimension and dimension < 1:
            raise ValueError(
                f"Arrays must have 1 or more dimension(s). {dimension} given.")
        self.dimensionality = dimension

        if shape and not len(shape) == dimension:
            raise ValueError(
                f"Array dimensionality({dimension}) does not match the shape({shape})."
            )
        self.shape = shape

    def __eq__(self, other):
        self_ = (self.name, self.scope, self.lineno, self.col_offset,
                 self.dimensionality, self.shape)
        other_ = (other.name, other.scope, other.lineno, other.col_offset,
                  other.dimensionality, other.shape)
        return self_ == other_


class Function(Object):
    def __init__(self, name, scope, lineno, col_offset, dtype=''):
        super().__init__(name, scope, lineno, col_offset)
        self.args_list = []
        self.dtype = dtype

    def add_arg(self, argument):
        if isinstance(argument, list):
            self.args_list.extend(argument)
        else:
            self.args_list.append(argument)

    def insert_arg(self, argument, position):
        self.args_list.insert(position, argument)

    def prepend_arg(self, argument):
        self.insert_arg(argument, 0)

    def arguments(self):
        return self.args_list

    def __eq__(self, other):
        self_ = (self.name, self.scope, self.lineno, self.col_offset,
                 self.args_list, self.dtype)
        other_ = (other.name, other.scope, other.lineno, other.col_offset,
                  other.args_list, other.dtype)
        return self_ == other_


class FunctionCall(Function):
    pass


class FunctionDef(Function):
    pass