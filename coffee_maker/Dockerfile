ARG BUILD_FROM
FROM $BUILD_FROM
ENV LANG C.UTF-8
# Copy data for add-on
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
#SHELL ["/bin/bash", "-o", "pipefail", "-c"]



FROM ghcr.io/hassio-addons/debian-base/amd64:4.1.2

RUN apt-get -y update 
RUN apt-get -y upgrade
#RUN apt-get -y install python3 
#RUN apt-get -y install python3-dev 


#RUN apt-get -y install git
#RUN apt-get -y install libgtk2.0-dev


RUN apt-get -y install python3-pip

RUN apt-get -y install pkg-config
RUN apt-get -y install python-dev=2.7.16-1 
RUN apt-get -y install python3-dev=3.7.3-1
RUN apt-get -y install python3-distutils=3.7.3-1
RUN apt-get -y install python3-minimal=3.7.3-1
RUN apt-get -y install zlib1g-dev=1:1.2.11.dfsg-1
        
RUN pip install pyzk paho-mqtt wheel 	

COPY main.py /


ADD main.py .


CMD ["python3" , "./main.py"]
