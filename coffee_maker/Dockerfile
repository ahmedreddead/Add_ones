ARG BUILD_FROM
FROM $BUILD_FROM
ENV LANG C.UTF-8
# Copy data for add-on
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]

FROM python:3.9

ADD main.py .

RUN pip install paho-mqtt 
RUN pip install pyzk

CMD ["python3" , "./main.py"]
