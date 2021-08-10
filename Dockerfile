FROM python:3.6-slim as python-base
ENV TZ=Asia/Seoul \
    \
    # python    
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 

FROM python-base as builder-base
    # poetry
ENV POETRY_VERSION=1.1.7 \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1 \ 
    POETRY_HOME="/opt/poetry" 
    
    # path
ENV PATH="${POETRY_HOME}/bin:${PATH}"

RUN apt-get update && apt-get install -y curl

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -

WORKDIR /build
COPY poetry.lock pyproject.toml ./

RUN poetry export -o requirements.txt
RUN pip install --user -r requirements.txt

FROM python-base as release-base

WORKDIR /app
COPY main.py ./
COPY utils/ ./utils/
COPY --from=builder-base /root/.local /root/.local

CMD [ "python", "main.py" ]