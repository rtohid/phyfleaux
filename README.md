<!-- 
Copyright (c) 2020 R. Tohid

Distributed under the Boost Software License, Version 1.0.(See accompanying
file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt) 
-->

# phyflow

**{note->rtohid}**
---

## definitions

---

---

### **<span style="color:green">Flow</span>**

<!-- 
metaobject
base class 
-->

snapshot of the latest change to data and its state:

* data

   + value
   + location

* state

   + frequency 
   + estimated cost <!-- callback cost- function --> 
   + ... 
</br>
</br>

``` python
class Flow:
    class Data:
        def __init__(self, value=None, address=None):
            self.value = value
            self.address = address

    class State:
        def __init__(self, freq=0, cost=0.5):
            self.freq = freq # how many times 
            self.cost = cost

dataflow = Flow.Data
computeflow = Flow.State
```

</br>
---

### **<span style="color:green">dataflow</span>**

(compute and) update value -> change the value of the <span style="color:purple">flow</span>

move flow -> change address

</br>
---

### **<span style="color:green">computeflow</span>**

update the state of the data

</br>
---

## Implied

---

1. any phyflow function is a <span style="color:purple">flow</span>

---

## Requirements

---

* each flow object must have a <span style="color:lightblue">cost</span> attribute- cost of:

   + data movement, and/or
   + computation.

---

## ToDo

* python interpreter as a primitive

   + In many real application much of the computation happens in a small portion

