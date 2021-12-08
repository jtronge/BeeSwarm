FROM debian:11

ENV DEBIAN_FRONTEND=noninteractive
RUN echo "deb http://deb.debian.org/debian buster-backports main" >> /etc/apt/sources.list \
    && apt-get update \
    && apt-get -y install python3.6 \
                          python3-pip \
                          python3-venv \
                          python3-dev \
                          python3-jinja2 \
                          python3-yaml \
                          python3-requests \
                          build-essential \
                          vim \
                          git \
                          curl \
                          procps \
                          tmux \
                          screen \
                          wireguard

# Install Charliecloud
RUN curl -O -L https://github.com/hpc/charliecloud/releases/download/v0.25/charliecloud-0.25.tar.gz \
    && tar -xvf charliecloud-0.25.tar.gz \
    && cd charliecloud-0.25 \
    && ./configure --prefix=/usr \
    && make \
    && make install

# Make a /data directory
RUN mkdir -p /data
