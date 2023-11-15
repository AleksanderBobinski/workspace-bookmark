FROM archlinux:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN pacman-key --refresh-keys && pacman -Syyu --noconfirm python-pylint \
	python-black \
	flake8 \
	python-pytest

