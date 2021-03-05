# Copyright (c) 2019-2020 Christopher Taylor
#
#  Distributed under the Boost Software License, Version 1.0. (See accompanying
#  file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
#
BASE_DIR=$(HOME)/git

# this is a variable referencing the
# source tree for isl where the file
# 'isl_ast_private.h' is located.
# this file is not part of the isl
# install manifest.
#
ISL_SOURCE_BASE_DIR=$(TIRAMISU_ROOT_DIR)/3rdParty/isl

# this is a variable referencing the
# installed build of isl
#
ISL_ROOT_DIR=$(ISL_SOURCE_BASE_DIR)/build
ISL_LIB_DIR=$(ISL_ROOT_DIR)/lib
ISL_INC_DIR=$(ISL_ROOT_DIR)/include

TIRAMISU_ROOT_DIR=$(BASE_DIR)/tiramisu
TIRAMISU_LIB_DIR=$(TIRAMISU_ROOT_DIR)/build
TIRAMISU_INC_DIR=$(TIRAMISU_ROOT_DIR)/include

EXTRA_INC=$(HOME)/git/install/include 
EXTRA_LIB=$(HOME)/git/install/lib

INC_FLAGS=-I$(EXTRA_INC) -I$(ISL_INC_DIR) -I$(TIRAMISU_INC_DIR) -I$(ISL_SOURCE_BASE_DIR)
LIB_FLAGS=-L$(EXTRA_LIB) -L$(ISL_LIB_DIR) -L$(TIRAMISU_LIB_DIR)
LIBS=-lisl -ltiramisu
CXX_FLAGS=-g -Wall -shared -std=c++14 -fPIC $(CXX_EXT)
#-stdlib=libc++
#-D_GLIBCXX_USE_CXX11_ABI=1

# this variable should resolve to something like...
# pytiramisu.cpython-36m-x86_64-linux-gnu.so
#
PYTIRAMISU_OBJ=pytiramisu`python3.8-config --extension-suffix`

CXX_EXT=$(INC_FLAGS) $(LIB_FLAGS)
CXX=clang++-8
#CXX=g++

#all: $(PYTIRAMISU_OBJ)
#	@echo "pytiramisu build complete"

all: physl_isl.o physl_tiramisu.o pytiramisu.cpp
	$(CXX) $(CXX_FLAGS) physl_isl.o physl_tiramisu.o pytiramisu.cpp -o $(PYTIRAMISU_OBJ) `python3.8 -m pybind11 --includes` $(LIBS)

physl_isl.o: physl_isl.cpp
	$(CXX) -O3 -std=c++17 -fPIC $(INC_FLAGS) -c physl_isl.cpp

physl_tiramisu.o: physl_isl.o physl_tiramisu.cpp
	$(CXX) -O3 -std=c++17 -fPIC $(INC_FLAGS) -c physl_tiramisu.cpp


#test: physl_tiramisu.o physl_isl.o
#	$(CXX) $(CXX_FLAGS) -g $(INC_FLAGS) $(LIB_FLAGS) test.cpp -o test physl_isl.o physl_tiramisu.o $(LIBS)
#	g++ $(CXX_FLAGS) -g $(INC_FLAGS) $(LIB_FLAGS) test.cpp -o test physl_isl.o physl_tiramisu.o $(LIBS)
#test:
#	$(CXX) $(CXX_FLAGS) -g -fPIC $(INC_FLAGS) $(LIB_FLAGS) test.cpp -o test
 
clean:
	rm *.o
	rm $(PYTIRAMISU_OBJ)
