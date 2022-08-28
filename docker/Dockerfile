# syntax=docker/dockerfile:1

ARG POETRY_HOME=/opt/poetry
ARG PYTHON_VERSION=3.10
ARG USER="vscode"
ARG GROUP="ccds"

FROM mcr.microsoft.com/vscode/devcontainers/python:${PYTHON_VERSION}-buster as builder
# FROM python:${PYTHON_VERSION}-buster as builder

ARG POETRY_HOME
ARG USER
ARG GROUP
ENV PATH="$POETRY_HOME/bin:$PATH"

# poetryの導入
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - \
    && poetry config virtualenvs.create false

WORKDIR /poetry_practice
COPY pyproject.toml poetry.lock* ./

# RUN pip install setuptools -t /usr/local/lib/python3.10/site-packages/
RUN --mount=type=cache,target=~/.cache/pypoetry poetry install --no-root


RUN if ! cat /etc/group | grep -e $GROUP: > /dev/null 2>&1; then groupadd -r $GROUP; fi \
    && usermod -a -G $GROUP $USER 
    # && umask 0002 && mkdir poetry_practice \
    # && chown -R $USER:$GROUP /poetry_practice


# FROM mcr.microsoft.com/vscode/devcontainers/python:${PYTHON_VERSION}-buster as base
FROM python:${PYTHON_VERSION}-buster as base
ARG POETRY_HOME

# 日本語設定
RUN apt-get update \
    && apt-get install -y locales \
    && locale-gen ja_JP.UTF-8 \
    && localedef -f UTF-8 -i ja_JP ja_JP.utf8

ENV LANG ja_JP.UTF-8 \
    LANGUAGE ja_JP:ja \
    LC_ALL=ja_JP.UTF-8

COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group
COPY --from=builder --chown=$USER:$GROUP /opt/poetry /opt/poetry
COPY --from=builder --chown=$USER:$GROUP /root/.cache/pypoetry /root/.cache/pypoetry
# COPY --from=builder --chown=$USER:$GROUP /usr/local/lib/python${PYTHON_VERSION}/site-packages/ /usr/local/lib/python${PYTHON_VERSION}/site-packages/

# python周りの設定
ENV PYTHONDONTWRITEBYTECODE=1 \ 
    PYTHONUNBUFFERED=1 \
    PYTHONUTF8=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PATH="$POETRY_HOME/bin:$PATH"


# 開発用
FROM base as dev
ARG USER
ARG GROUP

RUN apt-get update && apt-get install -y \
    git \
    vim \
    && \
    apt-get clean && rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/*

RUN umask 0002 && mkdir poetry_practice \
    && chown -R $USER:$GROUP /poetry_practice \
    && cd /poetry_practice

WORKDIR /poetry_practice
COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false \
    && poetry completions bash > /etc/bash_completion.d/poetry.bash-completion \
    && poetry install --no-root && rm -rf ~/.cache/pypoetry


# ユーザの作成
USER $USER
# RUN poetry install --no-root && rm -rf ~/.cache/pypoetry
# EXPOSE $APP_PORT
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]


# # 本番用
# FROM base as prod
# RUN poetry install --no-root --no-dev && rm -rf ~/.cache/pypoetry
