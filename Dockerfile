FROM ubuntu:jammy

WORKDIR /app
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y python3 python3-pip libopencv-contrib-dev -y

RUN cd / && rm -rf /app && apt autoremove -y && apt clean -y

RUN python3 -m pip install --upgrade pip

COPY . .

RUN python3 -m pip install .

ENTRYPOINT ["robotraconteur-camera-driver"]
