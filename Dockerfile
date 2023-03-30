FROM python:3.9.6-alpine

WORKDIR /app

# do not write pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# do not buffer stdout and stderr
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY /app /app
COPY .env /app

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]