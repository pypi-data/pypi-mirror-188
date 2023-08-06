FROM python:3.8

COPY . /app/
VOLUME ./output:/app/output
VOLUME ./coverage:/app/coverage/

WORKDIR /app

ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"

# Installs poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \ 
  poetry install --no-interaction --no-ansi --no-root -vvv

CMD python src/main.py

