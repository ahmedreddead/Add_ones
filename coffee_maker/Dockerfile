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
RUN sudo apt-get install deb-multimedia-keyring
RUN apt-get update
RUN sudo apt-get install build-essential libmp3lame-dev libvorbis-dev libtheora-dev libspeex-dev yasm pkg-config libfaac-dev libopenjpeg-dev libx264-dev
RUN sudo apt-get install ffmpeg
RUN pip install pandas numpy ipython pyzmq tornado opencv-python

CMD ["python" , "./rtmp.py"]
