ARG BUILD_FROM
FROM $BUILD_FROM
ENV LANG C.UTF-8
# Copy data for add-on
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]

FROM python:3.9

ADD rtmp.py .

RUN apt-get update && apt-get install -y python3-opencv

#RUN sudo apt-get install ffmpeg

RUN pip install pandas numpy ipython pyzmq tornado opencv-python ffmpeg

#RUN sudo add-apt-repository ppa:jon-severinsson/ffmpeg
#RUN sudo apt-get update
#RUN sudo apt-get install ffmpeg

RUN wget http://launchpadlibrarian.net/339874908/libav-tools_3.3.4-2_all.deb
RUN sudo apt install ./libav-tools_3.3.4.2_all.deb

CMD ["python" , "./rtmp.py"]
