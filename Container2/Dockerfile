FROM ubuntu:16.04

MAINTAINER Yash Suhagiya <yasu279d@msx.tu-dresden.de>

RUN apt-get update
RUN apt-get upgrade -y

RUN apt-get install -y openssh-server sudo
ENV git_key="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDcFj9AJ0yx2NswwEKPFQZqpiYZ8Mzk1LlRNatsVQqUfaDoQTKewuHRpp5jREB9RIMPczgFPDZSOBQ+mV8u5qJScmOcB8rhaF0GZkF1KIgHSNj8VqDNZWP52m1+NxSJetp6Opu3zTzkoZt9uo4HHeVZseTfN0UkxSjcWKYPX7+rOrvMhIxxKB9bR7UjmMkmoMfzP8UVkmc4MxIOo+RW9OM9GFselGN9JTYceZW8xhWNH2ENXQNWE5a807vP6kaKWp5bQ/c7NpISvTAO5UaVD26IRrtqea//MiUORjbXX+dEpFZuN6fRMh+zemerQ9rDHcgxRMacGZxBUjIRCa92zSr3 gitlab-runner@sep"
ENV local_key="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCm+6aRn0v+2ZGWwB/0ofMrXOJKzECXW3lZKuJXaGMTrKia88w5PzhT7T6vlGX8ebAvB4rO00e7Ue/trkrsK++x8+QTvHxUYxS53o6RNAcNiSkrVTb2dGE5DLuwqN5Es3jseIWhscnsKVDl0K35V3dNQqmazb6Oq+rMGCKennsTSQg56zohgZPDzH7/Km1H6Kje/fQ5HkIMkRtSJ5TUuG1umlM0eEfrh12+0Qbvbmu+wW2mucqGD6IR2KVyLhtX0C7MSB6+wVhZNJab7hN0E2uYGj7Gkq+YOF9W1Bq0A70ISlxSoPBGNXGS/kvPEvV2z7Ng3M9+6KfBXpgYYk0tjwptKYT5Sr8j7ENEKKjl0PNpTOHfq7vfTIURYsy0JjJU3gRVVWKLEKX9kNq/DmUc+4fS7Qu8gjwDgNKE4afOiWa6+ZfVUbks09FSu2KCrjayswifTiZLdAC84DmvsxOlb/SMpPEoTajC6MkvSkofOaYdrQ5WTaumx3+N0SpklKp3rs0= yash suhagiya@DESKTOP-JQP2N2O"

RUN mkdir -p /home/ubuntu/.ssh
RUN mkdir -p /root/.ssh
COPY sshcontainerkey /home/ubuntu/.ssh/
RUN echo "$git_key\n" > /home/ubuntu/.ssh/authorized_keys
RUN echo "$local_key\n" >> /home/ubuntu/.ssh/authorized_keys
RUN chmod 600 /home/ubuntu/.ssh/authorized_keys
RUN chmod 700 /home/ubuntu/.ssh/sshcontainerkey

RUN cp /home/ubuntu/.ssh/authorized_keys /root/.ssh/authorized_keys

COPY sshd_config /home/ubuntu/.ssh/sshd_config
RUN chmod 700 /home/ubuntu/.ssh/sshd_config

RUN apt-get install -y gcc make wget
RUN cd /home/ubuntu
RUN wget https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/twemperf/mcperf-0.1.1.tar.gz
RUN tar zxvf mcperf-0.1.1.tar.gz
RUN cd mcperf-0.1.1 && ./configure && make && make install
RUN rm -f /mcperf-0.1.1.tar.gz

RUN apt install -y r-base python git
RUN git clone https://bitbucket.org/db7/dude.git
RUN cd /dude && python setup.py install


RUN service ssh start
RUN useradd -ms /bin/bash -g root -G sudo -u 1000 ubuntu

RUN cp /etc/ssh /home/ubuntu/ssh -r

COPY run.sh /home/ubuntu/
COPY graphs.R /home/ubuntu/
COPY Benchmark.py /home/ubuntu/
COPY Dudefile /home/ubuntu/

RUN chmod -R 700 /home/ubuntu/
RUN chown -R ubuntu /home/ubuntu/
RUN chmod 600 /home/ubuntu/.ssh/authorized_keys
WORKDIR /home/ubuntu

EXPOSE 10022

USER ubuntu

CMD ["/usr/sbin/sshd","-D","-f","/home/ubuntu/.ssh/sshd_config"]
