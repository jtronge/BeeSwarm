FROM jtronge/openmpi-debian

ARG BRANCH=master
RUN git clone -b $BRANCH https://github.com/LLNL/LULESH.git && \
    cd LULESH && \
    mkdir -p build &&  \
    cd build && \
    cmake -DCMAKE_BUILD_TYPE=Release -DMPI_CXX_COMPILER=`which mpicxx` ../ && \
    make && \
    cp lulesh2.0 /

# Add a run script
RUN printf "#!/bin/sh\n" > /run.sh && \
    printf "exec /lulesh2.0 $@\n" >> /run.sh && \
    chmod 755 /run.sh
