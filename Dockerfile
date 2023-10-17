FROM python:3.11.6-alpine3.18 as builder

RUN pip install poetry==1.6.1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY poetry.lock pyproject.toml ./

# RUN --mount=type=cache,id=c4db0c74-0027-4edf-9670-297c828b3276-cache-poetry,target=$POETRY_CACHE_DIR poetry install --without dev --no-root
RUN poetry install --without dev && \
    rm -rf $POETRY_CACHE_DIR

FROM python:3.11.6-alpine3.18 as runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY . /app

CMD ["python", "main.py"]
