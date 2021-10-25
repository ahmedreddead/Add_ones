ARG BUILD_FROM
FROM $BUILD_FROM
ENV LANG C.UTF-8
# Copy data for add-on
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
#SHELL ["/bin/bash", "-o", "pipefail", "-c"]



FROM debian

RUN apt-get -y update 
RUN apt-get -y upgrade
RUN sudo apt -y install software-properties-common
RUN sudo add-apt-repository ppa:deadsnakes/ppa
RUN sudo apt -y install python3.7
#RUN apt-get -y install python3
#RUN apt-get -y install python3-dev 


#RUN apt-get -y install git
#RUN apt-get -y install libgtk2.0-dev


RUN apt-get -y install python3-pip

RUN apt-get -y install pkg-config
RUN apt-get -y install python-dev
RUN apt-get -y install python3-dev
RUN apt-get -y install python3-distutils
RUN apt-get -y install python3-minimal
        
RUN pip install pyzk paho-mqtt wheel 	

COPY main.py /


ADD main.py .


CMD ["python3" , "./main.py"]
