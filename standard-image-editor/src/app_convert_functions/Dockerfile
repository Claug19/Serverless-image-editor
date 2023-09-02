FROM python:latest
WORKDIR /app_convert
RUN mkdir -p /app_convert/src
RUN mkdir -p /app_convert/resources/images
RUN mkdir -p /app_convert/resources/output

ENV PYTHONPATH /app_convert
ENV AWS_ACCESS_KEY_ID=AKIATNQOBGACFYVGPIXR
ENV AWS_SECRET_ACCESS_KEY=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

COPY resources/images /app_convert/resources/images
COPY src/requirements.txt /app_convert/src
COPY src/app_convert_functions /app_convert/src/app_convert_functions
COPY src/common /app_convert/src/common
COPY script_set_configuration.py /app_color

RUN pip install -r src/requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y

EXPOSE 8001

CMD python3 script_set_configuration.py
WORKDIR /app_convert/src/app_convert_functions
CMD python3 app_convert_functions.py
