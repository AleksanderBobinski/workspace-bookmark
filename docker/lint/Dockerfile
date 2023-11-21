FROM archlinux:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN pacman-key --refresh-keys && pacman -Syyu --noconfirm python-pylint \
	python-black \
	flake8 \
	python-pip \
	python-pytest
RUN pip install --break-system-packages \
	pylint-pytest
