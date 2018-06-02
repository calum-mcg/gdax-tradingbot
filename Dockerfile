FROM python:3.6-alpine

ADD . /code
WORKDIR /code

RUN echo "http://dl-8.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
RUN apk --no-cache --update-cache add \
  gcc \
  gfortran \
  python \
  python-dev \
  py-pip \
  build-base \
  wget \
  freetype-dev \
  libpng-dev \
  openblas-dev

RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "example.py"]
