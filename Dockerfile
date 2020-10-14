# Pull official base image.
FROM python:3.8-alpine

# Set work directory.
WORKDIR /app

# Set environmental variables.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
ENV DEBUG 0

# Install psycopg2.
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk del build-deps

# Install dependencies.
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy project.
COPY . .

# Add and run as non-root user.
RUN adduser -D myuser
USER myuser
