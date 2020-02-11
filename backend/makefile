# Copyright (c) 2019-2020 Christopher Taylor
#
#  Distributed under the Boost Software License, Version 1.0. (See accompanying
#  file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
#
BASE_DIR=$(HOME)/git
ISL_BASE_DIR=$(BASE_DIR)/isl
ISL_ROOT_DIR=$(ISL_BASE_DIR)/install
TIRAMISU_ROOT_DIR=$(BASE_DIR)/tiramisu
HALIDE_ROOT_DIR=$(BASE_DIR)/tiramisu/3rdParty/Halide/build

INC_FLAGS=-I$(HOME)/git/install/include -I$(ISL_ROOT_DIR)/include -I$(HALIDE_ROOT_DIR)/include -I$(TIRAMISU_ROOT_DIR)/include -I$(ISL_BASE_DIR)
LIB_FLAGS=-L$(HOME)/git/install/lib -L$(ISL_ROOT_DIR)/lib -L$(HALIDE_ROOT_DIR)/lib -L$(TIRAMISU_ROOT_DIR)/build
#LIBS=-lstdc++ -lisl -lHalide -ltiramisu
LIBS=-lisl -lHalide -ltiramisu
#CXX_FLAGS=-O3 -Wall -shared -std=c++17 -fPIC -fsized-deallocation -Wdelete-non-abstract-non-virtual-dtor -D_GLIBCXX_USE_CXX11_ABI=1
#CXX_FLAGS=-std=libstdc++ -lstdc++ -O3 -Wall -shared -std=c++17
CXX_FLAGS=-stdlib=libstdc++ -O3 -Wall -shared -std=c++17
#-D_GLIBCXX_USE_CXX11_ABI=1
#--no-as-needed 

PYTIRAMISU_OBJ=pytiramisu`python3.6-config --extension-suffix`
#pytiramisu.cpython-36m-x86_64-linux-gnu.so

CXX_EXT=$(INC_FLAGS) $(LIB_FLAGS) $(LIBS)
CXX=clang++-8
GCXX=g++-8

all: $(PYTIRAMISU_OBJ) test
	@echo "pytiramisu build complete"

physl_isl.o: physl_isl.cpp
	$(CXX) -O3 -std=c++17 -stdlib=libstdc++ -fPIC $(INC_FLAGS) -c physl_isl.cpp

physl_tiramisu.o: physl_isl.o physl_tiramisu.cpp
	$(CXX) -O3 -std=c++17 -stdlib=libstdc++ -fPIC $(INC_FLAGS) -c physl_tiramisu.cpp

$(PYTIRAMISU_OBJ): physl_isl.o physl_tiramisu.o pytiramisu.cpp
	$(CXX) $(CXX_FLAGS) -fPIC `python3.6 -m pybind11 --includes` pytiramisu.cpp -o $(PYTIRAMISU_OBJ) physl_isl.o physl_tiramisu.o $(CXX_EXT)

test: physl_tiramisu.o physl_isl.o
	$(CXX) $(CXX_FLAGS) -g $(INC_FLAGS) $(LIB_FLAGS) test.cpp -o test physl_isl.o physl_tiramisu.o $(LIBS)
#	g++ $(CXX_FLAGS) -g $(INC_FLAGS) $(LIB_FLAGS) test.cpp -o test physl_isl.o physl_tiramisu.o $(LIBS)

clean:
	rm physl_isl.o
	rm $(PYTIRAMISU_OBJ)
