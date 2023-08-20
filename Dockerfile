# Pull base image
FROM python:3.10.0

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# Set work directory
WORKDIR /app

# Install dependencies
COPY ./requirements.txt /app/
# think this may work
RUN apt-get update && apt-get install ffmpeg -y && apt-get install python3-gevent -y
RUN pip install gunicorn

RUN pip install -r requirements.txt

# Copy project
COPY . /app/
# Solves issue of a patch for the Pytube package that hasnt yet been merged to the pytube library, Love it!
COPY /transcribe/cipher.py /usr/local/lib/python3.10/site-packages/pytube/

# Collect static files
RUN python manage.py collectstatic --noinput