FROM alpine:latest

RUN apk update
RUN apk add python3
ENV VENV_PATH=/root
RUN python3 -m venv ${VENV_PATH}
ENV PATH="$VENV_PATH/bin:$PATH"
RUN python3 -m ensurepip
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

EXPOSE 6767

COPY . . 

CMD ["gunicorn", "--bind", "0.0.0.0:6767", "--workers", "3", "start:application"]

# docker run -d -p 6767:6767 m3r:latest
