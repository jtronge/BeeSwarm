FROM jtronge/openmpi-debian

ARG REPO=https://github.com/jtronge/CoMD.git
ARG COMMIT

# Build the MPI version
RUN git clone $REPO && \
    cd CoMD && \
    git checkout $COMMIT && \
    cp src-mpi/Makefile.vanilla src-mpi/Makefile && \
    make -C src-mpi
