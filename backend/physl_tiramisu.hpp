//  Copyright (c) 2019-2020 Christopher Taylor
//
//  Distributed under the Boost Software License, Version 1.0. (See accompanying
//  file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
//
#pragma once

#ifndef __PHYSL_TIRAMISU__
#define __PHYSL_TIRAMISU__

#include <map>
#include <unordered_map>
#include <string>
#include <vector>
#include <numeric>
#include <memory>
#include <sstream>
#include <iostream>
#include <algorithm>

#include <tiramisu/tiramisu.h>

#include "physl_isl.hpp"

namespace physl { namespace tiramisu {

using namespace tiramisu;

class PhyslComputation : public ::tiramisu::computation {

public:

    std::unordered_map<std::string, std::string> get_iterators_mapping() {
        std::unordered_map<std::string, std::string> ret_map{};

        const auto map = get_iterators_map();
        for(const auto& p : map) {
            ret_map[std::get<0>(p)] = std::string{isl_ast_expr_to_C_str(std::get<1>(p))};
        }

        return ret_map;
    }
};

class PhyslFunction : public ::tiramisu::function, ::tiramisu::generator {

    public:

    PhyslFunction() : function("physl_codegen"), generator() {
    }

    PhyslFunction(std::string & name) : function(name), generator() {
    }

    void lift_dist_computations() {
        lift_dist_comps();
    }

    static inline std::string get_value(const ::tiramisu::expr& e) {
        if (e.get_expr_type() == ::tiramisu::e_val) {
            const auto edt = e.get_data_type();
            if (edt == ::tiramisu::p_uint8) {
                return std::to_string(e.get_uint8_value());
            }
            else if (edt == ::tiramisu::p_int8) {
                return std::to_string(e.get_int8_value());
            }
            else if (edt == ::tiramisu::p_uint16) {
                return std::to_string(e.get_uint16_value());
            }
            else if (edt == ::tiramisu::p_int16) {
                return std::to_string(e.get_int16_value());
            }
            else if (edt == ::tiramisu::p_uint32) {
                return std::to_string(e.get_uint32_value());
            }
            else if (edt == ::tiramisu::p_int32) {
                return std::to_string(e.get_int32_value());
            }
            else if (edt == ::tiramisu::p_uint64) {
                return std::to_string(e.get_uint64_value());
            }
            else if (edt == ::tiramisu::p_int64) {
                return std::to_string(e.get_int64_value());
            }
            else if (edt == ::tiramisu::p_float32) {
                return std::to_string(e.get_float32_value());
            }
            else if (edt == ::tiramisu::p_float64) {
                return std::to_string(e.get_float64_value());
            }
        }

        return "";
    }; 

    static isl_ast_node *for_code_generator_after_for(isl_ast_node *node, isl_ast_build *build, void *user)
    {
        return node;
    }

    std::vector< std::unordered_map<std::string, std::string> > generate_code(std::vector< ::tiramisu::buffer* > & bufs) {

        set_arguments(bufs);
        lift_dist_computations();
        gen_time_space_domain();
        gen_isl_ast();

        auto computations = this->get_computations(); 

        std::vector< std::unordered_map<std::string, std::string> > generated_code{};

        if(computations.size() < 1) {
            std::string strout = 
            physl::codegen::generate_physl(
                this->get_isl_ctx(),
                this->get_isl_ast()
            );

            std::unordered_map<std::string, std::string> comp_code{};
            comp_code["computation"] = "none";
            comp_code["isl"] = strout;
            generated_code.emplace_back(comp_code);
        }
        else {
           generated_code.resize(computations.size());

           auto ctx = this->get_isl_ctx();
           auto ast = this->get_isl_ast();

           for(auto & comp : computations) {
                std::unordered_map<std::string, std::string> comp_code{};
                comp_code["computation"] = comp->get_name();

                std::string physl_loop_str = 
                    physl::codegen::generate_physl(
                        ctx,
                        ast
                    );

                if(physl_loop_str.size() > 0) {
                    comp_code["isl"] = physl_loop_str;
                }

                auto map = reinterpret_cast<PhyslComputation*>(comp)->get_iterators_mapping();
                std::string iter_mapping{};

                const std::int32_t map_size = map.size();
                std::int32_t map_counter = 0;
                for(auto p : map) {
                    iter_mapping += std::get<0>(p) + ":" + std::get<1>(p) +
                         ((map_counter == (map_size-1)) ? "" : ",");
                    ++map_counter;
                }

std::cout << "c++ iter_mapping size\t" << iter_mapping.size() << std::endl;

                comp_code["iterators"] = iter_mapping;

/*
                std::string dim_str{}, buffer_indices{"i, j"}, buffer_name{};

                const auto buffer = comp->get_buffer();
                buffer_name = buffer->get_name();
                auto dim_vec = buffer->get_dim_sizes();
                const auto dim_vec_size = dim_vec.size();

                for(std::int64_t i = 0; i < dim_vec_size; ++i) {
                    dim_str += get_value(dim_vec[i]);

                    if(dim_str.size() < 1) {
                        std::cerr << "provided tiramisu dimension value bad" << std::endl;
                        break;
                    }

                    if(i < dim_vec_size-1) {
                                dim_str += ", ";
                    }
               }
*/
               generated_code.emplace_back(comp_code);
           }

// buffer_indices -> tiramisu_codegen_halide.cpp -> std::map<std::string, isl_ast_expr *> generator::compute_iterators_map

/*
           std::stringstream code{};
           code << "define(" << buffer_name << ", shape(" << dim_str << "))" << std::endl
                << "define(" << comp->get_name() << ", " << buffer_indices << ", __tiramisu__schedule_index__, block(" << std::endl
                << "    store(" << buffer_name << "(" << buffer_indices << "), " << str_ << ")" << std::endl
                << "), " << buffer_name << ")" << std::endl
                << "//KERNEL_EXPR_ABOVE_SPLIT_BELOW_FOR_LOOP_PARAMS" << std::endl
                << physl_str_ << std::endl;
                         
            comp_code["expr"] = code.str();
*/
        }

        return generated_code;
    }
};

std::vector< std::unordered_map<std::string, std::string> > codegen(std::vector< ::tiramisu::buffer > &arguments);

} /* end namespace tiramisu */ } // end namespace physl

static std::vector< std::unordered_map<std::string, std::string> > codegen_physl(std::vector< tiramisu::buffer > &arguments) {
    return physl::tiramisu::codegen(arguments);
}

#endif
