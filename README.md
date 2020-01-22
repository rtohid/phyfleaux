<!-- 
Copyright (c) 2020 R. Tohid

Distributed under the Boost Software License, Version 1.0.(See accompanying
file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt) 
-->

# phyflow

---
**<span style="color:red">CAUTION</span>**

this document may contain horrific mistakes and assumptions! Please critic, your feedback is very much appreciated.

---

**{note:@commenter}**
---
note (to @rtohid)
: (from) @commenter

## **<span style="color:gray">definitions</span>**

### **<span style="color:gold">state</span>**

* snapshot of a mutable object at a given step of code execution.
* and also {prediction of the next state based on available information.:rtohid}

### **<span style="color:gold">mutable object</span>**

an object with mutable state. At this point we only focus on two kinds of such objects:

1. functions with variable arguments(?) {the input arguments may change- not only between calls, but also during a single call.:rtoihd}
      + {during a single call?? is it possible to change the arguments of the function without changing the function itself?

         - what does it mean/take to change a function?

            * change the computation resource used to execute function
            * change the implementation of the function
            * change the scheduled time of the execution
            * ...
      + is it accurate to say that variable arguments are global objects?:@rtohid}

2. data objects

      * a data object is mutable in a few orthogonal dimensions:

         - ownership- possibly shareable and transferable.
         - address: the location of a data. any given object may have multiple global and local addresses.
         - value: the quantity associated to the object.
         - layout: how to retrieve the value of data from ... memory(?).

#### **<span style="color:skyblue">function</span>**

a relation between two sets.

1. input set: input arguments
2. output set: returned values {/variables:@rtohid})

Each element of the first set (input set) associates to exactly one element of the second set. In our framework we implement :class:Function: as

``` python
# not the best implementation
class Function:
   def __init__(self, fn):
      self.original_fn = fn
      self.input = defaultdict
      self.output = defaultdict
   
   def __call__(self, *args, **kwargs):
      self.input = {'args': args, 'kwargs': kwargs}

      if kwargs:
         return self.original_fn(*self.input['args'], self.input['kwargs'])
      else:
         return self.original_fn(*self.input['args'])

```

The issue with the above implementation is that such function has global artifacts, making it difficult to analyze data and control. In order to avoid this, we make sure that functions only work with copies of data while changes to the original data is made through :class:Data: handles by the runtime system- not the application.

``` python
# better implementation:
class Function:
   def __init__(self, fn):
      self.original_fn = fn
      self.input = defaultdict
      self.output = defaultdict
   
   def __call__(self, *args, **kwargs):
      # making sure the function works with the copy of input not the orginal
      self.input = {'args': deepcopy(args), 'kwargs': deepcopy(kwargs)}

      # for now, we only return the value of the return variable(s). once the implementation of code analysis and transformation is in place we need to make sure to update the input arguments before returning the results
      if kwargs:
         result = self.original_fn(*self.input['args'], self.input['kwargs'])
         # self.update(input_arguments) -> once implementation is in place.
         return result
      else:
         result = self.original_fn(*self.input['args'])
         # self.update(input_arguments) -> once implementation is in place.
         return result

```
<!--
#### **<span style="color:skyblue">data</span>**

``` python
class Data:
   def __init__(self, owner=None, value=None, address=None, layout=None):
      self.owner = owner
      self.address = address
      self.value = value
      self.layout = layout
```

* state

   + frequency 

      - how often the data is accessed.

   + cost 

      - estimated (before requesting), and actual (after retrieving) cost of data access {retrieval:rtohid}- from a given location in the system
   + ... 
   
</br>
</br>

### **<span style="color:gold">flow</span>**

* state of the mutable object

   * snapshot of the latest change to the mutable object
   * 

``` python
class Flow:
   def __init__(self, current_state=None, cost=None, freq=0):
      self.current_state = self.current_state
      self.next_state = None
      self.freq = freq 
      self.cost = cost

dataflow = Flow.Data
costflow = Flow.State
```

</br>
</br>
---

### **<span style="color:green">dataflow</span>**

(compute and) update value -> change the value of the <span style="color:purple">flow</span>

move flow -> change address

</br>
---

### **<span style="color:green">costflow</span>**

update the state of the data

</br>
---

## Implied

---

1. any phyflow function is a <span style="color:purple">flow</span>

---

## Requirements

---

* Each flow object must have a <span style="color:lightblue">cost</span> attribute- cost of:

   + data movement, and/or
   + computation.

---

## ToDo

* python interpreter as a primitive

   + In many real application much of the computation happens in a small portion
-->
