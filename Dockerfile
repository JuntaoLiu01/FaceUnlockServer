FROM ubuntu:16.04

RUN apt-get -y update
RUN apt-get install -y --fix-missing \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-dev \
    libavcodec-dev \
    libavformat-dev \
    libboost-all-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python-dev \
    python-pip \
    build-essential \
    python-numpy \
    python-setuptools \
    software-properties-common \
    zip \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*

RUN cd ~ && \
    mkdir -p dlib && \
    git clone -b 'v19.7' --single-branch https://github.com/davisking/dlib.git dlib/ && \
    cd  dlib/ && \
    python setup.py install --yes USE_AVX_INSTRUCTIONS

RUN pip install --upgrade pip && \
	pip install Flask && \
	pip install Flask-SQLAlchemy && \
	pip install PyMySQL && \
	pip install SQLAlchemy

RUN cd /root && \
    git clone https://github.com/ageitgey/face_recognition && \
    cd face_recognition && \
    pip install -r requirements.txt && \
    python setup.py install

COPY . /app
CMD cd app && \
    python app.py

