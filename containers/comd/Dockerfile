FROM jtronge/openmpi-debian

ARG BRANCH
RUN git clone https://github.com/ECP-copa/CoMD.git && \
    cd CoMD && \
    git checkout $BRANCH && \
    cp src-mpi/Makefile.vanilla src-mpi/Makefile && \
    make -C src-mpi
