#!/usr/bin/env sh

act -W .github/workflows/lint.yaml && \
act -W .github/workflows/test.yaml

