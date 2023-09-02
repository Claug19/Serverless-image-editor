FROM python:latest
WORKDIR /app_color
RUN mkdir -p /app_color/src
RUN mkdir -p /app_color/resources/images
RUN mkdir -p /app_color/resources/output

ENV PYTHONPATH /app_color
ENV AWS_ACCESS_KEY_ID=AKIATNQOBGACFYVGPIXR
ENV AWS_SECRET_ACCESS_KEY=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

COPY resources/images /app_color/resources/images
COPY src/requirements.txt /app_color/src
COPY src/app_color_functions /app_color/src/app_color_functions
COPY src/common /app_color/src/common
COPY script_set_configuration.py /app_color

RUN pip install -r src/requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y

EXPOSE 8000

CMD python3 script_set_configuration.py
WORKDIR /app_color/src/app_color_functions
CMD python3 app_color_functions.py
