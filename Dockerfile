FROM python:3.6 as python-base
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
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    POETRY_VERSION=1.1.7 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1


# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM python-base as builder-base

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

WORKDIR /build
COPY poetry.lock pyproject.toml ./

RUN poetry export

FROM python-base as release-base

WORKDIR /app
COPY main.py ./
COPY utils/ ./utils/
COPY --from=builder-base /build/requirements.txt ./

RUN pip install -r requirements.txt

CMD [ "python", "main.py" ]