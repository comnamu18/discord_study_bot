FROM ubuntu:18.04

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Seoul \
    LC_ALL=ko_KR.UTF-8 \
    LANG=ko_KR.UTF-8 \
    LANGUAGE=ko_KR.UTF-8 \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.1.7

RUN apt-get update -y
RUN apt-get install --no-install-recommends -y \
    g++ \
    ca-certificates \
    python3-dev \
    python3-distutils \
    python3-venv \
    git \
    ntp \
    tmux \
    locales \
    curl

# cleanup
RUN apt-get autoclean \
	&& apt-get -y autoremove \	
	&& rm -rf /var/lib/apt/lists/*

RUN locale-gen ko_KR.UTF-8

# PIP and python settings
RUN cd /tmp
RUN curl -O https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py

RUN ln -s /usr/bin/python3 /usr/bin/python
RUN ln -s /usr/bin/pip3 /usr/bin/pip

#Poetry Setttings
RUN pip install "poetry==$POETRY_VERSION"
WORKDIR /workspace
COPY poetry.lock pyproject.toml /workspace/

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

COPY . /workspace