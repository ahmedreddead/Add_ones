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
RUN apt-get install -y python3 
RUN apt-get install -y python3-dev 
RUN apt-get install -y git
RUN apt-get install -y libgtk2.0-dev
RUN apt-get install -y libavcodec-dev 
RUN apt-get install -y libavformat-dev
RUN apt-get install -y libswscale-dev 
RUN apt-get install -y libjpeg-dev 
RUN apt-get install -y libpng-dev 
RUN apt-get install -y libtiff-dev
RUN apt-get install -y libjasper-dev 
RUN apt-get install -y libv4l-dev 

#RUN sudo apt-get install ffmpeg

RUN apt-get install -y python3-pip

RUN pip install pandas numpy ipython pyzmq tornado opencv-python ffmpeg

#RUN sudo add-apt-repository ppa:jon-severinsson/ffmpeg
#RUN sudo apt-get update
#RUN sudo apt-get install ffmpeg


CMD ["python" , "./rtmp.py"]
