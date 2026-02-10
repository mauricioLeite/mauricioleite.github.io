FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
  curl \
  wget \
  git \
  build-essential \
  ca-certificates \
  gnupg \
  lsb-release \
  software-properties-common \
  python3 \
  python3-pip \
  python3-dev \
  && rm -rf /var/lib/apt/lists/*

RUN wget https://go.dev/dl/go1.25.7.linux-amd64.tar.gz && \
  tar -C /usr/local -xzf go1.25.7.linux-amd64.tar.gz && \
  rm go1.25.7.linux-amd64.tar.gz

ENV PATH=$PATH:/usr/local/go/bin
ENV GOPATH=/go
ENV PATH=$PATH:$GOPATH/bin

RUN wget https://github.com/gohugoio/hugo/releases/download/v0.155.2/hugo_0.155.2_linux-amd64.deb && \
  dpkg -i hugo_0.155.2_linux-amd64.deb && \
  rm hugo_0.155.2_linux-amd64.deb;

WORKDIR /app

COPY go.mod go.sum ./
COPY hugo.yaml ./

RUN go mod download

COPY . .

RUN hugo

EXPOSE 1313

CMD ["hugo", "server", "--logLevel", "info", "--disableFastRender", "-p", "1313", "--bind", "0.0.0.0"]