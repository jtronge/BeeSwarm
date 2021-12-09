FROM jtronge/openmpi-debian

ARG REPO=https://github.com/jtronge/LULESH.git
ARG BRANCH=master
ARG COMMIT=3e01c40b3281aadb7f996525cdd4a3354f6d3801
RUN git clone -b $BRANCH $REPO && \
    cd LULESH && \
    git checkout $COMMIT && \
    mkdir -p build &&  \
    cd build && \
    cmake -DCMAKE_BUILD_TYPE=Release -DMPI_CXX_COMPILER=`which mpicxx` ../ && \
    make && \
    cp lulesh2.0 /

# Add a run script
RUN printf "#!/bin/sh\n" > /run.sh && \
    printf "exec /lulesh2.0 $@\n" >> /run.sh && \
    chmod 755 /run.sh
