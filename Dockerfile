# debian with Python preinstalled
FROM python:3.7-slim-buster

ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux

# copy dependency information
COPY requirements.txt /

# install Python packages
RUN /usr/local/bin/python -m pip install --upgrade pip && pip install -r /requirements.txt

# copy sources
RUN mkdir /app
#COPY asp.proto server.py /app/
COPY protobuf/iris.proto irisServer.py /app/

# adhere to container specification by also providing these two files
COPY protobuf/iris.proto /model.proto
#COPY license.json /license.json

WORKDIR /app

# compile protobuf
RUN python3 -m grpc_tools.protoc --python_out=. --proto_path=. --grpc_python_out=. iris.proto

EXPOSE 8061

# run server
CMD python3 irisServer.py
