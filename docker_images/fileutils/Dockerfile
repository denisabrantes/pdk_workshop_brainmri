FROM determinedai/environments:py-3.8-pytorch-1.12-tf-2.11-cpu-2b7e2a1

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY validate.py /app
COPY convert.py /app
COPY resize.py /app
COPY report.py /app
COPY utils.py /app

ENV http_proxy=
ENV https_proxy=

ENV PYTHONUNBUFFERED=1
