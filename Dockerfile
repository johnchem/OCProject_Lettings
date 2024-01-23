FROM python:3.10-alpine3.19

RUN apk update \
&& apk add git \
&& apk add --no-cache --upgrade bash

WORKDIR /OCProject_Lettings
COPY . /OCProject_Lettings

ENV VIRTUAL_ENV=/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# RUN --mount=type=secret,id=_env,dst=/etc/secrets/.env cat .env
# RUN --mount=type=secret,id=_env,dst=/etc/secrets/.env cat /etc/secrets/.env
# docker build -t orange_county --secret id=django,src=.env .

RUN pip3 install --upgrade pip \
&& pip3 install -r requirements.txt --no-cache-dir

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=oc_lettings_site.settings
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


CMD ["python3", "manage.py", "collectstatic", "--noinput", "&&", "python3", "manage.py", "runserver", "0.0.0.0:8000"]

LABEL version="0.2"

# Lancez le serveur Django après avoir collecté les fichiers statiques
# CMD ["sh", "-c", "python3 manage.py collectstatic --noinput && python3 manage.py runserver 0.0.0.0:8000"]