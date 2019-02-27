FROM python:3.6-alpine
RUN apk update
RUN apk add --update --no-cache \
    gcc \
    tzdata \
    openssl-dev \
    libxml2 \
    libxml2-dev \
    libffi \
    libffi-dev \
    libxslt-dev \
	build-base \
    && pip install scrapy \
    && rm -rf /var/cache/apk/*
WORKDIR /usr
CMD ["/bin/sh"]