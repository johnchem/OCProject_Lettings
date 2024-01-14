FROM python:3.10-alpine3.19

RUN apk update \
&& apk add git \
&& apk add --no-cache --upgrade bash

WORKDIR /OCProject_Lettings
COPY . /OCProject_Lettings

ENV VIRTUAL_ENV=/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"


RUN pip3 install --upgrade pip \
&& pip3 install -r requirements.txt --no-cache-dir

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=oc_lettings_site.settings
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# RUN <<EDF
# addgroup -S docker
# adduser -S --shell /bin/bash --ingroup vscode
# EOF

# ENTRYPOINT [ "python3" ]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["manage.py", "runserver"]

LABEL version="0.1"