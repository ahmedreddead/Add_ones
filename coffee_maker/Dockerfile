ARG BUILD_FROM
FROM $BUILD_FROM
ENV LANG C.UTF-8
# Copy data for add-on
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
SHELL ["/bin/bash", "-o", "pipefail", "-c"]


FROM ghcr.io/hassio-addons/debian-base/amd64:4.1.2

RUN \
    MAKEFLAGS="-j$(nproc)" \
    && export MAKEFLAGS \
    \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential=12.6 \
        dirmngr=2.2.12-1+deb10u1 \
        git=1:2.20.1-2+deb10u3 \
        gpg-agent=2.2.12-1+deb10u1 \
        gpg=2.2.12-1+deb10u1 \
        libffi-dev=3.2.1-9 \
        libffi6=3.2.1-9 \
        libfreetype6-dev=2.9.1-3+deb10u2 \
        libfreetype6=2.9.1-3+deb10u2 \
        libjpeg62-turbo-dev=1:1.5.2-2+deb10u1 \
        libjpeg62-turbo=1:1.5.2-2+deb10u1 \
        libmariadb-dev=1:10.3.25-0+deb10u1 \
        libmariadb3=1:10.3.25-0+deb10u1 \
        libnginx-mod-http-lua=1.14.2-2+deb10u3 \
        libpng-dev=1.6.36-6 \
        libpng16-16=1.6.36-6 \
        libpq-dev=11.11-0+deb10u1 \
        libpq5=11.11-0+deb10u1 \
        libssl-dev=1.1.1d-0+deb10u6 \
        libtiff5-dev=4.1.0+git191117-2~deb10u2 \
        libxml2-dev=2.9.4+dfsg1-7+deb10u1 \
        libxml2=2.9.4+dfsg1-7+deb10u1 \
        libxslt1-dev=1.1.32-2.2~deb10u1 \
        libxslt1.1=1.1.32-2.2~deb10u1 \
        libzmq3-dev=4.3.1-4+deb10u2 \
        libzmq5=4.3.1-4+deb10u2 \
        nginx=1.14.2-2+deb10u3 \
        pandoc>=2.2.1-3 \
        pkg-config=0.29-6 \
        python-dev=2.7.16-1 \
        python3-dev=3.7.3-1 \
        python3-distutils=3.7.3-1 \
        python3-minimal=3.7.3-1 \
        zlib1g-dev=1:1.2.11.dfsg-1 \
    \
    && curl -sL https://deb.nodesource.com/setup_12.x | bash - \
    \
    && apt-get install -y --no-install-recommends \
        nodejs=12.22.0-1nodesource1 \
    \
    && curl https://bootstrap.pypa.io/get-pip.py | python3 \
    \
    && update-alternatives \
        --install /usr/bin/python python /usr/bin/python3 10 \
    \
    && pip3 install --no-cache-dir numpy==1.20.2 \

RUN pip install  pyzk paho-mqtt wheel future	

COPY main.py /


ADD main.py .


CMD ["python3" , "./main.py"]
