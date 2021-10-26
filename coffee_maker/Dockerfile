ARG BUILD_FROM
FROM $BUILD_FROM
ENV LANG C.UTF-8
# Copy data for add-on
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]

FROM ubuntu:21.04

RUN apt-get -y update 
RUN apt-get -y upgrade
RUN apt-get -y install python3 
RUN apt-get -y install python3-dev 

RUN apt-get -y install libavcodec-dev 
RUN apt-get -y install libavformat-dev
RUN apt-get -y install libswscale-dev 
RUN apt-get -y install libjpeg-dev 
RUN apt-get -y install libpng-dev 
RUN apt-get -y install libtiff-dev
RUN apt-get -y install libv4l-dev 

RUN apt-get -y install python3-pip

RUN pip install pandas numpy ipython pyzmq tornado pyzk paho-mqtt

COPY main.py /


ADD main.py .


CMD ["python3" , "./main.py"]
