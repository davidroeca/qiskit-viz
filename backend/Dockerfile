#####################################################################
# Base stage
#####################################################################
FROM python:3.14.2-alpine3.23 AS base

# Accept user ID as build argument
ARG USERID=1001

# Install system dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    cargo \
    rust \
    curl

RUN addgroup -g ${USERID} dev \
    && adduser -D -u ${USERID} -G dev dev

RUN mkdir -p /home/dev/src && chown dev:dev /home/dev/src

WORKDIR /home/dev/src

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY --chown=dev:dev pyproject.toml uv.lock ./

#####################################################################
# Production dependencies stage
#####################################################################
FROM base AS deps-prod
USER dev
RUN uv sync --frozen --no-dev

#####################################################################
# Development dependencies stage
#####################################################################
FROM base AS deps-dev
USER dev
RUN uv sync --frozen

#####################################################################
# Development stage
#####################################################################
FROM base AS development
USER root

COPY --from=deps-dev --chown=dev:dev /home/dev/src/.venv /home/dev/src/.venv

COPY --chown=dev:dev . .

USER dev
WORKDIR /home/dev/src
EXPOSE 8000
ENV PYTHONUNBUFFERED=1
ENV PATH="/home/dev/src/.venv/bin:$PATH"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

#####################################################################
# Production stage
#####################################################################
FROM base AS production
USER root

COPY --from=deps-prod --chown=dev:dev /home/dev/src/.venv /home/dev/src/.venv

COPY --chown=dev:dev . .

USER dev
WORKDIR /home/dev/src
EXPOSE 8000
ENV PYTHONUNBUFFERED=1
ENV PATH="/home/dev/src/.venv/bin:$PATH"
CMD ["python", "main.py"]
