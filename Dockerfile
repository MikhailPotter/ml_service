FROM python:3.10

WORKDIR /big_app
COPY ./pyproject.toml ./poetry.lock ./app/main.py /big_app
COPY ./app /big_app/app

RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry install

CMD poetry run python main.py

EXPOSE 8000