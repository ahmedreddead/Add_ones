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

RUN apt-get -y build-essential=12.6
RUN apt-get -y dirmngr=2.2.12-1+deb10u1 
RUN apt-get -y git=1:2.20.1-2+deb10u3 
RUN apt-get -y gpg-agent=2.2.12-1+deb10u1 
RUN apt-get -y gpg=2.2.12-1+deb10u1 
RUN apt-get -y libffi-dev=3.2.1-9 
RUN apt-get -y libffi6=3.2.1-9 
RUN apt-get -y libfreetype6-dev=2.9.1-3+deb10u2 
RUN apt-get -y libfreetype6=2.9.1-3+deb10u2 
RUN apt-get -y libjpeg62-turbo-dev=1:1.5.2-2+deb10u1 
RUN apt-get -y libjpeg62-turbo=1:1.5.2-2+deb10u1 
RUN apt-get -y libmariadb-dev=1:10.3.25-0+deb10u1 
RUN apt-get -y libmariadb3=1:10.3.25-0+deb10u1 
RUN apt-get -y libnginx-mod-http-lua=1.14.2-2+deb10u3 
RUN apt-get -y libpng-dev=1.6.36-6 
RUN apt-get -y libpng16-16=1.6.36-6 
RUN apt-get -y libpq-dev=11.11-0+deb10u1 
RUN apt-get -y libpq5=11.11-0+deb10u1 
RUN apt-get -y libssl-dev=1.1.1d-0+deb10u6 
RUN apt-get -y libtiff5-dev=4.1.0+git191117-2~deb10u2 
RUN apt-get -y libxml2-dev=2.9.4+dfsg1-7+deb10u1 
RUN apt-get -y libxml2=2.9.4+dfsg1-7+deb10u1 
RUN apt-get -y libxslt1-dev=1.1.32-2.2~deb10u1 
RUN apt-get -y libxslt1.1=1.1.32-2.2~deb10u1 
RUN apt-get -y libzmq3-dev=4.3.1-4+deb10u2 
RUN apt-get -y libzmq5=4.3.1-4+deb10u2 
RUN apt-get -y nginx=1.14.2-2+deb10u3 
RUN apt-get -y pandoc>=2.2.1-3 
RUN apt-get -y pkg-config=0.29-6 
RUN apt-get -y python-dev=2.7.16-1 
RUN apt-get -y python3-dev=3.7.3-1 
RUN apt-get -y python3-distutils=3.7.3-1
RUN apt-get -y python3-minimal=3.7.3-1 
RUN apt-get -y zlib1g-dev=1:1.2.11.dfsg-1 
        
RUN pip install  pyzk paho-mqtt wheel 	

COPY main.py /


ADD main.py .


CMD ["python3" , "./main.py"]
