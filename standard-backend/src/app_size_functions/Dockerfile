FROM python:latest
WORKDIR /app_size
RUN mkdir -p /app_size/src
RUN mkdir -p /app_size/resources/images
RUN mkdir -p /app_size/resources/output

ENV PYTHONPATH /app_size
ENV AWS_ACCESS_KEY_ID=AKIATNQOBGACFYVGPIXR
ENV AWS_SECRET_ACCESS_KEY=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

COPY resources/images /app_size/resources/images
COPY src/requirements.txt /app_size/src
COPY src/app_size_functions /app_size/src/app_size_functions
COPY src/common /app_size/src/common
COPY script_set_configuration.py /app_color

RUN pip install -r src/requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y

EXPOSE 8004

WORKDIR /app_size/src/app_size_functions
CMD python3 app_size_functions.py
