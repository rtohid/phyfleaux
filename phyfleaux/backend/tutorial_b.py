#  Copyright (c) 2019-2020 Christopher Taylor
#
#  Distributed under the Boost Software License, Version 1.0. (See accompanying
#  file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
#
from pytiramisu import init_physl, var, expr, constant, function, primitive_t, argument_t, buffer, computation, codegen_physl, p_uint8, a_output, a_input, input

if __name__ == "__main__":

    '''
    '''

    NN = 10
    MM = 20

    init_physl("tut_02")

    N = constant("N", expr(NN))
    M = constant("M", expr(MM)) # expr needs to wrap all integers going into these constructors

    A = input("A", list(["i", "j"]), list([expr(NN), expr(MM)]), p_uint8)

    i = var("i", expr(0), N)
    j = var("j", expr(0), M)

    output = computation("output", list([i, j]), A(i, j) + cast(p_uint8, i) + uint8(4))

    i0 = var("i0")
    i1 = var("i1")
    j0 = var("j0")
    j1 = var("j1")

    output.tile(i, j, expr(2), expr(2), i0, j0, i1, j1)
    output.parallelize(i0)

    b_A = buffer("b_A", list([expr(NN), expr(MM)]), p_uint8, a_input)
    b_output = buffer("b_output", list([expr(NN), expr(MM)]), p_uint8, a_output)

    A.store_in(b_A)
    output.store_in(b_output)

    physl_str = codegen_physl(buffers)
    print(physl_str)
