FROM ubuntu:18.04

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y g++ && \
    ca-certificates python3-dev python3-distutils python3-venv git ntp tmux locales curl && \
    rm -rf /var/lib/apt/lists/* && cd /tmp && \
    curl -O https://bootstrap.pypa.io/get-pip.py && \
    python3 get-pip.py

RUN ln -s /usr/bin/python3 /usr/bin/python
RUN ln -s /usr/bin/pip3 /usr/bin/pip

ENV TZ=Asia/Seoul

RUN locale-gen ko_KR.UTF-8
ENV LC_ALL=ko_KR.UTF-8
ENV LANG=ko_KR.UTF-8
ENV LANGUAGE=ko_KR.UTF-8

CMD ["python", "main.py"]