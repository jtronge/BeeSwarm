FROM jtronge/openmpi-debian

ARG REPO=https://github.com/llnl/LULESH.git
ARG BRANCH=master
# ARG COMMIT=3e01c40b3281aadb7f996525cdd4a3354f6d3801
# Note: disables OpenMP for doing the strong scaling test
RUN git clone -b $BRANCH $REPO && \
    cd LULESH && \
    mkdir -p build &&  \
    cd build && \
    cmake -DCMAKE_BUILD_TYPE=Release -DMPI_CXX_COMPILER=`which mpicxx` -DWITH_OPENMP=FALSE ../ && \
    make && \
    cp lulesh2.0 /
