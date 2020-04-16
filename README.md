<!-- 
Copyright (c) 2020 R. Tohid

Distributed under the Boost Software License, Version 1.0.(See accompanying
file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt) 
-->

# Phyfleaux: Context-Aware Scheduler for Distributed Programs

## About
Phyfleaux is [Phylanx](github.com/stellar-group/phylanx) scheduler. Given a
Python program, Phyfleaux analyze the code and generate optimized distributed
PhySL. Phyfleaux will also support submission to various science gateways
through [JetLag](https://github.com/STEllAR-GROUP/JetLag.git).

## Problem

### Input
A valid Python program encapsuled in a function which we refer to as *code*.

* Valid implementation of a sequential algorithm.

* Already checked for syntax and grammar.

* Code is accessible through its python AST within the framework.

* Indexing of all possible iteration spaces are known, either:
   * parametrically, e.g., affine iteration spaces, or
   * stored as data, e.g., indirect memory accesses.

* Memory access patten of the sequential implementation, for both data consumed
  by the application and that of iteration spaces are known.
   <!-- * It might be beneficial to assume the initial memory layout in 1-d. -->

#### Description
Given a valid Python code, and specification of the system, generate distributed
PhySL code, where:
* Each PhySL primitive can run on one or more nodes.
* There is a cost function associated to each PhySL function, a.k.a., task.

assign time-step and target node (each could be a range) to each task so the
cost function is minimized.

## Notes
* Cost could be minimizing execution time or maximizing throughput.
* Ideally, the cost function returns outputs of a NN.
* Several common iteration space, e.g., affine, mesh, tree, ... are supported as
  data domains.

