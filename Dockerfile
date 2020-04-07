FROM ubuntu:16.04

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev libmysqlclient-dev libcogl-pango-dev  libcairo2-dev  python3-venv \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && rm -fr /var/lib/apt/lists/*

WORKDIR /project


COPY . .

RUN pip3 install --upgrade pip

RUN pip3 install --upgrade setuptools && \
    pip3 install -r etc/requirements.txt

RUN touch ./django_shop/error.log ./django_shop/logs.log


ENV STATIC_ROOT="/project/staticfiles/static" MEDIA_ROOT="/project/staticfiles/media"

EXPOSE 8000


