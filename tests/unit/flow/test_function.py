# Copyright (c) 2020 R. Tohid
#
# Distributed under the Boost Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

raise NotImplementedError('*** this test is broken ***')

# from __future__ import absolute_import

# from phyflow.flow.function import PureFun, deepcopy


# class TestFunction:
#     def test_pure_function(self):
#         @PureFun
#         def fn(a):
#             a[1] = 2 * a[1]
#             return a

#         arg = [1, 2, 3]
#         arg_after_call = deepcopy(arg)
#         fn(arg_after_call)

#         assert arg_after_call == arg
