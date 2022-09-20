FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

# Runtime dependencies
RUN apt-get update && apt-get install -y python3 jq

# Test tools
RUN apt-get update && apt-get install -y bats git python3-pytest
RUN (cd /usr/lib;\
	git clone https://github.com/bats-core/bats-assert;\
	git clone https://github.com/bats-core/bats-support)
