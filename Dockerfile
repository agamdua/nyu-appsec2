FROM ubuntu:xenial

WORKDIR /appsec

EXPOSE 5000 5000

COPY requirements.txt .
COPY Makefile .

RUN apt-get update
RUN apt-get install -y python3-pip python3-dev 
RUN make install

ADD . /appsec

CMD make runserver
