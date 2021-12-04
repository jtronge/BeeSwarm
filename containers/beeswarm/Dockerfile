FROM debian:11

RUN apt-get -y update && \
    apt-get -y install python3 python3-pip python3-requests gcc curl git

RUN curl -O -L https://github.com/hpc/charliecloud/releases/download/v0.25/charliecloud-0.25.tar.gz && \
    tar -xvf charliecloud-0.25.tar.gz && \
    cd charliecloud-0.25 && \
    ./configure --prefix=/usr && \
    make && \
    make install

COPY bee-setup.sh /
RUN /bee-setup.sh
