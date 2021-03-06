FROM ubuntu:16.04

RUN apt-get update -q && \
    apt-get install -qy git python3 python3-pip wget && \
    apt-get install -qy libgc-dev libunwind8-dev libz-dev libpcre3-dev

RUN echo "deb http://apt.llvm.org/xenial/ llvm-toolchain-xenial-3.9 main" >> /etc/apt/sources.list && \
    echo "deb-src http://apt.llvm.org/xenial/ llvm-toolchain-xenial-3.9 main" >> /etc/apt/sources.list && \
    wget -O - http://apt.llvm.org/llvm-snapshot.gpg.key | apt-key add - && \
    apt-get update -q && \
    apt-get install -qy llvm-3.9 clang-3.9 && \
    ln -s /usr/bin/clang-3.9 /usr/bin/clang && \
    ln -s /usr/bin/llvm-config-3.9 /usr/bin/llvm-config
