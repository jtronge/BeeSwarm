FROM debian:11

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get -y install git cmake gcc g++ gfortran libopenmpi-dev openmpi-bin \
                       libpmix-dev libpmix-bin curl

# Put scripts in /opt
COPY scripts /opt/
