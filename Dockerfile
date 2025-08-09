FROM python:3.13.5

WORKDIR /app
COPY . /app

RUN pip install poetry
RUN poetry install

CMD ["sleep", "5", ";", "poetry", "run", "gunicorn", "backend.app.wsgi:app"]