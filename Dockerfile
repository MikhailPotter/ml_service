FROM python:3.10

WORKDIR /code
COPY ./pyproject.toml ./poetry.lock ./api/main.py /code
COPY ./src/api /code/api

RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry install

CMD poetry run python main.py

EXPOSE 8000