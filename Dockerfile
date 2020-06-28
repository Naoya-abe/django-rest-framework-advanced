FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
# apk: Alpineのパッケージマネージャ
# --update: 取得できるパッケージを最新版にする
# --no-cache: Dockerのイメージを小さくしたいので、cacheを残さない
RUN apk add --update --no-cache postgresql-client
# --virtual .tmp-build-deps
# 複数のパッケージを追加する際に、仮想的に1つにまとめて
# 後々、容易にパッケージ群を削除できるようにする
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt
# .tmp-build-depsを削除
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user