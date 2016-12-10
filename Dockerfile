FROM ubuntu:trusty

ENV DEBIAN_FRONTEND noninteractive

EXPOSE 9090
WORKDIR /src
VOLUME /src

CMD python setup.py develop && python setup.py build && baseplate-serve2 --debug --bind 0.0.0.0:9090 --reload example.ini
