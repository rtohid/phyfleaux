# Copyright (c) 2020 R. Tohid
#
# Distributed under the Boost Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

from flow.ir.base import Transformer


def flowfn(fn):
    internal_rep = Transformer(fn)
    print('internal_rep:\n')
    import astpretty
    transed = internal_rep.transform(internal_rep.python_ast.body[0])
    for k, v in transed.items():
        print(transed)
        print()
    # astpretty.pprint(internal_rep.python_ast)
    return internal_rep
