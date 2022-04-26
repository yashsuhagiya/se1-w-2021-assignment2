FROM ubuntu:16.04
      
MAINTAINER Yash Suhagiya <yasu279d@msx.tu-dresden.de>

RUN apt-get update
RUN apt-get upgrade -y

RUN apt-get install -y openssh-server libevent-dev build-essential wget make sudo gcc

ENV git_key="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDcFj9AJ0yx2NswwEKPFQZqpiYZ8Mzk1LlRNatsVQqUfaDoQTKewuHRpp5jREB9RIMPczgFPDZSOBQ+mV8u5qJScmOcB8rhaF0GZkF1KIgHSNj8VqDNZWP52m1+NxSJetp6Opu3zTzkoZt9uo4HHeVZseTfN0UkxSjcWKYPX7+rOrvMhIxxKB9bR7UjmMkmoMfzP8UVkmc4MxIOo+RW9OM9GFselGN9JTYceZW8xhWNH2ENXQNWE5a807vP6kaKWp5bQ/c7NpISvTAO5UaVD26IRrtqea//MiUORjbXX+dEpFZuN6fRMh+zemerQ9rDHcgxRMacGZxBUjIRCa92zSr3 gitlab-runner@sep"
ENV local_key="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCm+6aRn0v+2ZGWwB/0ofMrXOJKzECXW3lZKuJXaGMTrKia88w5PzhT7T6vlGX8ebAvB4rO00e7Ue/trkrsK++x8+QTvHxUYxS53o6RNAcNiSkrVTb2dGE5DLuwqN5Es3jseIWhscnsKVDl0K35V3dNQqmazb6Oq+rMGCKennsTSQg56zohgZPDzH7/Km1H6Kje/fQ5HkIMkRtSJ5TUuG1umlM0eEfrh12+0Qbvbmu+wW2mucqGD6IR2KVyLhtX0C7MSB6+wVhZNJab7hN0E2uYGj7Gkq+YOF9W1Bq0A70ISlxSoPBGNXGS/kvPEvV2z7Ng3M9+6KfBXpgYYk0tjwptKYT5Sr8j7ENEKKjl0PNpTOHfq7vfTIURYsy0JjJU3gRVVWKLEKX9kNq/DmUc+4fS7Qu8gjwDgNKE4afOiWa6+ZfVUbks09FSu2KCrjayswifTiZLdAC84DmvsxOlb/SMpPEoTajC6MkvSkofOaYdrQ5WTaumx3+N0SpklKp3rs0= yash suhagiya@DESKTOP-JQP2N2O"
ENV container_key="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCy7Sej2ILVyN4so7eH5tT9pu6eOXlprCSsDhZHlrrPn4z9dQXI2uVyOMC8U0WozWVPIkibC6Oj4t5Z7oCfotOePyp/o+CMUzEUiak7+sKYloRpqPNoOGIFNmdyUjBpVVi6S8pHAQCdHQtMfkmmq62UwxlfUWr1hUkI76ksiOxHdrMEqtpuglfNnY1bEIqw2SS9dr5JUqd4CeqtNi9i4JJgVH9+Rrc7EM0TGsR2wNLkDS7GXzFhvve2RPJWUpnujEqmfqTh56bulX9HE1vng0FiPoIpfVL4kdyTt7Hiq7bU4tvEFgzDk/BKbKM130vxSmEGb89CtSgmftPBbKpFp4Zd ubuntu@01b9676b7fdd"

RUN wget https://github.com/libevent/libevent/releases/download/release-2.1.8-stable/libevent-2.1.8-stable.tar.gz
RUN tar -zxf libevent-2.1.8-stable.tar.gz
RUN cd /libevent-2.1.8-stable && ./configure -prefix=/usr && make && make install
RUN cd / 
RUN rm -fv libevent-2.1.8-stable.tar.gz

RUN wget https://memcached.org/files/memcached-1.6.12.tar.gz
RUN tar -xvf memcached-1.6.12.tar.gz -C .
RUN memcached-1.6.12/configure && make && make install
RUN rm -fv memcached-1.6.12.tar.gz

RUN mkdir -p /home/ubuntu/.ssh

RUN echo "$git_key\n" > /home/ubuntu/.ssh/authorized_keys
RUN echo "$local_key\n" >> /home/ubuntu/.ssh/authorized_keys
RUN echo "$container_key\n" >> /home/ubuntu/.ssh/authorized_keys
RUN chmod -R 700 /home/ubuntu/.ssh/
RUN chmod 600 /home/ubuntu/.ssh/authorized_keys

COPY sshd_config /home/ubuntu/.ssh/sshd_config
RUN chmod 700 /home/ubuntu/.ssh/sshd_config

RUN service ssh start

RUN useradd -ms /bin/bash -g root -G sudo -u 1000 ubuntu

RUN cp /etc/ssh /home/ubuntu/ssh -r
RUN chown -R ubuntu /home/ubuntu/

WORKDIR /home/ubuntu

EXPOSE 20022 11211

USER ubuntu

CMD ["/usr/sbin/sshd","-D","-f","/home/ubuntu/.ssh/sshd_config"]