# Copyright (c) 2020 R. Tohid
#
# Distributed under the Boost Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

from copy import deepcopy


class PureFun:
    def __init__(self, fn):
        self.original_fn = fn

    def __call__(self, *args, **kwargs):
        self.args = deepcopy(args)
        self.kwargs = deepcopy(kwargs)
        if kwargs:
            self.original_fn(*self.args, self.kwargs)
            return self.original_fn(*self.args, self.kwargs)
        else:
            result = self.original_fn(*self.args)
            return result