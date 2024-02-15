FROM python:3.10-alpine3.19

# update and install software in the OS
RUN apk update \
&& apk add --no-cache git \
&& apk add --no-cache gcc \
&& apk add --no-cache g++ \
&& apk add --no-cache --upgrade bash \
&& apk add --no-cache graphviz-dev

#copy source code
WORKDIR /OCProject_Lettings
COPY . /OCProject_Lettings

# set virtual env and install librairies
ENV VIRTUAL_ENV=/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip3 install --upgrade pip \
&& pip3 install -r requirements.txt --no-cache-dir

EXPOSE 8000

# Environment variables to define the settings and avoid
# the storage of .pyc and the buffering of stdout/stderr
ENV DJANGO_SETTINGS_MODULE=oc_lettings_site.settings
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# command to start 
CMD sh ./script.sh

LABEL version="0.2"