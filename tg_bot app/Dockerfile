FROM python:3.10.3
RUN apt-get update -qy
RUN apt-get install -qy python3-pip python3-dev
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python3","tgbot.py"]