FROM ubuntu:16.04

WORKDIR /app

ENV USERNAME=admin
ENV PASSWORD=admin

RUN apt-get update
RUN apt-get install curl
RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
RUN apt-get install git-lfs

ADD run.sh /app/
RUN chmod a+x /app/run.sh

CMD ["./run.sh"]
