FROM ubuntu:14.04

RUN apt-get update && apt-get install -yq \
        postgresql-client \
        build-essential \
        cmake \
        git \
        wget \
        unzip \
        pkg-config \
        libswscale-dev \
        python \
        python-dev \
        python-pip \
        python-numpy \
        python-opencv \
        libtbb2 \
        libtbb-dev \
        libjpeg-dev \
        libpng-dev \
        libtiff-dev \
        libjasper-dev \
        libavformat-dev \
        libpq-dev \
    && apt-get -y clean all \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD ./ .

EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:8000
