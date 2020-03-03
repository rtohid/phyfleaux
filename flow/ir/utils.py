# Copyright (c) 2020 R. Tohid
#
# Distributed under the Boost Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

import pprint


def print_dict(dict, _depth=1, _indent=4):
    pprint.PrettyPrinter(depth=_depth, indent=_indent).pprint(dict)