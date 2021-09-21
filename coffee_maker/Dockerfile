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
RUN sudo apt install ffmpeg


RUN pip install pandas numpy ipython pyzmq tornado opencv-python


CMD ["python" , "./rtmp.py"]
