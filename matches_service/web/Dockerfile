FROM python:3.4
ENV PYTHONUNBUFFERED 1
RUN apt-get update; RUN sudo apt-get install gdal-bin; apt-get --assume-yes install binutils libproj-dev gdal-bin

#RUN wget http://download.osgeo.org/geos/geos-3.4.2.tar.bz2
#RUN tar -xjf geos*
#RUN cd geos*; ./configure; make; make install

RUN apt-get install libgeos-dev

#RUN wget http://download.osgeo.org/gdal/1.11.0/gdal-1.11.0.tar.gz
#RUN tar -xzf gdal-1.11.0.tar.gz
#RUN cd gdal-1.11.0; ./configure; make; make install

RUN apt-get install -y rabbitmq-server
RUN rabbitmq-plugins enable rabbitmq_management
RUN service rabbitmq-server start

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code
RUN pip install -r requirements.txt

ADD . /code/

#ENTRYPOINT celery -A web worker --concurrency=5 --loglevel=info
