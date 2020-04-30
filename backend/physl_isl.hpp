//  Copyright (c) 2019-2020 Christopher Taylor
//
//  Distributed under the Boost Software License, Version 1.0. (See accompanying
//  file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
//
#pragma once

#ifndef __PHYSL_CODEGEN__
#define __PHYSL_CODEGEN__

#include <string>
#include <memory>
#include <ostream>

#include <isl/ast_type.h>
#include <tiramisu/core.h>

namespace physl { namespace codegen {

std::string generate_physl(isl_ctx * ctx, isl_ast_node * node);
//int generate_physl(isl_ctx * ctx, isl_ast_node * node, std::ostream & fstr);
//int generate_physl(isl_ctx * ctx, isl_ast_node * node, std::string & physlstr);

int generate_physl(isl_ctx * ctx, isl_ast_node * node, const ::tiramisu::expr & e);
int generate_physl(isl_ctx * ctx, isl_ast_node * node, const ::tiramisu::expr & e, const std::string & kernel_str, std::ostream & fstr);
int generate_physl(isl_ctx * ctx, isl_ast_node * node, const ::tiramisu::expr & e, const std::string & kernel_str, std::string & physlstr);

} /* end namespace codegen */ } // end namespace physl

#endif
