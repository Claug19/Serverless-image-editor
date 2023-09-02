FROM python:latest
WORKDIR /app_edit
RUN mkdir -p /app_edit/src
RUN mkdir -p /app_edit/resources/images
RUN mkdir -p /app_edit/resources/output

ENV PYTHONPATH /app_edit
ENV AWS_ACCESS_KEY_ID=AKIATNQOBGACFYVGPIXR
ENV AWS_SECRET_ACCESS_KEY=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

COPY resources/images /app_edit/resources/images
COPY src/requirements.txt /app_edit/src
COPY src/app_edit_functions /app_edit/src/app_edit_functions
COPY src/common /app_edit/src/common
COPY script_set_configuration.py /app_color

RUN pip install -r src/requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y

EXPOSE 8002

CMD python3 script_set_configuration.py
WORKDIR /app_edit/src/app_edit_functions
CMD python3 app_edit_functions.py
