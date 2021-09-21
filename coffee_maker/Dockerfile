ARG BUILD_FROM
FROM $BUILD_FROM
ENV LANG C.UTF-8
# Copy data for add-on
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]

FROM ubuntu:21.04


ADD rtmp.py .

RUN apt-get update && apt-get install -y python3-opencv
RUN apt-get install -y python3 \
        python3-dev \
        git \
        wget \
        unzip \
        cmake \
        build-essential \
        pkg-config \
        libatlas-base-dev \
        gfortran \
        libjasper-dev \
        libgtk2.0-dev \
        libavcodec-dev \
        libavformat-dev \
        libswscale-dev \
        libjpeg-dev \
        libpng-dev \
        libtiff-dev \
        libjasper-dev \
        libv4l-dev \

#RUN sudo apt-get install ffmpeg

RUN sudo apt install -y python3-pip

RUN pip install pandas numpy ipython pyzmq tornado opencv-python ffmpeg

#RUN sudo add-apt-repository ppa:jon-severinsson/ffmpeg
#RUN sudo apt-get update
#RUN sudo apt-get install ffmpeg


CMD ["python" , "./rtmp.py"]
