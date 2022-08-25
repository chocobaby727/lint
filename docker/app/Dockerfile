# syntax=docker/dockerfile:1

FROM python:3.9-buster as builder
WORKDIR /ailab_line

COPY pyproject.toml poetry.lock* /ailab_line/

# poetryの導入
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 - && \
    cd /usr/local/bin && ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false && \
    cd /ailab_line

RUN --mount=type=cache,target=~/.cache/pypoetry poetry update


FROM python:3.9-slim-buster as base
WORKDIR /ailab_line

ARG USERNAME=${USERNAME}
ARG USER_UID=${USER_UID}
ARG USER_GID=${USER_GID}
ENV HOME=/home/$USERNAME

# ユーザの作成
RUN groupadd --gid $USER_GID $USERNAME && \
    useradd --uid $USER_UID --gid $USER_GID -m $USERNAME && \
    chown -R $USER_UID /ailab_line && \
    # sudoを可能にする
    apt-get update && \
    apt-get install -y sudo && \
    echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME && \
    chmod 0440 /etc/sudoers.d/$USERNAME

USER $USERNAME

COPY --from=builder /opt/poetry /opt/poetry
COPY --from=builder /ailab_line/pyproject.toml poetry.lock* /ailab_line/
COPY --from=builder --chown=$USER_UID:$USER_GID /root/.cache/pypoetry $HOME/.cache/pypoetry
COPY --chown=$USER_UID:$USER_GID entrypoint.sh /usr/local/bin/entrypoint.sh

RUN chmod -R 755 $HOME/.cache && chmod 555 /usr/local/bin/entrypoint.sh

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONUTF8=1 \
    PIP_NO_CACHE_DIR=off  \
    HISTFILESIZE=0 \
    PYTHONPATH="/usr/local/lib/python3.9/site-packages" \
    PYTHONPATH="$HOME/.local/bin:$PYTHONPATH" \
    PATH="$HOME/.local/bin:$PATH"

RUN cd /usr/local/bin && sudo ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false && \
    poetry completions bash >> ~/.bash_completion && \
    cd /ailab_line


# 開発用
FROM base as dev
RUN sudo apt-get update && sudo apt-get install -y \
    git \
    vim \
    && \
    sudo apt-get clean && sudo rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/*
RUN poetry install --no-root && rm -rf ~/.cache/pypoetry


# 本番用
FROM base as prod
RUN poetry install --no-root --no-dev && rm -rf ~/.cache/pypoetry
