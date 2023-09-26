#!/usr/bin/env sh

act -W .github/workflows/lint.yaml && \
act -W .github/workflows/test.yaml && \
act -W .github/workflows/integration-test.yaml && \
echo OK!
