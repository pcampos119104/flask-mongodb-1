
FROM python:3.8-slim

WORKDIR /app

RUN pip install pipenv
COPY Pipfile* ./
RUN pipenv install --system 

COPY . .

# CMD exec gunicorn -b 0.0.0.0:8080 --workers 1 --threads 8 app:app
CMD [ "python", "app.py" ]


