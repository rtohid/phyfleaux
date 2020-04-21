__license__ = """
Copyright (c) 2020 R. Tohid

Distributed under the Boost Software License, Version 1.0. (See accompanying
file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""


class ISL:
    pass


class Array:
    def __init__(self, name: str, size: int = None, name_space=None):
        super().__init__()

    def getbuffer(self):
        pass

    def codegen(self):
        pass

    def parallelize(self):
        pass

    def vectorize(self):
        pass


def init(fn_name: str) -> None:
    print(f"init({fn_name})")
    print()


def expr(constant: int) -> None:
    print(f"exp({constant}")
    print()


def var(target_name: str, lower_bound: int, upper_bound: int) -> None:
    print(f"var({target_name}, {lower_bound}, {upper_bound})")
    print()