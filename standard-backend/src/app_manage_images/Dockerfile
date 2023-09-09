FROM python:latest
WORKDIR /app_manage
RUN mkdir -p /app_manage/src
RUN mkdir -p /app_manage/resources/images
RUN mkdir -p /app_manage/resources/output

ENV PYTHONPATH /app_manage
ENV AWS_ACCESS_KEY_ID=AKIATNQOBGACFYVGPIXR
ENV AWS_SECRET_ACCESS_KEY=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

COPY resources/images /app_manage/resources/images
COPY src/requirements.txt /app_manage/src
COPY src/app_manage_images /app_manage/src/app_manage_images
COPY src/common /app_manage/src/common
COPY script_set_configuration.py /app_color

RUN pip install -r src/requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y

EXPOSE 8003

WORKDIR /app_manage/src/app_manage_images
CMD python3 app_manage_images.py
