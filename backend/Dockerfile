FROM python:3.12

RUN pip install --upgrade pip

RUN mkdir /usr/backend

WORKDIR /usr/backend

ADD requirements.txt /usr/backend/

RUN pip install -r requirements.txt

ADD . /usr/backend/

CMD ["bash"]
