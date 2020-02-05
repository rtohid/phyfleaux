# Copyright (c) 2020 R. Tohid
#
# Distributed under the Boost Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

import ast
from inspect import getsource


class Transformer:
    '''Transform code (in AST format) based on given transformation rules.'''

    def __init__(self, fn, transformation=None):
        self.python_fn = fn
        self.python_ast = ast.parse(getsource(fn))

        if transformation:
            self.transform = transformation
        else:
            self.transform = self._transform

    def _transform(self, node, parents=[]):
        fn_name = "on_%s" % node.__class__.__name__.lower()
        if hasattr(self, fn_name):
            fn = getattr(self, fn_name)
            return fn(node, parents)

################################################################################

    def on_constant(self, node, parents):
        return {'value': node.value}

    def on_formattedvalue(self, node, parents):
        value = self.transform(node.value)
        conversion = self.transform(node.conversion)
        format_spec = None
        if node.format_spec:
            format_spec = self.transform(node.format_spec)

        return {
            'value': value,
            'conversion': conversion,
            'format_spec': format_spec
        }

    def on_joinedstr(self, node, parents):

        return {'values': [self.transform(v) for v in node.values]}

    def on_list(self, node, parents):
        elements = [self.transform(e) for e in node.elts]
        context = node.ctx

        return {'elements': elements, 'context': context}

    def on_tuple(self, node, parents):
        elements = (self.transform(e) for e in node.elts)
        context = node.ctx

        return {'elements': elements, 'context': context}

    def on_set(self, node, parents):
        return {'elts': [self.transform(e) for e in node.elts]}

    def on_dict(self, node, parents):
        keys = (self.transform(k) for k in node.keys)
        values = (self.transform(v) for v in node.keys)

        return {'keys': keys, 'values': values}
        # return zip(keys, values)

    def on_name(self, node, parents):
        id = node.id
        context = node.ctx

        return (id, context)

    def on_load(self, node, parents):
        pass

    def on_store(self, node, parents):
        pass

    def on_del(self, node, parents):
        pass

    def on_starred(self, node, parents):
        value = self.transform(node.value)
        context = node.ctx

        return {'value': value, 'context': context}

    def on_expr(self, node, parents):
        return self.transform(node.value)

    def on_unaryop(self, node, parents):
        op = self.transform(node.op)
        operand = self.transform(node.operand)

        return {'op': op, 'operand': operand}

    def on_uadd(self, node, parents):
        class UnaryAdd:
            pass

        return UnaryAdd

    def on_usub(self, node, parents):
        class UnarySub:
            pass

        return UnarySub

    def on_not(self, node, parents):
        class Not:
            pass

        return Not

    def on_invert(self, node, parents):
        class Invert:
            pass

        return Invert

    def on_binop(self, node, parents):
        left = self.transform(node.left)
        right = self.transform(node.right)
        op = self.transform(node.op)

        return {'left': left, 'right': right, 'op': op}

    def on_add(self, node, parents):
        class Add:
            pass

        return Add

    def on_sub(self, node, parents):
        class Sub:
            pass

        return Sub

    def on_mult(self, node, parents):
        class Mult:
            pass

        return Mult

    def on_div(self, node, parents):
        class Div:
            pass

        return Div

    def on_floordiv(self, node, parents):
        class FloorDiv:
            pass

        return FloorDiv

    def on_mod(self, node, parents):
        class Mod:
            pass

        return Mod

    def on_pow(self, node, parents):
        class Pow:
            pass

        return Pow

    def on_lshift(self, node, parents):
        class LShift:
            pass

        return LShift

    def on_rshift(self, node, parents):
        class RShift:
            pass

        return RShift

    def on_bitor(self, node, parents):
        class BitOr:
            pass

        return BitOr

    def on_bitxor(self, node, parents):
        class BitXor:
            pass

        return BitXor

    def on_bitand(self, node, parents):
        class BitAnd:
            pass

        return BitAnd

    def on_matmult(self, node, parents):
        class MatMult:
            pass

        return MatMult

    def on_boolop(self, node, parents):
        values = [self.transform(v) for v in node.vlues]
        op = self.transform(node.op)
        return {'values': values, 'op': op}

    def on_and(self, node, parents):
        class And(object):
            pass

        return And

    def on_or(self, node, parents):
        class Or(object):
            pass

        return Or

    def on_compare(self, node, parenets):
        left = node.left
        ops = [self.transform(op) for op in node.ops]
        comparators = [node.transform(comp) for comp in node.comparators]

        return {'left': left, 'ops': ops, 'comparators': comparators}

    def on_eq(self, node, parents):
        class Eq:
            pass

        return Eq

    def on_noteq(self, node, parents):
        class NotEq:
            pass

        return NotEq

    def on_lt(self, node, parents):
        class Lt:
            pass

        return Lt

    def on_lte(self, node, parents):
        class LtE:
            pass

    def on_gt(self, node, parents):
        class Gt:
            pass

        return Gt

    def on_gte(self, node, parents):
        class GtE:
            pass

        return GtE

    def on_is(self, node, parents):
        class Is:
            pass

        return Is

    def on_isnot(self, node, parents):
        class IsNot:
            pass

        return IsNot

    def on_in(self, node, parents):
        class In:
            pass

        return In

    def on_notin(self, node, parents):
        class NotIn:
            pass

        return NotIn

    def on_call(self, node, parents):
        func = self.transform(node.func)
        # here we need to update the function's entry
        args = [self.transform(arg) for arg in node.args]
        keywords = [self.transform(keyword) for keyword in node.keywords]

        return {'func': func, 'args': args, 'keywords': keywords}

    def on_keyword(self, node, parents):
        arg = self.transform(node.arg)
        value = self.transform(node.value)

        return {'arg': arg, 'value': value}

    def on_ifexp(self, node, parents):
        test = self.transform(node.test)
        body = self.transform(node.body)
        orelse = self.transform(node.orelse)

        return {'test': test, 'body': body, 'orelse': orelse}

    def on_attribute(self, node, parents):
        value = self.transform(node.value)
        attr = node.attr
        context = self.transform(node.ctx)

        return {'value': value, 'attr': attr, 'cxt': context}

    def on_subscript(self, node, parents):
        value = self.transform(node.value)
        slice_ = self.transform(node.slice)
        context = self.transform(node.ctx)

        return {'value': value, 'slice': slice_, 'cxt': context}

    def on_index(self, node, parents):
        value = self.transform(node.value)

        return {'value': value}

    def on_slice(self, node, parents):
        lower = self.transform(node.lower)
        upper = self.transform(node.upper)
        step = self.transform(node.step)

        return {'lower': lower, 'upper': upper, 'step': step}

    def on_extslice(self, node, parents):
        dims = [self.transform(dim) for dim in node.dims]

        return {'dims': dims}

    def on_listcomp(self, node, parents):
        elt = self.transform(node.elt)
        generators = [
            self.transform(generator) for generator in node.generators
        ]

        return {'elt': elt, 'generatore': generators}

    def on_setcomp(self, node, parents):
        elt = self.transform(node.elt)
        generators = [
            self.transform(generator) for generator in node.generators
        ]

        return {'elt': elt, 'generatore': generators}

    def on_generatorexp(self, node, parents):
        elt = self.transform(node.elt)
        generators = [
            self.transform(generator) for generator in node.generators
        ]

        return {'elt': elt, 'generatore': generators}

    def on_dictcomp(self, node, parents):
        key = self.transform(node.key)
        value = self.transform(node.value)
        generators = [
            self.transform(generator) for generator in node.generators
        ]

        return {'key': key, 'value': value, 'generatore': generators}

    def on_comprehension(self, node, parents):
        target = self.transform(node.target)
        iter_ = self.transform(node.iter)
        ifs = [self.transform(if_) for if_ in node.ifs]
        is_async = node.is_async

        return {
            'target': target,
            'iter': iter_,
            'ifs': ifs,
            'is_async': is_async
        }

    def on_assign(self, node, parents):
        targets = [self.transform(target) for target in node.targets]
        value = self.transform(node.value)

        return {'targets': targets, 'value': value}

    def on_annassign(self, node, parents):
        target = self.transform(node.target)
        annotation = self.annotation(node.annotation)
        value = self.transform(node.value)
        simple = node.simple

        return {
            'target': target,
            'annotation': annotation,
            'value': value,
            'simple': simple
        }

    def on_augassign(self, node, parents):
        target = self.transform(node.target)
        op = self.transform(node.op)
        value = self.transform(node.value)

        return {'target': target, 'op': op, 'value': value}

    def on_raise(self, nodem, parents):
        exc = self.transform(node.exc)
        cause = None
        if node.cause:
            cause = self.transform(node.cause)

        return {'exc': exc, 'cause': cause}

    def on_assert(self, node, parents):
        test = self.transform(node.test)
        msg = self.transform(node.msg)

        return {'test': test, 'msg': msg}

    def on_delete(self, node, parents):
        return {'targets': [self.transform(target) for target in node.targets]}

    def on_pass(self, node, parents):
        class Pass:
            pass

        return Pass

    def on_import(self, node, parents):
        raise NotImplementedError('Import is not supported at this point.')

    def on_importfrom(self, node, parents):
        raise NotImplementedError('ImportFrom is not supported at this point.')

    def on_alias(self, node, parents):
        raise NotImplementedError('Alias is not supported at this point.')

    def on_if(self, node, parents):
        test = self.transform(node.test)
        body = [self.transform(b) for b in node.body]
        orelse = [self.transform(o) for o in node.orelse]

        return {'test': test, 'body': body, 'orelse': orelse}

    def on_for(self, node, parents):
        target = self.transform(node.target)
        iter = self.transform(node.iter)
        body = [self.transform(b) for b in node.body]
        orelse = [self.transform(o) for o in node.orelse]

        return {'target': target, 'iter': iter, 'body': body, 'orelse': orelse}

    def on_while(self, node, parents):
        test = self.transform(node.test)
        body = [self.transform(b) for b in node.body]
        orelse = [self.transform(o) for o in node.orelse]

        return {'test': test, 'body': body, 'orelse': orelse}

    def on_break(self, node, parents):
        class Break:
            pass

        return Break

    def on_continue(self, node, parents):
        class Continue:
            pass

        return Continue

    def on_try(self, node, parents):
        raise NotImplementedError('Try is not supported at this point.')

    def on_tryfinally(self, node, parents):
        raise NotImplementedError('TryFinally is not supported at this point.')

    def on_tryexcept(self, node, parents):
        raise NotImplementedError('TryExcept is not supported at this point.')

    def on_excepthandler(self, node, parents):
        raise NotImplementedError(
            'ExceptHandler is not supported at this point.')

    def on_with(self, node, parents):
        raise NotImplementedError('With is not supported at this point.')

    def on_withitem(self, node, parents):
        raise NotImplementedError('WithItem is not supported at this point.')

    def on_functiondef(self, node, parents):
        name = node.name
        args = self.transform(node.args)
        for b in node.body:
            print(b)
        body = [self.transform(b) for b in node.body]
        if len(node.decorator_list) > 1:
            raise NotImplementedError(
                'decorated functions are not supported yet.')

        return {
            'name': name,
            'args': args,
            'body': body,
            'decorator_list': None
        }

################################################################################

    def on_module(self, node, parents):
        '''Ignored.'''
        pass


# import ast, astpretty

# ast_ = ast.parse('def foo(a, b): return a + b')
# astpretty.pprint(ast_)