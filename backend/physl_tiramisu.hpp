//  Copyright (c) 2019-2020 Christopher Taylor
//
//  Distributed under the Boost Software License, Version 1.0. (See accompanying
//  file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
//
#pragma once

#ifndef __PHYSL_TIRAMISU__
#define __PHYSL_TIRAMISU__

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

class PhyslFunction : public ::tiramisu::function, ::tiramisu::generator {

    private:

    std::vector<std::string> computations_physl;

    public:

    PhyslFunction() : function("physl_codegen"), generator(), computations_physl() {
    }

    PhyslFunction(std::string & name) : function(name), generator(), computations_physl() {
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

    void generate_code(std::vector< ::tiramisu::buffer* > & bufs, std::string &physlstr) {

        set_arguments(bufs);
        lift_dist_computations();
        gen_time_space_domain();
        gen_isl_ast();

        const auto computations = this->get_computations();

        if(computations.size() < 1) {
            std::cerr << "no computations associated with PhyslFunction:\t" << this->get_name() << std::endl;

            std::string strout = 
            physl::codegen::generate_physl(
                this->get_isl_ctx(),
                this->get_isl_ast()
            );

            computations_physl.push_back(strout);
        }
        else {

            computations_physl.resize(computations.size());

            auto ctx = this->get_isl_ctx();
            auto ast = this->get_isl_ast();

            std::transform(computations.begin(),
                computations.end(),
                computations_physl.begin(),
                [&ctx, &ast](const auto& comp) {

                    std::string physl_str_{};
                    std::string str_{};

                    physl::codegen::generate_physl(
                        ctx,
                        ast,
                        comp->get_expr(),
                        str_,
                        physl_str_
                    );

                    std::string dim_str{}, buffer_indices{"i, j"}, buffer_name{};

                    {
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
                    }

//std::cout << str_ << "\t" << physl_str_ << std::endl;

                    std::stringstream code{};
                    code << "define(" << buffer_name << ", shape(" << dim_str << "))" << std::endl
                         << "define(" << comp->get_name() << ", " << buffer_indices << ", __tiramisu__schedule_index__, block(" << std::endl
                         << "    store(" << buffer_name << "(" << buffer_indices << "), " << str_ << ")" << std::endl
                         << "), " << buffer_name << ")" << std::endl
                         << physl_str_ << std::endl;
                         
                    return code.str();
            });
        }

        physlstr = std::accumulate(
            computations_physl.begin(),
            computations_physl.end(),
            physlstr, std::plus<std::string>()
        );
    }
};

int codegen(std::vector< ::tiramisu::buffer > &arguments, std::string & physlstr);

} /* end namespace tiramisu */ } // end namespace physl

static inline std::string codegen_physl(std::vector< tiramisu::buffer > &arguments) {
    std::string output{};
    physl::tiramisu::codegen(arguments, output);
    return output;
}

#endif
