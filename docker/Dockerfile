# Copyright (c) 2020 R. Tohid
#
# Distributed under the Boost Software License, Version 1.0. (See a copy at
# http://www.boost.org/LICENSE_1_0.txt)

FROM fedora

RUN dnf -y update

RUN dnf install -y sudo

RUN dnf install -y xz xz-devel bzip2 bzip2-devel zlib-devel tar
RUN dnf install -y compat-openssl10 compat-openssl10-devel

RUN dnf install -y git
RUN dnf install -y wget curl
RUN dnf install -y findutils which


RUN dnf install -y vim-enhanced 
RUN dnf install -y bash-completion
RUN dnf install -y environment-modules 

RUN dnf install -y make cmake
RUN dnf install -y llvm llvm-devel clang clang-devel

RUN dnf install -y flex patch graphviz

ARG BUILD_PATH=/usr/local/build
ARG BUILD_TYPE=Debug
ARG PYTHON_VERSION=3.8
ARG NPROCS=48
ARG PREFIX=/home/stellar/bin
ARG REPO_PATH=/home/stellar/repos
ARG USER=stellar

# install Python ${PYTHON_VERSION}
RUN git clone -b ${PYTHON_VERSION} https://github.com/python/cpython.git python-${PYTHON_VERSION}
WORKDIR /python-${PYTHON_VERSION}
RUN ./configure
RUN make -j ${NPROCS} install

RUN python3 -m pip install -U pip
RUN python3 -m pip install pytest

# add user
RUN groupadd -r ${USER}
RUN useradd -r -m -g stellar -G wheel stellar
RUN echo '%wheel ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers


RUN mkdir -p ${PREFIX}

# install pybind11
WORKDIR ${REPO_PATH}
RUN git clone https://github.com/pybind/pybind11.git
WORKDIR ${BUILD_PATH}/pybind11
RUN cmake \
        -DCMAKE_BUILD_TYPE=${BUILD_TYPE} \
        ${REPO_PATH}/pybind11
RUN make -j ${NPROCS} install


COPY Dockerfile /Dockerfile

RUN sudo chown -R stellar:stellar /home/stellar

USER stellar
RUN sh -c "$(wget https://raw.githubusercontent.com/ohmybash/oh-my-bash/master/tools/install.sh -O -)"