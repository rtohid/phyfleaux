# Copyright (c) 2020 R. Tohid
#
# Distributed under the Boost Software License, Version 1.0. (See accompanying
# # file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)



raise NotImplementedError('*** this tutorial is out of date. ***')


class Flow:
    class Data:
        def __init__(self, value=None, address=None):
            self.value = value
            self.address = address

    class State:
        def __init__(self, frequency=0, cost=0.5):
            self.frequency = frequency
            self.cost = cost

dataflow = Flow.Data
computeflow = Flow.State

dflow = dataflow()
cflow = computeflow()

print(dflow.address, dflow.value)
print(cflow.frequency, cflow.cost)
print('end tutorial')