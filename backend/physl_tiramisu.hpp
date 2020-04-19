//  Copyright (c) 2019-2020 Christopher Taylor
//
//  Distributed under the Boost Software License, Version 1.0. (See accompanying
//  file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
//
#pragma once

#ifndef __PHYSL_TIRAMISU__
#define __PHYSL_TIRAMISU__

#include <string>
#include <memory>

#include <tiramisu/tiramisu.h>

using namespace tiramisu;

namespace physl { namespace tiramisu {

int codegen(std::vector< buffer > &arguments, std::string & physlstr);

} /* end namespace tiramisu */ } // end namespace physl

#endif
