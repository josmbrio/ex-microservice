FROM python:3.9.15-slim-buster
WORKDIR /app
COPY ./requirements.txt ./requirements.txt
RUN pip3 install -r ./requirements.txt
COPY ./application/ .
CMD ["python3", "main.py"]
