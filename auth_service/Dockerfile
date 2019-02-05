FROM python:3.5

ENV PYTHONUNBUFFERED 1
ENV FLASK_APP /code

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code
RUN pip install -r requirements.txt

ENTRYPOINT [ "flask" ]
