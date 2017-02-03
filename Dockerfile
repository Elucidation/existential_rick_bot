FROM phusion/baseimage:latest
MAINTAINER Sam <elucidation@gmail.com>

# Use baseimage-docker's init system.
CMD ["/sbin/my_init"]

RUN apt-get -y update && apt-get install -y \
  python \
  python-pip \
  screen \
   && apt-get clean
RUN pip install --upgrade praw

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY . /tmp/erb/
# Once the docker instance is up, copy over your praw.ini file for credentials
# into /tmp/erb
# Then manually start the script from inside in headless mode using:
# $ cd /tmp/erb && nohup python /tmp/erb/existential_rick_bot > out.log 2> out_error.log &