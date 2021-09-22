ARG BUILD_FROM
FROM $BUILD_FROM
ENV LANG C.UTF-8
# Copy data for add-on
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]

FROM ubuntu:21.04
RUN apt-get -y update && apt-get -y install python3 && apt-get -y install python3-dev && apt-get -y install python3-opencv
    
#RUN sudo apt-get update && sudo apt-get install -y python3-opencv
#RUN sudo apt-get install -y python3 
#RUN sudo apt-get install -y python3-dev 

#RUN apt-get -y install git
#RUN apt-get -y install libgtk2.0-dev
RUN apt-get -y install libavcodec-dev 
RUN apt-get -y install libavformat-dev
RUN apt-get -y install libswscale-dev 
RUN apt-get -y install libjpeg-dev 
RUN apt-get -y install libpng-dev 
RUN apt-get -y install libtiff-dev
RUN apt-get -y install libv4l-dev 

RUN apt-get -y install ffmpeg

RUN apt-get -y install python3-pip

RUN pip install pandas numpy ipython pyzmq tornado opencv-python ffmpeg

#RUN sudo add-apt-repository ppa:jon-severinsson/ffmpeg
#RUN sudo apt-get update
#RUN sudo apt-get install ffmpeg
COPY rtmp.py /


ADD rtmp.py .


CMD ["python3" , "./rtmp.py"]
