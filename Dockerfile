FROM python:3.12

WORKDIR /code

COPY ./poetry.lock /code.poetry.lock
COPY ./pyproject.toml /code/pyproject.toml

RUN pip install --no-cache-dir --upgrade pip poetry
RUN poetry config virtualenvs.create false
RUN poetry install --only=main --no-interaction --no-ansi

COPY app /code/app

CMD ["uvicorn", "--factory", "app.app_setup:default_app_factory", "--host", "0.0.0.0", "--port", "8000"]