FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

# Runtime dependencies
RUN apt-get update && apt-get install -y python3 jq

# Test tools
RUN apt-get update && apt-get install -y git python3-pytest
RUN (git clone -b v1.7.0 https://github.com/bats-core/bats-core && \
	cd bats-core && ./install.sh /usr/local)
RUN (cd /usr/lib;\
	git clone https://github.com/bats-core/bats-assert;\
	git clone https://github.com/bats-core/bats-support)
