<!-- 
Copyright (c) 2020 R. Tohid

Distributed under the Boost Software License, Version 1.0. (See accompanying
file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt) 
-->


<!--
- target machine, anything in between a local Raspberry Pi to  {a / one or more?} full-blown HPC system{s?} accessed remotely.
```

-->
# phyflow
A program flow optimizer for Phylanx {any other ideas, or maybe better phrasing?}.

---
**Please Note**

This document is my attempt to   
---

## Objective
 
---

Build a flexible runtime-system based on [HPX](https://github.com/stellar-group/hpx.git)- high-performance distributed C++. Provided a (an arbitrary) Python source, and a target machine:
1. Analyze
   * the code
      + domain
      + common (expensive operations)
      + data layout
      + domain
      + ...
   * resources
      + number of nodes, cores, gpus, ...
      + memory hierarchy
      + ...
2. Transform
   * create the IR
      - possibly Phylanx primitives as it's optimize (based on step 1 analyses)
   * generate code
      + [PhySL](https://github.com/STEllAR-GROUP/phylanx/blob/master/examples/interpreter/physl.cpp).
      - , estimate the cost function representing.
   * many other representations of the program is also generated in the process, including the control- and data-flow graphs, Python AST and possibly more in the future.
3. Deploy
   * the PhySL code on the target machine.
   * facilities for configuration, and authentication requirements of the application including access to the target machine.

---

## Methodology
### Outline
#### input
1. Python source with at least one function decorated with `@phyflow` 
2. the specification of the target machine
   + it can explicitly set by the application developer
   + or, collected by phyflow- if need, credentials to access the target machine must be provided by the application developer. 

#### transformation

---
**NOTES**

is triggered when the application hits the first function decorated with `@phyflow`.
1. the automatic detection and analysis of the subsequent phyflow-functions is desirable, or maybe even required.
2. 

---

## Implementation

## Input
As expressed in [Goal](#goal):
* One or more functions decorated with `@phyflow`
   
* Description of the target machine.
  + We assume the more information available, the higher quality of transformation. For this reason, phyflow attempts to collect information at multiple points during the transformation process. Before anything else, phyflow creates the profile of the target machine, including resources available on the system. User can provide this information, but if not, phyflow queries the target machine to collect this information.


## Output



## ToDo
- python interpreter as a primitive
   + In many real application much of the computation happens in a small portion
<!--
* PhySL / One or python source (it could be one or more depending on the target. In case of distributed executions, potentially, each node may have its own unique source.)
-->