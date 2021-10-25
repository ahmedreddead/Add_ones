ARG BUILD_FROM
FROM $BUILD_FROM
ENV LANG C.UTF-8
# Copy data for add-on
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]

FROM python:4.0

ADD main.py .

RUN pip install pyzk paho-mqtt wheel 	

CMD ["python" , "./main.py"]
