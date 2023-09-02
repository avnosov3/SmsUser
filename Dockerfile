FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml .

RUN pip install poetry
RUN poetry install

COPY ./backend .
