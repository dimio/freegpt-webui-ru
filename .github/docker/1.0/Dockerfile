##################################################################
##################################################################
##################################################################
#                     Build stage   
##################################################################
##################################################################
##################################################################
FROM python:3.10-slim AS build    

ENV FREEGPT_PATH=/app
ENV FREEGPT_PORT=1338
ENV FREEGPT_ENDPOINT_PORT=1337
ENV PATH=/root/.local/bin:${PATH}

##################################################################
#                   prepare system
##################################################################
RUN for i in $(seq 1 8); do mkdir -p "/usr/share/man/man${i}"; done

##################################################################
#                   update lists
##################################################################
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections && \
    apt-get update

##################################################################
#                   installing utils
##################################################################
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections && \
    apt-get install -y --allow-unauthenticated \
    apt-transport-https \
    apt-utils \
    gnupg \
    gnupg1 \
    gnupg2 \
    aptitude \
    bash \
    binutils \
    console-cyrillic \
    ca-certificates \
    locales \
    software-properties-common \
    sudo \
    cron \
    curl \
    git \
    dos2unix \
    util-linux \
    uuid-runtime \
    openssl \
    wget \
    supervisor \
    build-essential \
    libffi-dev cmake \
    libcurl4-openssl-dev

##################################################################
#                   download sources and cleanup
##################################################################
ARG FREEGPT_VERSION=1.0
RUN git clone --depth 1 --branch ${FREEGPT_VERSION} https://github.com/Em1tSan/freegpt-webui-ru.git ${FREEGPT_PATH} && \
    rm -rfv ${FREEGPT_PATH}/.git && \ 
    rm -rfv ${FREEGPT_PATH}/.github && \ 
    rm -rfv ${FREEGPT_PATH}/docker && \ 
    rm -rfv ${FREEGPT_PATH}/docs && \ 
    rm -rfv ${FREEGPT_PATH}/.gitattributes && \ 
    rm -rfv ${FREEGPT_PATH}/.gitignore && \ 
    rm -rfv ${FREEGPT_PATH}/README.MD && \ 
    rm -rfv ${FREEGPT_PATH}/Dockerfile && \ 
    rm -rfv ${FREEGPT_PATH}/docker-compose.yml && \ 
    rm -rfv ${FREEGPT_PATH}/*.bat 

##################################################################
#                   build sources
##################################################################
RUN pip3 install --user --no-cache-dir -r ${FREEGPT_PATH}/requirements.txt   

##################################################################
#                   fix codepage
##################################################################
RUN find ${FREEGPT_PATH} -type f -exec dos2unix -k -s -o {} ';'

##################################################################
##################################################################
##################################################################
#                     Production stage   
##################################################################
##################################################################
##################################################################
FROM python:3.10-slim AS production    

ENV FREEGPT_PATH=/app
ENV FREEGPT_PORT=1338
ENV FREEGPT_ENDPOINT_PORT=1337

##################################################################
#                   prepare system
##################################################################
RUN for i in $(seq 1 8); do mkdir -p "/usr/share/man/man${i}"; done
RUN mkdir -p ${FREEGPT_PATH}

##################################################################
#                   update lists
##################################################################
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections && \
    apt-get update

##################################################################
#                   installing utils
##################################################################
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections && \
    apt-get install -y --allow-unauthenticated \
    apt-transport-https \
    apt-utils \
    gnupg \
    gnupg1 \
    gnupg2 \
    aptitude \
    bash \
    binutils \
    console-cyrillic \
    ca-certificates \
    locales \
    software-properties-common \
    sudo \
    cron \
    curl \
    git \
    dos2unix \
    util-linux \
    uuid-runtime \
    openssl \
    wget \
    supervisor

RUN update-ca-certificates

##################################################################
#                   install supervisord config
##################################################################
COPY etc/supervisor/conf.d/freegpt.conf /etc/supervisor/conf.d/freegpt.conf

##################################################################
#                   copy bins
##################################################################
COPY --from=build /root/.local /usr/local
COPY --from=build /app ${FREEGPT_PATH}

##################################################################
#                   cleaninig up
##################################################################
RUN apt clean -y && \
    apt-get clean all && \
    apt autoclean -y && \
    rm -rfv /var/lib/apt/lists/* && \
    rm -rfv /var/cache/apt/archives/*.deb && \
    rm -rfv /tmp/*

WORKDIR ${FREEGPT_PATH}   
EXPOSE  ${FREEGPT_PORT} ${FREEGPT_ENDPOINT_PORT}

CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/conf.d/freegpt.conf"]
