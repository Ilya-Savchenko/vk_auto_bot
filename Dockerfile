FROM python:3.8.10-slim

RUN pip install pipenv

RUN mkdir /app
COPY . /app/

ENV PIPENV_VENV_IN_PROJECT enabled

WORKDIR /app

RUN pipenv install --deploy --ignore-pipfile
CMD ["pipenv", "run", "python", "bot.py"]
