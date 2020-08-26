For more information please see the [source](https://github.com/Tiramisu-Compiler/tiramisu/blob/28868a3dbb204aa89ebd7b0c542c473b9eaa26d2/include/tiramisu/type.h).

#   Expression Types

in [Tiramisu](https://github.com/Tiramisu-Compiler/tiramisu/blob/28868a3dbb204aa89ebd7b0c542c473b9eaa26d2/include/tiramisu/type.h#L14)

    'expr_t'

*    'e_val'   
    - literal value, like 1, 2.4, 10, ...

*    'e_var'   
    - a variable of a primitive type (i.e., an identifier holding one value)

*    'e_sync'  
    - syncs parallel computations. Currently used in the context of GPUs.

*    'e_op'    
    - an operation: add, mul, div, ...

*    'e_none', 
    - undefined expression, i.e., error.

---
---

# Data Types

in [Tiramisu](https://github.com/Tiramisu-Compiler/tiramisu/blob/28868a3dbb204aa89ebd7b0c542c473b9eaa26d2/include/tiramisu/type.h#L27)

    'primitive_t'
    

*   'p_uint8'
*   'p_uint16'
*   'p_uint32'
*   'p_uint64'
*   'p_int8'
*   'p_int16'
*   'p_int32'
*   'p_int64'
*   'p_float32'
*   'p_float64'
*   'p_boolean'
*   'p_async'
*   'p_wait_ptr'
*   'p_void_ptr'

*   'pnone'

---
---

# Argument Types

in [Tiramisu](https://github.com/Tiramisu-Compiler/tiramisu/blob/28868a3dbb204aa89ebd7b0c542c473b9eaa26d2/include/tiramisu/type.h#L134)

    'argument_t'

*   'a_input'
*   'a_output'
*   'a_temporary'

---
---

# Operations Types

in [Tiramisu](https://github.com/Tiramisu-Compiler/tiramisu/blob/28868a3dbb204aa89ebd7b0c542c473b9eaa26d2/include/tiramisu/type.h#L54)

    'op_t'

*   'o_minus'
*   'o_floor'
*   'o_sin'
*   'o_cos'
*   'o_tan'
*   'o_asin'
*   'o_acos'
*   'o_atan'
*   'o_sinh'
*   'o_cosh'
*   'o_tanh'
*   'o_asinh'
*   'o_acosh'
*   'o_atanh'
*   'o_abs'
*   'o_sqrt'
*   'o_expo'
*   'o_log'
*   'o_ceil'
*   'o_round'
*   'o_trunc'
*   'o_allocate'
*   'o_free'
*   'o_cast'
*   'o_address'
*   'o_add'
*   'o_sub'
*   'o_mul'
*   'o_div'
*   'o_mod'
*   'o_logical_and'
*   'o_logical_or'
*   'o_logical_not'
*   'o_eq'
*   'o_ne'
*   'o_le'
*   'o_lt'
*   'o_ge'
*   'o_gt'
*   'o_max'
*   'o_min'
*   'o_right_shift'
*   'o_left_shift'
*   'o_memcpy'
*   'o_select'
*   'o_cond'
*   'o_lerp'
*   'o_call'
*   'o_access'
*   'o_address_of'
*   'o_lin_index'
*   'o_type'
*   'o_dummy'
*   'o_buffer'

---
---

# Ranks

in [Tiramisu](https://github.com/Tiramisu-Compiler/tiramisu/blob/28868a3dbb204aa89ebd7b0c542c473b9eaa26d2/include/tiramisu/type.h#L145)

    'rank_t'

*   'r_sender'
*   'r_receiver'
*   'global'

---
---

# Misc.

*    'function'

*    'expr'
*    'uint8_expr'
*    'int8_expr'
*    'uint16_expr'
*    'int16_expr'
*    'uint32_expr'
*    'int32_expr'
*    'uint64_expr'
*    'int64_expr'
*    'float_expr'
*    'double_expr'

*    'var'
*    'computation'
*    'generator'
*    'buffer'
*    'constant'
*    'input'
*    'Input'
*    'isl_set'
*    'isl_map'
*    'init'
*    'init_physl'
*    'cast'
*    'value_cast'
*    'codegen'
*    'codegen_physl
