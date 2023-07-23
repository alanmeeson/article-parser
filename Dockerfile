FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    build-essential \
    tesseract-ocr \
    git \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /app
WORKDIR /app

COPY requirements_prod_pt1.txt .
RUN pip install -r requirements_prod_pt1.txt
COPY requirements_prod_pt2.txt .
RUN pip install -r requirements_prod_pt2.txt

COPY . .
RUN pip install -e .

ENTRYPOINT ["article-parser"]
