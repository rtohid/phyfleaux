//  Copyright (c) 2019-2020 Christopher Taylor
//
//  Distributed under the Boost Software License, Version 1.0. (See accompanying
//  file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
//
#include <memory>

#include <isl/ast_type.h>

#include "physl_tiramisu.hpp"

#include <tiramisu/debug.h>
#include <tiramisu/expr.h>
#include <tiramisu/type.h>
#include <tiramisu/computation_graph.h>
#include <tiramisu/core.h>

namespace physl { namespace tiramisu {

using namespace tiramisu;

// taken from `tiramisu_codegen_halide.cpp:2549`
//
//static inline isl_ast_node *for_code_generator_after_for(isl_ast_node *node, isl_ast_build *build, void *user) {
//    return node;
//}

//int codegen(const std::vector< std::shared_ptr<buffer> > &arguments, const bool gen_cuda_stmt, std::string & physlstr)
//
int codegen(std::vector< ::tiramisu::buffer > &arguments, std::string & physlstr)
{

    std::vector< ::tiramisu::buffer * > bufs{};

    if(arguments.size()) {
        bufs.reserve(arguments.size());

        for(auto & arg : arguments) {
            //bufs.push_back(&arg);
            bufs.emplace_back( std::addressof(arg) );
        }
    }

    { // begin scope

        PhyslFunction * fct = static_cast<PhyslFunction *>(::tiramisu::global::get_implicit_function());
        /*
        if(gen_cuda_stmt)
        {
            if(!fct.get_mapping().empty())
            {
                tiramisu::computation* c1 = fct->get_first_cpt();
                tiramisu::computation* c2 = fct->get_last_cpt();
                Automatic_communication(c1,c2);
            }
            else {
                //DEBUG(3, ::tiramisu::str_dump("You must specify the corresponding CPU buffer to each GPU buffer else you should do the communication manually"));
            }
        }
        */

        fct->generate_code(bufs, physlstr);

        /*
        if (gen_cuda_stmt) {
            fct.gen_cuda_stmt();
        }

        fct.gen_halide_stmt();
        fct->gen_halide_obj(obj_filename);
        */

    } // end scope

    return 1;

} // end codegen

// https://github.com/Tiramisu-Compiler/tiramisu/blob/62e1513d1580aa7ba304d3ebe22f631dfe30814d/src/tiramisu_codegen_halide.cpp
//
void PhyslFunction::gen_physl_from_tiramisu_expr(const ::tiramisu::expr & tiramisu_expr, std::string & ret_result) {

    std::stringstream result{};

    if (tiramisu_expr.get_expr_type() == ::tiramisu::e_val)
    {
        if (tiramisu_expr.get_data_type() == ::tiramisu::p_uint8)
        {
            result << tiramisu_expr.get_uint8_value();
        }
        else if (tiramisu_expr.get_data_type() == ::tiramisu::p_int8)
        {
            result << tiramisu_expr.get_int8_value();
        }
        else if (tiramisu_expr.get_data_type() == ::tiramisu::p_uint16)
        {
            result << tiramisu_expr.get_uint16_value();
        }
        else if (tiramisu_expr.get_data_type() == ::tiramisu::p_int16)
        {
            result << tiramisu_expr.get_int16_value();
        }
        else if (tiramisu_expr.get_data_type() == ::tiramisu::p_uint32)
        {
            result << tiramisu_expr.get_uint32_value();
        }
        else if (tiramisu_expr.get_data_type() == ::tiramisu::p_int32)
        {
            result << tiramisu_expr.get_int32_value();
        }
        else if (tiramisu_expr.get_data_type() == ::tiramisu::p_uint64)
        {
            result << tiramisu_expr.get_uint64_value();
        }
        else if (tiramisu_expr.get_data_type() == ::tiramisu::p_int64)
        {
            result << tiramisu_expr.get_int64_value();
        }
        else if (tiramisu_expr.get_data_type() == ::tiramisu::p_float32)
        {
            result << tiramisu_expr.get_float32_value();
        }
        else if (tiramisu_expr.get_data_type() == ::tiramisu::p_float64)
        {
            result << tiramisu_expr.get_float64_value();
        }
    }
    else if (tiramisu_expr.get_expr_type() == ::tiramisu::e_op)
    {
        //Halide::Expr op0, op1, op2;
        std::stringstream op0{}, op1{}, op2{};

        if (tiramisu_expr.get_n_arg() > 0)
        {
            ::tiramisu::expr expr0 = tiramisu_expr.get_operand(0);
            op0 << gen_physl_from_tiramisu_expr(fct, index_expr, expr0, comp);
        }

        if (tiramisu_expr.get_n_arg() > 1)
        {
            ::tiramisu::expr expr1 = tiramisu_expr.get_operand(1);
            op1 << gen_physl_from_tiramisu_expr(fct, index_expr, expr1, comp);
        }

        if (tiramisu_expr.get_n_arg() > 2)
        {
            ::tiramisu::expr expr2 = tiramisu_expr.get_operand(2);
            op2 << gen_physl_from_tiramisu_expr(fct, index_expr, expr2, comp);
        }

        switch (tiramisu_expr.get_op_type())
        {
            case ::tiramisu::o_logical_and:
                //result = Halide::Internal::And::make(op0, op1);
                result << op0.str() + " && " + op1.str();
                //DEBUG(10, ::tiramisu::str_dump("op type: o_logical_and"));
                break;
            case ::tiramisu::o_logical_or:
                //result = Halide::Internal::Or::make(op0, op1);
                result << op0.str() + " || " + op1.str();
                //DEBUG(10, ::tiramisu::str_dump("op type: o_logical_or"));
                break;
            case ::tiramisu::o_max:
                //result = Halide::Internal::Max::make2(op0, op1, true);
		result << "max(" + op0.str() + ", " + op1.str() + ")";
                //DEBUG(10, ::tiramisu::str_dump("op type: o_max"));
                break;
            case ::tiramisu::o_min:
                //result = Halide::Internal::Min::make2(op0, op1, true);
		result << "min(" + op0.str() + ", " + op1.str() + ")";
                //DEBUG(10, ::tiramisu::str_dump("op type: o_min"));
                break;
            case ::tiramisu::o_minus:
                //result = Halide::Internal::Sub::make(Halide::cast(op0.type(), Halide::Expr(0)), op0, true);
		result << "-" + op0.str();
                //DEBUG(10, ::tiramisu::str_dump("op type: o_minus"));
                break;
            case ::tiramisu::o_add:
                //result = Halide::Internal::Add::make(op0, op1, true);
		result << op0.str() + " + " + op1.str();
                //DEBUG(10, ::tiramisu::str_dump("op type: o_add"));
                break;
            case ::tiramisu::o_sub:
                //result = Halide::Internal::Sub::make(op0, op1, true);
		result << op0.str() + " - " + op1.str();
                //DEBUG(10, ::tiramisu::str_dump("op type: o_sub"));
                break;
            case ::tiramisu::o_mul:
                //result = Halide::Internal::Mul::make(op0, op1, true);
                result << op0.str() + " * " + op1.str(); 
                //DEBUG(10, ::tiramisu::str_dump("op type: o_mul"));
                break;
            case ::tiramisu::o_div:
                //result = Halide::Internal::Div::make(op0, op1, true);
                result << op0.str() + " / " + op1.str(); 
                //DEBUG(10, ::tiramisu::str_dump("op type: o_div"));
                break;
            case ::tiramisu::o_mod:
                //result = Halide::Internal::Mod::make(op0, op1, true);
                result << op0.str() + " % " + op1.str(); 
                //DEBUG(10, ::tiramisu::str_dump("op type: o_mod"));
                break;
/*
            case ::tiramisu::o_select:
                result = Halide::Internal::Select::make(op0, op1, op2);
                //DEBUG(10, ::tiramisu::str_dump("op type: o_select"));
                break;
            case ::tiramisu::o_lerp:
                result = Halide::lerp(op0, op1, op2);
                //DEBUG(10, ::tiramisu::str_dump("op type: lerp"));
                break;
            case ::tiramisu::o_cond:
                ERROR("Code generation for o_cond is not supported yet.", true);
                break;
*/
            case ::tiramisu::o_le:
                //result = Halide::Internal::LE::make(op0, op1, true);
                result << op0.str() + " <= " + op1.str();
                //DEBUG(10, ::tiramisu::str_dump("op type: o_le"));
                break;
            case ::tiramisu::o_lt:
                //result = Halide::Internal::LT::make(op0, op1, true);
                result << op0.str() + " < " + op1.str();
                //DEBUG(10, ::tiramisu::str_dump("op type: o_lt"));
                break;
            case ::tiramisu::o_ge:
                //result = Halide::Internal::GE::make(op0, op1, true);
                result << op0.str() + " >= " + op1.str();
                //DEBUG(10, ::tiramisu::str_dump("op type: o_ge"));
                break;
            case ::tiramisu::o_gt:
                //result = Halide::Internal::GT::make(op0, op1, true);
                result << op0.str() + " > " + op1.str();
                //DEBUG(10, ::tiramisu::str_dump("op type: o_gt"));
                break;
            case ::tiramisu::o_logical_not:
                //result = Halide::Internal::Not::make(op0);
                result << "!" + op0.str();
                //DEBUG(10, ::tiramisu::str_dump("op type: o_not"));
                break;
            case ::tiramisu::o_eq:
                //result = Halide::Internal::EQ::make(op0, op1, true);
                result << op0.str() + " == " + op1.str();
                //DEBUG(10, ::tiramisu::str_dump("op type: o_eq"));
                break;
            case ::tiramisu::o_ne:
                //result = Halide::Internal::NE::make(op0, op1, true);
                result << op0.str() + " != " + op1.str();
                //DEBUG(10, ::tiramisu::str_dump("op type: o_ne"));
                break;
/*
            case ::tiramisu::o_type:
                result = halide_expr_from_tiramisu_type(tiramisu_expr.get_data_type());
                break;
            case ::tiramisu::o_access:
            case ::tiramisu::o_lin_index:
            case ::tiramisu::o_address:
            case ::tiramisu::o_address_of:
            {
                //DEBUG(10, ::tiramisu::str_dump("op type: o_access or o_address"));

                const char *access_comp_name = NULL;

                if (tiramisu_expr.get_op_type() == ::tiramisu::o_access ||
                    tiramisu_expr.get_op_type() == ::tiramisu::o_lin_index ||
                    tiramisu_expr.get_op_type() == ::tiramisu::o_address_of)
                {
                    access_comp_name = tiramisu_expr.get_name().c_str();
                }
                else if (tiramisu_expr.get_op_type() == ::tiramisu::o_address)
                {
                    access_comp_name = tiramisu_expr.get_operand(0).get_name().c_str();
                }
                else
                {
                    ERROR("Unsupported operation.", true);
                }

                assert(access_comp_name != NULL);

                //DEBUG(10, ::tiramisu::str_dump("Computation being accessed: "); ::tiramisu::str_dump(access_comp_name));

                // Since we modify the names of update computations but do not modify the
                // expressions.  When accessing the expressions we find the old names, so
                // we need to look for the new names instead of the old names.
                // We do this instead of actually changing the expressions, because changing
                // the expressions will make the semantics of the printed program ambiguous,
                // since we do not have any way to distinguish between which update is the
                // consumer is consuming exactly.
                std::vector<tiramisu::computation *> computations_vector
                        = fct->get_computation_by_name(access_comp_name);
                if (computations_vector.size() == 0)
                {
                    // Search for update computations.
                    computations_vector
                            = fct->get_computation_by_name("_" + std::string(access_comp_name) + "_update_0");
                    assert((computations_vector.size() > 0) && "Computation not found.");
                }

                // We assume that computations that have the same name write all to the same buffer
                // but may have different access relations.
                tiramisu::computation *access_comp = computations_vector[0];
                assert((access_comp != NULL) && "Accessed computation is NULL.");
                if (comp && comp->is_wait()) {
                    // swap
                    // use operations_vector[0] instead of access_comp because we need it to be non-const
                    isl_map *orig = computations_vector[0]->get_access_relation();
                    computations_vector[0]->set_access(computations_vector[0]->wait_access_map);
                    computations_vector[0]->wait_access_map = orig;
                }
                isl_map *acc = access_comp->get_access_relation_adapted_to_time_processor_domain();
                if (comp && comp->is_wait()) {
                    // swap back
                    isl_map *orig = computations_vector[0]->get_access_relation();
                    computations_vector[0]->set_access(computations_vector[0]->wait_access_map);
                    computations_vector[0]->wait_access_map = orig;
                }
                const char *buffer_name = isl_space_get_tuple_name(
                        isl_map_get_space(acc),
                        isl_dim_out);
                assert(buffer_name != NULL);
                //DEBUG(10, ::tiramisu::str_dump("Name of the associated buffer: "); ::tiramisu::str_dump(buffer_name));

                const auto &buffer_entry = fct->get_buffers().find(buffer_name);
                assert(buffer_entry != fct->get_buffers().end());

                const auto &tiramisu_buffer = buffer_entry->second;

                Halide::Type type = halide_type_from_tiramisu_type(tiramisu_buffer->get_elements_type());

                // Tiramisu buffer is from outermost to innermost, whereas Halide buffer is from innermost
                // to outermost; thus, we need to reverse the order
                halide_dimension_t *shape = new halide_dimension_t[tiramisu_buffer->get_dim_sizes().size()];
                int stride = 1;
                std::vector<Halide::Expr> strides_vector;

                if (tiramisu_buffer->has_constant_extents())
                {
                    //DEBUG(10, ::tiramisu::str_dump("Buffer has constant extents."));
                    for (size_t i = 0; i < tiramisu_buffer->get_dim_sizes().size(); i++)
                    {
                        shape[i].min = 0;
                        int dim_idx = tiramisu_buffer->get_dim_sizes().size() - i - 1;
                        shape[i].extent = (int)tiramisu_buffer->get_dim_sizes()[dim_idx].get_int_val();
                        shape[i].stride = stride;
                        stride *= (int)tiramisu_buffer->get_dim_sizes()[dim_idx].get_int_val();
                    }
                }
                else
                {
                    //DEBUG(10, ::tiramisu::str_dump("Buffer has non-constant extents."));
                    std::vector<isl_ast_expr *> empty_index_expr;
                    Halide::Expr stride_expr = Halide::Expr(1);
                    for (int i = 0; i < tiramisu_buffer->get_dim_sizes().size(); i++)
                    {
                        int dim_idx = tiramisu_buffer->get_dim_sizes().size() - i - 1;
                        strides_vector.push_back(stride_expr);
                        stride_expr = stride_expr * generator::halide_expr_from_tiramisu_expr(fct, empty_index_expr, tiramisu_buffer->get_dim_sizes()[dim_idx], comp);
                    }
                }
                //DEBUG(10, ::tiramisu::str_dump("Buffer strides have been computed."));

                if (tiramisu_expr.get_op_type() == ::tiramisu::o_access ||
                    tiramisu_expr.get_op_type() == ::tiramisu::o_address_of ||
                    tiramisu_expr.get_op_type() == ::tiramisu::o_lin_index)
                {
                    Halide::Expr index;

                    // If index_expr is empty, and since tiramisu_expr is
                    // an access expression, this means that index_expr was not
                    // computed using the statement generator because this
                    // expression is not an expression that is associated with
                    // a computation. It is rather an expression used by
                    // a computation (for example, as the size of a buffer
                    // dimension). So in this case, we retrieve the indices directly
                    // from tiramisu_expr.
                    // The possible problem in this case, is that the indices
                    // in tiramisu_expr cannot be adapted to the schedule if
                    // these indices are i, j, .... This means that these
                    // indices have to be constant value only. So we check for this.
                    if (index_expr.size() == 0)
                    {
                        //DEBUG(10, ::tiramisu::str_dump("index_expr is empty. Retrieving access indices directly from the tiramisu access expression without scheduling."));

                        for (int i = 0; i < tiramisu_buffer->get_dim_sizes().size(); i++)
                        {
			    // Actually any computation access that does not require
			    // scheduling is supported.
			    // Other access that require scheduling should not
			    // be accepted since we do not schedule them.
			    // Currently we allow all accesses since we do not have
			    // a way to check if an iterator is requires scheduling
			    // or not. But we show a warning if the access is
			    // not constant.
			    if (tiramisu_expr.get_access()[i].is_constant() == false)
			    {
				//DEBUG(3, ::tiramisu::str_dump("Possible error in code generation because the non-affine access."));
				//DEBUG(3, ::tiramisu::str_dump("Currently we do not schedule those accesses, but we allow them,"));
				//DEBUG(3, ::tiramisu::str_dump("therefore they might cause a problem in code generation."));

			    }
                            // assert(tiramisu_expr.get_access()[i].is_constant() && "Only constant accesses are supported.");
                        }

                        if (tiramisu_buffer->has_constant_extents())
                            index = tiramisu::generator::linearize_access(tiramisu_buffer->get_dim_sizes().size(), shape, tiramisu_expr.get_access());
                        else
                            index = tiramisu::generator::linearize_access(tiramisu_buffer->get_dim_sizes().size(), strides_vector, tiramisu_expr.get_access());
                    }
                    else
                    {
                        //DEBUG(10, ::tiramisu::str_dump("index_expr is NOT empty. Retrieving access indices from index_expr (i.e., retrieving indices adapted to the schedule)."));
                        if (tiramisu_buffer->has_constant_extents())
                            index = tiramisu::generator::linearize_access(tiramisu_buffer->get_dim_sizes().size(), shape, index_expr[0]);
                        else
                            index = tiramisu::generator::linearize_access(tiramisu_buffer->get_dim_sizes().size(), strides_vector, index_expr[0]);

                        index_expr.erase(index_expr.begin());
                    }
                    if (tiramisu_expr.get_op_type() == ::tiramisu::o_lin_index) {
                        result = index;
                    }
                    else if (tiramisu_buffer->get_argument_type() == ::tiramisu::a_input)
                    {
                        Halide::Buffer<> buffer = Halide::Buffer<>(
                                                      type,
                                                      tiramisu_buffer->get_data(),
                                                      tiramisu_buffer->get_dim_sizes().size(),
                                                      shape,
                                                      tiramisu_buffer->get_name());

                        Halide::Internal::Parameter param =
                                Halide::Internal::Parameter(halide_type_from_tiramisu_type(tiramisu_buffer->get_elements_type()),
                                                            true,
                                                            tiramisu_buffer->get_dim_sizes().size(),
                                                            tiramisu_buffer->get_name());

                        // TODO(psuriana): ImageParam is not currently supported.
                        if (tiramisu_expr.get_op_type() != tiramisu::o_address_of) {
                            result = Halide::Internal::Load::make(
                                    type, tiramisu_buffer->get_name(), index, Halide::Buffer<>(),
                                    param, Halide::Internal::const_true(type.lanes()));
                        } else {
                            result = Halide::Internal::Variable::make(Halide::type_of<struct halide_buffer_t *>(),
                                                                                   tiramisu_buffer->get_name() + ".buffer");
                            result = Halide::Internal::Call::make(Halide::Handle(1, type.handle_type),
                                                                  "tiramisu_address_of_" +
                                                                  str_from_tiramisu_type_primitive(tiramisu_buffer->get_elements_type()),
                                                                  {result, index},
                                                                  Halide::Internal::Call::Extern);
                        }
                    }
                    else
                    {
                        if (tiramisu_expr.get_op_type() != tiramisu ::o_address_of) {
                            result = Halide::Internal::Load::make(
                                    type, tiramisu_buffer->get_name(), index, Halide::Buffer<>(),
                                    Halide::Internal::Parameter(), Halide::Internal::const_true(type.lanes()));
                        } else {
                            result = Halide::Internal::Variable::make(Halide::type_of<struct halide_buffer_t *>(),
                                                                      tiramisu_buffer->get_name() + ".buffer");
                            result = Halide::Internal::Call::make(Halide::Handle(1, type.handle_type),
                                                                  "tiramisu_address_of_" +
                                                                  str_from_tiramisu_type_primitive(tiramisu_buffer->get_elements_type()),
                                                                  {result, index},
                                                                  Halide::Internal::Call::Extern);
                        }
                    }
                }
                else if (tiramisu_expr.get_op_type() == ::tiramisu::o_address)
                {
                    // Create a pointer to Halide buffer.
                    result = Halide::Internal::Variable::make(Halide::type_of<struct halide_buffer_t *>(),
                                                              tiramisu_buffer->get_name() + ".buffer");
                }
                delete[] shape;
            }
                break;
            case ::tiramisu::o_right_shift:
                result = op0 >> op1;
                //DEBUG(10, ::tiramisu::str_dump("op type: o_right_shift"));
                break;
            case ::tiramisu::o_left_shift:
                result = op0 << op1;
                //DEBUG(10, ::tiramisu::str_dump("op type: o_left_shift"));
                break;
            case ::tiramisu::o_floor:
                result = Halide::floor(op0);
                //DEBUG(10, ::tiramisu::str_dump("op type: o_floor"));
                break;
            case ::tiramisu::o_cast:
                result = Halide::cast(halide_type_from_tiramisu_type(tiramisu_expr.get_data_type()), op0);
                //DEBUG(10, ::tiramisu::str_dump("op type: o_cast"));
                break;
            case ::tiramisu::o_sin:
                result = Halide::sin(op0);
                //DEBUG(10, ::tiramisu::str_dump("op type: o_sin"));
                break;
            case ::tiramisu::o_cos:
                result = Halide::cos(op0);
                //DEBUG(10, ::tiramisu::str_dump("op type: o_cos"));
                break;
            case ::tiramisu::o_tan:
                result = Halide::tan(op0);
                //DEBUG(10, ::tiramisu::str_dump("op type: o_tan"));
                break;
            case ::tiramisu::o_asin:
                result = Halide::asin(op0);
                //DEBUG(10, ::tiramisu::str_dump("op type: o_asin"));
                break;
            case ::tiramisu::o_acos:
                result = Halide::acos(op0);
                //DEBUG(10, ::tiramisu::str_dump("op type: o_acos"));
                break;
            case ::tiramisu::o_atan:
                result = Halide::atan(op0);
                //DEBUG(10, ::tiramisu::str_dump("op type: o_atan"));
                break;
            case ::tiramisu::o_sinh:
                result = Halide::sinh(op0);
                //DEBUG(10, ::tiramisu::str_dump("op type: o_sinh"));
                break;
            case ::tiramisu::o_cosh:
                result = Halide::cosh(op0);
                //DEBUG(10, ::tiramisu::str_dump("op type: o_cosh"));
                break;
            case ::tiramisu::o_tanh:
                result = Halide::tanh(op0);
                //DEBUG(10, ::tiramisu::str_dump("op type: o_tanh"));
                break;
            case ::tiramisu::o_asinh:
                result = Halide::asinh(op0);
                //DEBUG(10, ::tiramisu::str_dump("op type: o_asinh"));
                break;
            case ::tiramisu::o_acosh:
                result = Halide::acosh(op0);
                //DEBUG(10, ::tiramisu::str_dump("op type: o_acosh"));
                break;
            case ::tiramisu::o_atanh:
                result = Halide::atanh(op0);
                //DEBUG(10, ::tiramisu::str_dump("op type: o_atanh"));
                break;
            case ::tiramisu::o_abs:
                result = Halide::abs(op0);
                //DEBUG(10, ::tiramisu::str_dump("op type: o_abs"));
                break;
            case ::tiramisu::o_sqrt:
                result = Halide::sqrt(op0);
                //DEBUG(10, ::tiramisu::str_dump("op type: o_sqrt"));
                break;
            case ::tiramisu::o_expo:
                result = Halide::exp(op0);
                //DEBUG(10, ::tiramisu::str_dump("op type: o_expo"));
                break;
            case ::tiramisu::o_log:
                result = Halide::log(op0);
                //DEBUG(10, ::tiramisu::str_dump("op type: o_log"));
                break;
            case ::tiramisu::o_ceil:
                result = Halide::ceil(op0);
                //DEBUG(10, ::tiramisu::str_dump("op type: o_ceil"));
                break;
            case ::tiramisu::o_round:
                result = Halide::round(op0);
                //DEBUG(10, ::tiramisu::str_dump("op type: o_round"));
                break;
            case ::tiramisu::o_trunc:
                result = Halide::trunc(op0);
                //DEBUG(10, ::tiramisu::str_dump("op type: o_trunc"));
                break;
*/
            case ::tiramisu::o_type:
            case ::tiramisu::o_access:
            case ::tiramisu::o_lin_index:
            case ::tiramisu::o_address:
            case ::tiramisu::o_address_of:
            case ::tiramisu::o_right_shift:
            case ::tiramisu::o_left_shift:
            case ::tiramisu::o_floor:
            case ::tiramisu::o_cast:
            case ::tiramisu::o_sin:
            case ::tiramisu::o_cos:
            case ::tiramisu::o_tan:
            case ::tiramisu::o_asin:
            case ::tiramisu::o_acos:
            case ::tiramisu::o_atan:
            case ::tiramisu::o_sinh:
            case ::tiramisu::o_cosh:
            case ::tiramisu::o_tanh:
            case ::tiramisu::o_asinh:
            case ::tiramisu::o_acosh:
            case ::tiramisu::o_atanh:
            case ::tiramisu::o_abs:
            case ::tiramisu::o_sqrt:
            case ::tiramisu::o_expo:
            case ::tiramisu::o_log:
            case ::tiramisu::o_ceil:
            case ::tiramisu::o_round:
            case ::tiramisu::o_trunc:
                break;
            case ::tiramisu::o_call:
            {
/*
                std::vector<Halide::Expr> vec;
                for (const auto &e : tiramisu_expr.get_arguments())
                {
                    Halide::Expr he = generator::halide_expr_from_tiramisu_expr(fct, index_expr, e, comp);
                    vec.push_back(he);
                }
                result = Halide::Internal::Call::make(halide_type_from_tiramisu_type(tiramisu_expr.get_data_type()),
                                                      tiramisu_expr.get_name(),
                                                      vec,
                                                      Halide::Internal::Call::CallType::Extern);
*/
                result << tiramisu_expr.get_name() + "(";

                std::vector<std::string> args{};
                const auto expr_args = tiramisu_expr.get_arguments(); 
                std::int64_t i = 0;
                for(const auto &e : expr_args) {
                    result << gen_physl_from_tiramisu_expr(f, index_expr, e, comp);
                    if(i < expr_args.size()-1) {
                        result << ", ";
                    }
                }
                result << ")";

                //DEBUG(10, ::tiramisu::str_dump("op type: o_call"));
                break;
            }
/*
            case ::tiramisu::o_allocate:
            case ::tiramisu::o_free:
                ERROR("An expression of type o_allocate or o_free "
                                        "should not be passed to this function", true);
                break;
*/
            case ::tiramisu::o_allocate:
            case ::tiramisu::o_free:
                break;


            default:
                //ERROR("Translating an unsupported ISL expression into a Halide expression.", 1);
                break;
        }
    }
/*
    else if (tiramisu_expr.get_expr_type() == ::tiramisu::e_var)
    {
        //DEBUG(3, ::tiramisu::str_dump("Generating a variable access expression."));
        //DEBUG(3, ::tiramisu::str_dump("Expression is a variable of type: " + tiramisu::str_from_tiramisu_type_primitive(tiramisu_expr.get_data_type())));
        result = Halide::Internal::Variable::make(
                halide_type_from_tiramisu_type(tiramisu_expr.get_data_type()),
                tiramisu_expr.get_name());
    }
*/
    else
    {
        ::tiramisu::str_dump("tiramisu type of expr: ",
                           str_from_tiramisu_type_expr(tiramisu_expr.get_expr_type()).c_str());
        //ERROR("\nTranslating an unsupported ISL expression in a Halide expression.", 1);
    }

    //if (result.defined())
    //{
        //DEBUG(10, ::tiramisu::str_dump("Generated stmt: "); std::cout << result);
    //}

    //DEBUG_INDENT(-4);
    //DEBUG_FCT_NAME(10);

    ret_result = result.str();
}




} /* end namespace tiramisu */ } // end namespace physl
