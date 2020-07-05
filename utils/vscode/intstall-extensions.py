#!/usr/bin/python3.8
__license__ = """
Copyright (c) 2020 R. Tohid

Distributed under the Boost Software License, Version 1.0. (See accompanying
file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""

__doc__ = """Installs all extensions in `recommended-vscode-extensions.txt`
file found in the current directory (`phyfleaux/utils/vscode`)."""

import subprocess

with open('recommended-vscode-extensions.txt', 'r') as extensions:
    for extension in extensions:
        installation = subprocess.call(
            ['code', '--install-extension', extension])
