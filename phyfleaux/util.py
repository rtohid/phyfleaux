__license__ = """
Copyright (c) 2020 R. Tohid

Distributed under the Boost Software License, Version 1.0. (See accompanying
file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""


class Stack:
    depth = 0

    def __init__(self):
        self.depth = Stack.depth

    def __enter__(self):
        Stack.depth += 1

    def __exit__(self, type, value, traceback):
        Stack.depth -= 1

    @staticmethod
    def get_depth():
        return Stack.depth

